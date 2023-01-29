from app import app
from flask import render_template, request, redirect, url_for, flash
from .forms import UserCreationForm, loginform, ItemSubmitForm
from .models import User, Item, Cart
from flask_login import login_user, logout_user, current_user


@app.route('/signup', methods=["GET", "POST"])
def signUpPage():
    form = UserCreationForm()
    print(request.method)
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            
            print(username, email, password)

            # add user to database
            user = User(username, email, password)
            # print(user)

            user.saveToDB()

            return redirect(url_for('homePage'))


    return render_template('signup.html', form = form )

@app.route('/login', methods=['GET', 'POST'])
def loginPage():
    form = loginform()
    if request.method == 'POST':
        if form.validate():
            username= form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()
            if user:

                if user.password == password:
                    login_user(user)
                    flash("Successfully logged in", category="success")
                    
                else:
                    flash("Wrong password", category="danger")
            else:
                flash("This user does not exist.", category="danger")

        return redirect(url_for('shopPage'))
        
    return render_template('login.html', form=form)
        


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash("Successfully logged out!", category="success")
    return redirect(url_for('loginPage'))


@app.route('/', methods=["GET", "POST"])
def shopPage():

    items = Item.query.all()

    return render_template('shop.html', items=items)

@app.route('/addtocart/<int:item_id>', methods=["GET", "POST"])
def addToCart(item_id):
    
    transaction = Cart(item_id, current_user.id)
    transaction.saveToDB()
    flash('Item successfully added to your cart!', category='success')

    return redirect(url_for('shopPage'))

@app.route('/mycart', methods=["GET", "POST"])
def myCart():

    my_cart = Cart.query.filter_by(customer_id = current_user.id).all()

    total = 0
    for item in my_cart:
        total += float(item.info.price)

    print(total)

    return render_template('cart.html', my_cart=my_cart, total=total)

@app.route('/cart/<int:item_id>/delete', methods=["GET", "POST"])
def deleteItem(item_id):
    item = Cart.query.get(item_id)

    item.deleteFromDB()

    return redirect(url_for('myCart'))

@app.route('/shop/<int:item_id>')
def singleItem(item_id):

    item = Item.query.get(item_id)

    return render_template('singleitem.html', item=item)

@app.route('/admin', methods=['GET', 'POST'])
def adminPage():
    form = ItemSubmitForm()
    print(request.method)
    if request.method == 'POST':
        if form.validate():
            name = form.name.data
            img_url = form.img_url.data
            details = form.details.data
            price = form.price.data

            item = Item(name, img_url, details, price)

            item.saveToDB()
            flash("Item saved to database", category="success")

            return redirect(url_for('adminPage'))

    return render_template('admin.html', form=form)