Restaurant Management System
This is a Restaurant Management System built using Flask, a lightweight WSGI web application framework in Python. It serves as a platform for managing restaurant inventory, processing orders, and handling customer interactions.

Features
Inventory Management: Keep track of ingredients and supplies in the restaurant inventory.
Menu Management: Create, update, and manage the restaurant menu.
Order Processing: Accept and process orders from customers.
User Authentication: Secure login system for restaurant staff members.
Customer Interaction: Provide contact information and facilitate communication with customers.
API Endpoints: Expose RESTful API endpoints for integrating with other systems.
Installation

Clone the repository:
git clone https://github.com/daveyhmariam/Restaurant_Management.git

Install dependencies:Set up the database:

flask db init
flask db migrate
flask db upgrade
cd restaurant-management
pip install -r requirements.txt

Run the application:

flask run

Access the application in your web browser at http://dawityilma.tech

Usage
Navigate through the different sections of the application using the provided navigation menu.
Log in with your credentials to access restricted areas for inventory management and order processing.
Add, update, or delete items from the inventory and menu as needed.
Process orders received from customers and manage their status.
Contributing
Contributions are welcome! If you have any suggestions, feature requests, or bug reports, please open an issue or submit a pull request.


# Requirements
Flask==2.0.1
SQLAlchemy==1.4.23
Flask-SQLAlchemy==2.5.1
mysql-connector-python==8.0.28
WTForms==2.3.3
Flask-Login==0.5.0
Flask-WTF==0.15.1
gunicorn==20.1.0

