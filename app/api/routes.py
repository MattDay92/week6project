from flask import render_template, request, redirect, url_for, flash, Blueprint
from ..forms import UserCreationForm, loginform, ItemSubmitForm
from ..models import User, Item, Cart
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth


api = Blueprint('api', __name__)

@api.route('/api/shop', methods=["GET", "POST"])
def shopPageAPI():

    items = Item.query.all()

    new_items = []
    for i in items:
        new_items.append(i.to_dict())
    
    return {
        'status': 'ok',
        'totalResults': len(items),
        'items': [i.to_dict() for i in items]
    }

@api.route('/api/shop/<int:item_id>', methods=["GET"])
def singleItem(item_id):

    item = Item.query.get(item_id)

    return item.to_dict()





basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()



@basic_auth.verify_password
def verifyPassword(username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        if user.password == password:
            return user

@token_auth.verify_token
def verifyToken(token):
    user = User.query.filter_by(apitoken=token).first()
    if user:
        return user




@api.route('/api/signup', methods=["POST"])
def signUpAPI():
    data = request.json

    username = data['username']
    email = data['email']
    password = data['password']

    user = User(username, email, password)

    user.saveToDB()

    return {
        'status': 'ok',
        'message': 'User successfully created!'
    }


@api.route('/api/login', methods=["POST"])
@basic_auth.login_required
# Login Function
def getToken():
    user = basic_auth.current_user()
    if user:
        print(user)
        return {
            'status': 'ok',
            'user': user.to_dict()
        }
    else:
        return {
            'status': 'not ok'
        }

@api.route('/api/addtocart/<int:item_id>', methods=["GET", "POST"])
@login_required
def addToCart(item_id):
    
    transaction = Cart(item_id, current_user.id)
    transaction.saveToDB()

    return {
        'status': 'ok',
        'message': 'Item successfully added to cart.'
    } 

@api.route('/api/mycart', methods=["GET", "POST"])
@login_required
def myCart():

    my_cart = Cart.query.filter_by(customer_id = current_user.id).all()

    total = 0
    for item in my_cart:
        total += float(item.info.price)

    return {
        'status': 'ok',
        'my_cart': my_cart,
        'total': total
    }

@api.route('/api/cart/<int:item_id>/delete', methods=["GET", "POST"])
@login_required
def deleteItem(item_id):
    item = Cart.query.get(item_id)

    item.deleteFromDB()

    return {
        'status': 'ok',
        'message': 'Item successfully deleted from cart'
    }

@api.route('/api/cart/deleteall', methods=["GET", "POST"])
@login_required
def deleteAll():

    cart = Cart.query.all()
    for item in cart:
        item.deleteFromDB()

    return {
        'status': 'ok',
        'message': 'Successfully deleted all items from cart.'
    }