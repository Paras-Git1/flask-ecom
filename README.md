# 🛒 Flask E-Commerce Application

A full-featured e-commerce web application built with Flask, SQLAlchemy, and modern web technologies. This application provides a complete online shopping experience with user authentication, product management, shopping cart functionality, and order processing.

![App Screenshot](images/homepage-screenshot.png)

## ✨ Features

### 🔐 User Management
- **User Registration & Authentication**: Secure signup and login system
- **Password Hashing**: Werkzeug security for password protection
- **Session Management**: Secure user sessions
- **Admin & Customer Roles**: Role-based access control

### 🛍️ Shopping Experience
- **Product Catalog**: Browse products with detailed information
- **Product Gallery**: Multiple images per product (up to 4 images)
- **Shopping Cart**: Add, remove, and update quantities
- **Responsive Design**: Works on desktop and mobile devices

![Product Detail Page](images/product-detail-screenshot.png)

### 📦 Order Management
- **Secure Checkout**: Protected checkout process
- **Order Tracking**: Real-time order status updates
- **Order History**: View past orders and their details
- **Shipping Information**: Collect and store shipping details

### 👨‍💼 Admin Panel
- **Product Management**: Add, edit, and delete products
- **Order Management**: Update order statuses
- **Dashboard**: Overview of products and recent orders
- **Stock Management**: Track inventory levels

![Admin Dashboard](images/admin-dashboard-screenshot.png)

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Werkzeug Security
- **Frontend**: HTML, CSS, JavaScript (with Jinja2 templating)
- **Session Management**: Flask Sessions

## 📋 Prerequisites

Before running this application, make sure you have the following installed:

- Python 3.7 or higher
- pip (Python package installer)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/flask-ecommerce-app.git
cd flask-ecommerce-app
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install the dependencies manually:

```bash
pip install flask flask-sqlalchemy werkzeug
```

### 4. Configure the Application

Update the configuration in the main Python file:

```python
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key
```

### 5. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

![Cart Page](images/cart-screenshot.png)

## 🎯 Default Credentials

The application creates a default admin account on first run:

- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@example.com`

⚠️ **Important**: Change these credentials immediately after first login!

## 📁 Project Structure

```
flask-ecommerce-app/
│
├── app.py                  # Main application file
├── ecommerce.db           # SQLite database (created automatically)
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── home.html         # Homepage
│   ├── product_detail.html
│   ├── cart.html
│   ├── checkout.html
│   ├── login.html
│   ├── signup.html
│   ├── admin_dashboard.html
│   └── ...
├── static/               # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
└── README.md
```

## 🔧 Configuration

### Database Configuration

The application uses SQLite by default. To use a different database:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'your-database-url-here'
```

### Security Configuration

Make sure to set a secure secret key:

```python
app.config['SECRET_KEY'] = 'your-very-secure-secret-key'
```

## 📱 Usage Guide

### For Customers:

1. **Browse Products**: Visit the homepage to see available products
2. **View Product Details**: Click on any product to see detailed information
3. **Add to Cart**: Add products to your shopping cart
4. **Register/Login**: Create an account or login to proceed with checkout
5. **Checkout**: Provide shipping information and place your order
6. **Track Orders**: View your order history and track order status

### For Administrators:

1. **Login as Admin**: Use admin credentials to access admin panel
2. **Manage Products**: Add new products, edit existing ones, or remove products
3. **Process Orders**: Update order statuses (placed, processing, shipped, delivered)
4. **Monitor Dashboard**: View overview of products and recent orders

![Order Status Page](images/order-status-screenshot.png)

## 🌐 API Endpoints

### Public Routes
- `GET /` - Homepage with product listing
- `GET /product/<id>` - Product detail page
- `GET /login` - Login page
- `GET /signup` - Registration page

### Protected Routes (Login Required)
- `GET /cart` - Shopping cart
- `GET /checkout` - Checkout page
- `POST /place_order` - Place an order
- `GET /my_orders` - User's order history

### Admin Routes (Admin Access Required)
- `GET /admin` - Admin dashboard
- `POST /admin/add_product` - Add new product
- `PUT /admin/edit_product/<id>` - Edit product
- `DELETE /admin/delete_product/<id>` - Delete product

## 🐛 Troubleshooting

### Common Issues:

1. **Database not found**: The database is created automatically on first run
2. **Module not found**: Make sure you've installed all dependencies with `pip install -r requirements.txt`
3. **Permission denied**: Ensure you have write permissions in the project directory
4. **Secret key warning**: Set a proper SECRET_KEY in production

### Debug Mode:

For development, the app runs in debug mode. For production, set:

```python
app.run(debug=False)
```

## 🚀 Deployment

### Local Deployment

The application is ready to run locally with the setup instructions above.

### Production Deployment

For production deployment, consider:

1. **Use a production WSGI server** (e.g., Gunicorn)
2. **Use a production database** (PostgreSQL, MySQL)
3. **Set environment variables** for sensitive configuration
4. **Enable HTTPS**
5. **Set up proper logging**

Example with Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 app:app
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/flask-ecommerce-app/issues) page
2. Create a new issue with detailed information
3. Contact the maintainers

## 🙏 Acknowledgments

- Flask team for the amazing web framework
- SQLAlchemy for the excellent ORM
- Unsplash for product images
- All contributors who helped improve this project

---

**⭐ If you found this project helpful, please give it a star!**
