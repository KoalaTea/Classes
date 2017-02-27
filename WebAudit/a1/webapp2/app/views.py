from flask import render_template, flash, redirect, request, url_for
from app import app, lm
from .forms import LoginForm
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from .objects import User
from .decorators import bartender_required, admin_required
from .db import db
import json
import time

CURRENT_STAT_FILE = 1
CUSTOM_COST=150

# TODO:
#   set all pages to check for authentication and if none - guest@Hackerbar
#   metrics
#   times
#   logging

# index
#   the main page
#
# returns
#   template of main page
@app.route("/")
@app.route("/index")
def index():
    drinks = [
        {
            'drink_name' : 'Godfather',
            'ingredients' : [ 'half ameretto', 'half scotch whiskey' ]
        },
        {
            'drink_name' : 'temp test',
            'ingredients' : [ 'nothing', 'more nothing' ]
        }
    ]
    return render_template('index.html', title='Home', user=current_user, drinks=drinks)

# login
#   login page
#
# data
#   username    - the username
#   password    - the password
#
# returns
#   login stuff if successful and redirect to index or flashed failed message if unsuccessful
@app.route("/login", methods=["POST", "GET"])
@app.route("/signin", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if(request.method == "POST" and form.validate_on_submit()):
        user = db.Users.find_one({"username": form.username.data})
        if(user is not None and User.validate_login(user['password'], form.password.data)):
            user_obj = User(user)
            login_user(user_obj)
        else:
            pass
            #TODO
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

# logout
#   logour page destroys session
#
# data
#   login information
#
# returns
#   cleared session and redirect to index
@app.route("/logout")
@app.route("/signout")
def logout():
    logout_user()
    return redirect('/index')

# list_alchohol
#   lists all available alchohols
#
# returns
#   alchohol template which has all alchohols available
@app.route("/list_alchohol", methods=["GET", "POST"])
def list_alchohol():
    return render_template('alchohol.html', title='Alchohol', user=current_user, alchohol_list=db.Alchohol.find())

# add_alchohol
#   will add bottles to an alchohol that exists, or add the alchohol to the list if it does not exist
#
# data
#   alchohol    {
#               type    - alchohol type
#               name    - brand name
#               flavor  - flavor of alchohol (None if just the alchohol)
#               bottles - number of bottles being added
#               }
#
# Returns
#   the new alchohol database entry or empty set if failed
@app.route("/add_alchohol", methods=["POST"])
@bartender_required
def add_alchohol():
    data = request.get_json()
    if set(data.keys()) == set(["type","name","flavor","bottles"]):
        current_alchohol = db.Alchohol.find({"type": data["type"], "name": data["name"], "flavor":data["flavor"]})
        if(current_alchohol is None):
            db.Alchohol.insert_one(data)
        #TODO update to set bottles += bottles added
        new_alchohol = db.Alchohol.find(data)
        return new_alchohol
    return "{}"

# remove_alchohol
#   will add bottles to an alchohol that exists, or add the alchohol to the list if it does not exist
#
# data
#   alchohol    {
#               type    - alchohol type
#               name    - brand name
#               flavor  - flavor of alchohol (None if just the alchohol)
#               bottles - number of bottles being removed
#               }
#
# Returns
#   the new alchohol database entry or empty set if failed
@app.route("/remove_alchohol", methods=["POST"])
@bartender_required
def remove_alchohol():
    data = request.get_json()
    if(set(data.keys()) == set(["type","name","flavor","bottles"])):
        print("works")
        current_alchohol = db.Alchohol.find({"type": data["type"], "name": data["name"], "flavor":data["flavor"]})
        if(current_alchohol is None or current_alchohol["bottles"] == 0 or current_alchohol["bottles"] < data["bottles"]):
            # raise issue
            return "{}"
        #TODO update to set bottles -= bottles added
        db.Alchohol.delete_one(current_alchohol)
        current_alchohol["bottles"] -= data["bottles"]
        db.Alchohol.insert_one(current_alchohol)
        new_alchohol = db.Alchohol.find(data)
        return new_alchohol
    return "{}"

# list_drinks
#   lists all drink recipes in the database
#
# returns
#   drinks template with all recorded drinks
@app.route("/list_drinks", methods=["GET", "POST"])
@app.route("/recipes", methods=["GET", "POST"])
def list_drinks():
    return render_template('recipes.html', title='All Drinks', user=current_user, drinks=db.Drinks.find())

@app.route("/bartender", methods=["GET"])
@bartender_required
@login_required
def bartender():
    Orders = db.Orders.find()
    Drinks = db.Drinks.find({"available" : True})
    return render_template('bartender.html', title='Bartender', user=current_user, orders=Orders, drinks=Drinks)

@login_required
@bartender_required
@app.route("/update_order", methods=["POST"])
#TODO delete order and move it to PastOrders on completion
def update_order():
    postData = dict(request.form)
    Orderup = ObjectId(postData['id'][0])
    Status = postData['status'][0]

    if Status == 'queued':
        print (Orderup)
        n = db.Orders.update_one(
            { "_id": Orderup },
            { '$set': { "status": "inprogress" } }
        )
    elif Status == 'InProgress':
        db.Orders.update_one({"_id": Orderup},
            {
                '$set': {
                    'status': "ready"
                }
            })
    elif Status.lower() == 'ready':
        db.Orders.update_one({"_id": Orderup},
            {
                '$set': {
                    'status': "complete"
                }
         })

    return redirect(url_for('bartender'))

# menu
#   lists all available drinks based on alchohol currently in stock
#
# returns
#   menu template with only available drinks

@app.route("/menu", methods=["GET"])
@login_required
def menu():
    return render_template('menu.html', title='Menu',
                           user=current_user,
                           credits=get_user_credits(current_user.username),
                           drinks=db.Drinks.find({"available": True}))

@app.route("/update_menu", methods=["POST"])
@login_required
@bartender_required
def update_menu():
    data = request.get_json()
    if(set(data.keys()) == set(["type","flavor"])):
        print("works")
        have_more = False
        alchohols = db.Alchohol.find({"type": data["type"], "flavor": data["flavor"]})
        if(alchohols is not None):
            for alchohol in alchohols:
                if(alchohol["bottles"] > 0):
                    have_more = True
            if(have_more):
                #TODO decide on format
                return '{"okay":"cool"}'
            else:
                drinks = db.Drinks.find({"available": True})
                for drink in drinks:
                    for ingredient in drink["recipe"]:
                        if(ingredient["type"] == data["type"] and ingredient["flavor"] == data["flavor"]):
                            #TODO update the drinks availability to false
                            #TODO maybe complete?
                            db.Drinks.delete_one(drink)
                            drink["available"] = False
                            db.Drinks.insert_one(drink)
                            return '{"New": "Menu"}'
    return "{}"


# order_drink
#   page to order drinks from
#
# data
#   drink   {
#           name    - name of drink
#           type    - type of drink (shot/mixed/on the rocks)
#           recipe  {
#                   type    - type of alchohol
#                   ammount - ammount to use
#                   }
#           }
#   user    - the user logged in
#
# returns
#   ... TODO think about money and other stuff for fails
"""
@app.route("/order_drink", methods=["POST"])
@login_required
def order_drink():
    #TODO money things
    print(current_user.username)
    data = request.json
    print(data)
    if(set(data.keys()) == set(["name"])):
        the_drink = db.Drinks.find_one(data)
        print(the_drink)
        if(the_drink is not None):
            db.Orders.insert_one({"drink": {"name": the_drink["name"], "type": the_drink["type"], "recipe": the_drink["recipe"]}, "user": current_user.username})
            output = ''
            for i in db.Orders.find({"user": current_user.username}):
                output += str(i)
            return output
    return "{}"
"""
# orders
#   view all orders, must be bartender or admin
#
# returns
#   orders template with all current orders listed
#
# TODO verify correct ordering
@app.route("/orders", methods=["GET"])
@login_required
@bartender_required
def orders():
    orders = db.Orders.find()
    return render_template('orders.html', title='Orders', user=current_user, orders=orders)

@app.route("/my_orders", methods=["GET"])
@login_required
def my_orders():
    orders = db.Orders.find({"user": current_user.username})
    return render_template('my_orders.html', title='My Orders', user=current_user, orders=orders)

@app.route("/current_orders", methods=["GET"])
@login_required
@bartender_required
def current_orders():
    orders = db.Orders.find()
    return render_template('current_orders.html', title='Orders', user=current_user, orders=orders)

@app.route("/my_current_orders", methods=["GET"])
@login_required
def my_current_orders():
    orders = db.Orders.find({"user": current_user.username})
    return render_template('my_current_orders.html', title='Orders', user=current_user, orders=orders)

@app.route("/recent_orders")
@login_required
def recent_orders():
    orders = db.Orders.find({"user": current_user.username})
    return render_template('recent_orders.html',
                           title='Orders',
                           user=current_user,
                           orders=orders,
                           totaldrinks=get_user_drinks(current_user.username),
                           credits=get_user_credits(current_user.username))

@app.route('/review_order/<drinkname>')
@login_required
def review_order(drinkname):
    drink = db.Drinks.find_one({"name": drinkname})
    if drink is not None:
        return render_template('review_order.html', title='Review and Order', user=current_user, drink=drink)
    else:
        return redirect(url_for('menu'))

@app.route('/order_drink', methods=["POST"])
@login_required
def order_drink():
    print("Order Drinks")
    postData = dict(request.form)
    print(postData)
    drink = db.Drinks.find_one({"name": postData['drink'][0]})
    print (drink['recipe'])
    if drink is not None:
        if get_user_credits(current_user.username) < drink['cost']:
            return '{"status": "failed - not enough credits"}'
        print("drink ordered since enough credits")
        db.Users.update_one({'username': current_user.username},
                            {
                            '$inc': {
                                    'credits': -drink['cost'],
                                    'drinksOrdered': 1
                                }
                            })
        print("credits edited")
        db.Orders.insert_one(
             {
                 "name": drink['name'],
                 "cost": drink['cost'],
                 "type": drink['type'],
                 "recipe": drink['recipe'],
                 "image": drink['image'],
                 "timeOrdered": int(time.time()),
                 "user": current_user.username,
                 "instructions": postData['instructions'][0],
                 "status": "queued"
             }
        )
        print("trying statistics")
        stats = db.Statistics.find_one({"id": CURRENT_STAT_FILE})
        #breaks here
        print("queried " + stats)
        if (int(time.time()) - stats['time']) >= 3600:
            #An hour or more has passed
            CURRENT_STAT_FILE = CURRENT_STAT_FILE + 1
            statistics.insert_one(
                {
                    "id": CURRENT_STAT_FILE,
                    "time": int(time.time()*1000) ,
                    "total_orders": 1,
                    "drink_orders": [
                        {"name": drink['name'], "Orders": 1},
                    ]
                })
        else:
            stat_exists = db.Statistics.find_one({"name" : drink['name']})
            if stat_exists:
                db.Users.update_one({'id': CURRENT_STAT_FILE},
                                    {
                                    '$inc': {
                                            'total_orders': 1
                                        }
                                    })

            db.Users.update_one({'id': CURRENT_STAT_FILE},
                                {
                                '$inc': {
                                        'total_orders': 1
                                    },
                                '$addToSet': {
                                        'name' : drink['name'], 'Orders': 1
                                    }

                                })

        return '{"status": "okay"}'
    else:
        return '{"status": "failed - no such drink"}'

@app.route('/cancel_drink', methods=["POST"])
@login_required
def cancel_drink():
    postData = dict(request.form)
    orderid = ObjectId(postData['order'][0])
    order = db.Orders.find_one({"_id": orderid})
    if order is not None:
        if order['status'].lower() == "queued":
            db.Orders.delete_one({"_id": orderid, "user": current_user.username})
            db.Users.update_one({'username': current_user.username},
                    {
                    '$inc': {
                            'credits': order['cost'],
                            'drinksOrdered': -1
                        }
                    })

            return '{"status": "okay"}'
        return '{"status": "cannot cancel progressed order"}'
    else:
        return '{"status": "failed - no such order"}'

@app.route('/custom_drink')
@login_required
def custom_drink():
    ingredients = db.Ingredients.find({"available": True})
    return render_template('custom_drink.html', ingredients=ingredients)

@app.route('/order_custom_drink', methods=["POST"])
@login_required
def order_custom_drink():
    recipe = []
    postData = dict(request.form)
    print(postData['recipe[]'])
    if get_user_credits(current_user.username) < CUSTOM_COST:
        print ("Can't afford drink")
        return '{"status": "failed - not enough credits"}'

    for ing in postData['recipe[]']:
        print(ing)

        ingredient = {}
        ingredient['type'] = ing
        ingredient['flavor'] = ''
        ingredient['amount'] = ""
        recipe.append(ingredient)

    db.Users.update_one({'username': current_user.username},
                        {
                        '$inc': {
                                'credits': -CUSTOM_COST,
                                'drinksOrdered': 1
                            }
                        })
    db.Orders.insert_one(
         {
             "name": "Custom Drink",
             "cost": CUSTOM_COST,
             "type": "custom",
             "recipe": recipe,
             "image": 'custom_drink.png',
             "timeOrdered": int(time.time()),
             "user": current_user.username,
             "instructions": postData['instructions'][0],
             "status": "queued"
         }
    )
    return '{"status": "okay"}'


@app.route("/order_complete", methods=["POST"])
@login_required
@bartender_required
def order_complete():
    print(current_user.username)
    data = request.json
    print(data)
    if(set(data.keys()) == set(["_id"])):
        print("we here")
        the_order = db.Orders.find_one({"_id": ObjectId(data["_id"])})
        db.PastOrders.insert_one(the_order)
        print(the_order)
        if(the_order is not None):
            db.Orders.delete_one({"_id": ObjectId(data["_id"])})
    orders = db.Orders.find()
    return render_template('current_orders.html', title='Orders', user=current_user, orders=orders)

# admin
#   admin panel
#
# returns
#   admin panel template
@app.route("/admin", methods=["GET"])
@admin_required
def admin_panel():
    pass


# load_user
#   sets things up for loading a user since we use mongo instead of sqllite
#
# returns
#   User object of the user from the database
@lm.user_loader
def load_user(username):
    u = db.Users.find_one({"username": username})
    if not u:
        return None
    return User(u)

def get_user_credits(username):
    usr = db.Users.find_one({'username': username})
    return usr['credits']
def get_user_drinks(username):
    usr = db.Users.find_one({'username': username})
    return usr['drinksOrdered']
