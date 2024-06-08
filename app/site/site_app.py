from flask import request, url_for, flash, render_template, redirect
from flask import jsonify
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from app.site import site
from models.users import User, Role
from models.menu_items import MenuItem
from models.orders import Order, Status
from models.order_items import OrderItem
from models import storage
from app import bcrypt


class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(
        min=4, max=40)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=7, max=20)], render_kw={"placeholder": "Password"})
    first_name = StringField(validators=[InputRequired(), Length(
        min=4, max=40)], render_kw={"placeholder": "first_name"})
    last_name = StringField(validators=[InputRequired(), Length(
        min=4, max=40)], render_kw={"placeholder": "last_name"})

    submit = SubmitField('Register')

    def validate_email(self, email):
        existing_user_email = storage.query(User, email)
        if existing_user_email:
            return False
        return True


class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(
        min=4, max=40)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=5, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')


@site.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = storage.query(User, form.email.data)
        if (user and bcrypt.check_password_hash(user.password,
                                                password=form.password.data)):

            login_user(user)
            return redirect(url_for('site.home'))

    return render_template('login.html', form=form)


@site.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('site.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = storage.query(User, form.email.data)
        if existing_user:
            flash('Email already exists. \
                    Please use a different email.', 'error')
        else:
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            new_user = User(email=form.email.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=hashed_password,
                            role=Role.CUSTOMER)
            storage.new(new_user)
            storage.save()
            flash('Registration successful. You can now login.', 'success')
            return redirect(url_for('site.login'))
    return render_template('register.html', form=form)


@site.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.login'))


@site.route("/menu", strict_slashes=False)
@login_required
def menu():
    menu_items = storage.all(MenuItem)

    menu = {}
    for item in menu_items.values():
        category = item.category
        if category not in menu:
            menu[category] = []
        menu[category].append(item)

    sorted_menu = {category: sorted(dishes, key=lambda x: x.name)
                   for category, dishes in sorted(menu.items())}

    return render_template("menu.html", menu=sorted_menu)


@site.route("/place_order", methods=["POST"], strict_slashes=False)
@login_required
def place_order():
    data = request.get_json()

    if not data or 'selectedDishes' not in data:
        return jsonify({"message": "No dishes selected"}), 400

    selected_dishes = data['selectedDishes']

    if not selected_dishes:
        return jsonify({"message": "No dishes selected"}), 400

    try:
        order = Order(user_id=current_user.id, status=Status.PENDING)
        storage.new(order)
        storage.save()

        for item in selected_dishes:
            order_item = OrderItem(order_id=order.id, menu_item_id=item)
            storage.new(order_item)

        storage.save()

        return jsonify({"message": "Order placed successfully",
                        "order_id": order.id}), 200

    except Exception as e:
        storage.rollback()
        return jsonify({"message": str(e)}), 500


@site.route("/pending_orders", strict_slashes=False)
@login_required
def pending_orders():
    orders = current_user.orders
    pending = []
    dishes = storage.all(MenuItem).values()
    if orders:
        for order in orders:
            OIT = order.order_items
            for order_item in order.order_items:
                for dish in dishes:
                    if dish.id == order_item.menu_item_id:
                        pending.append(dish.name)
    return jsonify({"pending_orders": pending})

@site.route("/", strict_slashes=False)
@site.route("/index", strict_slashes=False)
def index():
    return render_template("index.html")


@site.route("/home", strict_slashes=False)
@login_required
def home():
    return render_template("home.html")
