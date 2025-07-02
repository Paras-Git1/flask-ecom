from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image1 = db.Column(db.String(200), nullable=False)
    image2 = db.Column(db.String(200))
    image3 = db.Column(db.String(200))
    image4 = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='placed')
    shipping_address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('orders', lazy=True))

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    order = db.relationship('Order', backref=db.backref('items', lazy=True))
    product = db.relationship('Product', backref=db.backref('order_items', lazy=True))

# Helper functions
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user.is_admin:
            flash('Admin access required.', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

def get_cart():
    return session.get('cart', {})

def get_cart_total():
    cart = get_cart()
    total = 0
    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            total += product.price * quantity
    return total

def get_cart_count():
    cart = get_cart()
    return sum(cart.values())

# Routes
@app.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products, cart_count=get_cart_count())

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product, cart_count=get_cart_count())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            flash('Login successful!', 'success')
            
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return render_template('signup.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'error')
            return render_template('signup.html')
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1
    
    session['cart'] = cart
    flash(f'{product.name} added to cart!', 'success')
    return redirect(url_for('product_detail', product_id=product_id))

@app.route('/cart')
def cart():
    cart = get_cart()
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            subtotal = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal
    
    return render_template('cart.html', cart_items=cart_items, total=total, cart_count=get_cart_count())

@app.route('/update_cart', methods=['POST'])
def update_cart():
    product_id = request.form.get('product_id')
    action = request.form.get('action')
    
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    
    if action == 'increase':
        cart[product_id] = cart.get(product_id, 0) + 1
    elif action == 'decrease':
        if product_id in cart and cart[product_id] > 1:
            cart[product_id] -= 1
        elif product_id in cart:
            del cart[product_id]
    elif action == 'remove':
        if product_id in cart:
            del cart[product_id]
    
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/checkout')
@login_required
def checkout():
    cart = get_cart()
    if not cart:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('cart'))
    
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            subtotal = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal
    
    return render_template('checkout.html', cart_items=cart_items, total=total)

@app.route('/place_order', methods=['POST'])
@login_required
def place_order():
    cart = get_cart()
    if not cart:
        flash('Your cart is empty.', 'error')
        return redirect(url_for('cart'))
    
    # Get shipping details
    shipping_address = request.form.get('shipping_address')
    phone = request.form.get('phone')
    
    if not shipping_address or not phone:
        flash('Please provide shipping address and phone number.', 'error')
        return redirect(url_for('checkout'))
    
    # Create order
    order = Order(
        user_id=session['user_id'],
        total_amount=get_cart_total(),
        shipping_address=shipping_address,
        phone=phone,
        status='placed'
    )
    db.session.add(order)
    db.session.flush()  # Get order ID
    
    # Create order items
    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                price=product.price
            )
            db.session.add(order_item)
            
            # Update stock
            product.stock -= quantity
    
    db.session.commit()
    
    # Clear cart
    session['cart'] = {}
    
    flash('Order placed successfully!', 'success')
    return redirect(url_for('order_status', order_id=order.id))

