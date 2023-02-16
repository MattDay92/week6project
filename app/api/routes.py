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
    print(user, 'verify')
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

@api.route('/api/cart/add', methods=["POST"])
@token_auth.login_required
def addToCart():
    data = request.json
    
    item_id = data['itemId']
    item = Item.query.get(item_id)
    user = token_auth.current_user()
    
    transaction = Cart(item_id, user.id)
    transaction.saveToDB()

    return {
        'status': 'ok',
        'message': f'Item successfully added {item.name} to cart.',
        
    } 

@api.route('/api/mycart', methods=["GET"])
@token_auth.login_required
def myCart():

    user = token_auth.current_user()
    print(user)
    my_cart = [Item.query.get(c.item_id).to_dict() for c in user.cart]

    total = 0
    for item in my_cart:
        total += 1


    return {
        'status': 'ok',
        'my_cart': my_cart,
        'total': total
    }

@api.route('/api/cart/delete', methods=["POST"])
@token_auth.login_required()
def deleteItemAPI():

    user = token_auth.current_user()
    data = request.json
    print(data['itemId'])
    item = Cart.query.filter_by(customer_id = user.id).filter_by(item_id = data['itemId']).first()
    print(item)

    item.deleteFromDB()

    return {
        'status': 'ok',
        'message': 'Item successfully deleted from cart'
    }

@api.route('/api/cart/deleteall', methods=["POST"])
@token_auth.login_required
def deleteAllAPI():

    user = token_auth.current_user()
    items = Cart.query.filter_by(customer_id = user.id).all()
    print(items)
    for item in items:
        item.deleteFromDB()

    return {
        'status': 'ok',
        'message': 'Successfully deleted everything from your cart'
    }