from flask import render_template, request, redirect, url_for, flash, Blueprint
from ..forms import UserCreationForm, loginform, ItemSubmitForm
from ..models import User, Item, Cart
from flask_login import login_user, logout_user, current_user, login_required

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