@app.route('/order_status/<int:order_id>')
@login_required
def order_status(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Check if user owns this order or is admin
    if order.user_id != session['user_id'] and not session.get('is_admin'):
        flash('Access denied.', 'error')
        return redirect(url_for('home'))
    
    return render_template('order_status.html', order=order)

@app.route('/my_orders')
@login_required
def my_orders():
    orders = Order.query.filter_by(user_id=session['user_id']).order_by(Order.created_at.desc()).all()
    return render_template('my_orders.html', orders=orders)

# Admin routes
@app.route('/admin')
@admin_required
def admin_dashboard():
    products = Product.query.all()
    orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    total_orders = Order.query.count()
    total_products = Product.query.count()
    return render_template('admin_dashboard.html', 
                         products=products, 
                         orders=orders,
                         total_orders=total_orders,
                         total_products=total_products)

@app.route('/admin/add_product', methods=['GET', 'POST'])
@admin_required
def add_product():
    if request.method == 'POST':
        product = Product(
            name=request.form['name'],
            description=request.form['description'],
            price=float(request.form['price']),
            stock=int(request.form['stock']),
            image1=request.form['image1'],
            image2=request.form.get('image2', ''),
            image3=request.form.get('image3', ''),
            image4=request.form.get('image4', '')
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('add_product.html')

@app.route('/admin/edit_product/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        product.stock = int(request.form['stock'])
        product.image1 = request.form['image1']
        product.image2 = request.form.get('image2', '')
        product.image3 = request.form.get('image3', '')
        product.image4 = request.form.get('image4', '')
        
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('edit_product.html', product=product)

@app.route('/admin/delete_product/<int:product_id>')
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/update_order_status/<int:order_id>', methods=['POST'])
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form['status']
    order.status = new_status
    order.updated_at = datetime.utcnow()
    db.session.commit()
    flash('Order status updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# Initialize database and create default data
def init_db():
    with app.app_context():
        db.create_all()
        
        # Create default admin user
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
        
        # Create default products
        if Product.query.count() == 0:
            products = [
                Product(
                    name='Wireless Bluetooth Headphones',
                    description='High-quality wireless headphones with noise cancellation and 30-hour battery life. Perfect for music lovers and professionals.',
                    price=4999.99,
                    stock=50,
                    image1='https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500',
                    image2='https://images.unsplash.com/photo-1484704849700-f032a568e944?w=500',
                    image3='https://images.unsplash.com/photo-1583394838336-acd977736f90?w=500',
                    image4='https://images.unsplash.com/photo-1524678606370-a47ad25cb82a?w=500'
                ),
                Product(
                    name='Smart Fitness Watch',
                    description='Advanced fitness tracking watch with heart rate monitor, GPS, and smartphone connectivity. Track your health goals.',
                    price=1249.99,
                    stock=30,
                    image1='https://assets.ajio.com/medias/sys_master/root/20250131/YBBX/679cb6242960820c494d998f/-473Wx593H-4944219760-multi-MODEL11.jpg',
                    image2='https://assets.ajio.com/medias/sys_master/root/20250131/XAh1/679cb624bc78b543a90e60d1/-473Wx593H-4944219760-multi-MODEL3.jpg',
                    image3='https://assets.ajio.com/medias/sys_master/root/20250131/ZM1Q/679cb5f1bc78b543a90e5fbd/-473Wx593H-4944219760-multi-MODEL.jpg',
                    image4='https://assets.ajio.com/medias/sys_master/root/20250131/uXno/679cb61dbc78b543a90e601a/-473Wx593H-4944219760-multi-MODEL8.jpg'
                ),
                Product(
                    name='Portable Laptop Stand',
                    description='Ergonomic adjustable laptop stand made from premium aluminum. Improve your posture and productivity.',
                    price=600.99,
                    stock=75,
                    image1='https://www.ikea.com/in/en/images/products/vattenkar-laptop-monitor-stand-birch__1149392_pe884019_s5.jpg?f=xl',
                    image2='https://www.ikea.com/in/en/images/products/vattenkar-laptop-monitor-stand-birch__1149391_pe884020_s5.jpg?f=xl',
                    image3='https://www.ikea.com/in/en/images/products/vattenkar-laptop-monitor-stand-birch__1150514_pe884618_s5.jpg?f=xl',
                    image4='https://www.ikea.com/in/en/images/products/vattenkar-laptop-monitor-stand-birch__1150515_pe884617_s5.jpg?f=xl'
                )
            ]
            
            for product in products:
                db.session.add(product)
        
        db.session.commit()

        @app.context_processor
        def inject_cart_count():
            return dict(cart_count=get_cart_count())


if __name__ == '__main__':
    init_db()
    app.run(debug=True)