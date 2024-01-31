#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict(rules=("-baked_goods",)) for bakery in Bakery.query.all()]

    return make_response(bakeries, 200)
# GET /bakeries: returns a list of JSON objects for all bakeries in the database.



@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    return make_response(bakery.to_dict(), 200)
# GET /bakeries/<int:id>: returns a single bakery as JSON with its baked goods nested in a list. 
# Use the id from the URL to look up the correct bakery.

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [baked_good.to_dict() for baked_good in baked_goods_by_price]
    return make_response(baked_goods_by_price_serialized, 200)
# GET /baked_goods/by_price: returns a list of baked goods as JSON, 
# sorted by price in descending order. (HINT: how can you use SQLAlchemy to sort the baked goods in descending order?)


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_BG = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return make_response(most_expensive_BG.to_dict(), 200)

# GET /baked_goods/most_expensive: returns the single most expensive baked good as JSON. (HINT: how can you use
#  SQLAlchemy to sort the baked goods in descending order and limit the number of results?)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
