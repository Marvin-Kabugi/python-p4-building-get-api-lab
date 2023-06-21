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
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]

    response = make_response(jsonify(bakeries), 200)
    response.headers["Content-Type"] = 'application/json' 

    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id = id).first()
    print(bakery)
    bakery_obj = bakery.to_dict()

    response = make_response(jsonify(bakery_obj), 200)
    response.headers["Content-Type"] = 'application/json'

    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    goods = [baked_good.to_dict() for baked_good in BakedGood.query.order_by(db.desc(BakedGood.price))]

    response = make_response(jsonify(goods), 200)
    response.headers["Content-Type"] = 'application/json'

    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(db.desc(BakedGood.price)).limit(1).first()
    most_expensive_obj = most_expensive.to_dict()

    response = make_response(jsonify(most_expensive_obj), 200)
    response.headers["Content-Type"] = 'application/json'

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
