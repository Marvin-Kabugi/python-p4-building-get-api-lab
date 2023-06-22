#!/usr/bin/env python3

from flask import Flask, make_response, jsonify,request
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

@app.route('/bakeries/<int:id>', methods = ['GET', 'PATCH'])
def bakery_by_id(id):
    if request.method == "GET":
        bakery = Bakery.query.filter_by(id = id).first()
        print(bakery)
        bakery_obj = bakery.to_dict()

        response = make_response(jsonify(bakery_obj), 200)
        response.headers["Content-Type"] = 'application/json'

        return response
    
    elif request.method == "PATCH":
        bakery = Bakery.query.filter_by(id=id).first()

        if bakery:
            for args in request.form:
                setattr(bakery, args, request.form.get(args))

            db.session.add(bakery)
            db.session.commit()
            
            bakery_dict = bakery.to_dict()
            response = make_response(jsonify(bakery_dict), 200)
            response.headers["Content-Type"] = 'application/json'

            return response

@app.route('/baked_goods', methods = ['POST'])
def baked_goods():
    if request.method == 'POST':
        baked_good = BakedGood(
            name = request.form.get("name"),
            price = request.form.get("price"),
            bakery_id = request.form.get("bakery_id"),
        )

        db.session.add(baked_good)
        db.session.commit()

        baked_good_dict = baked_good.to_dict()

        response = make_response(jsonify(baked_good_dict), 201)
        response.headers["Content-Type"] = 'application/json'

        return response
    
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_goods(id):
    if request.method == 'DELETE':
        baked_good = BakedGood.query.filter_by(id=id).first()
        
        if baked_good:
            db.session.delete(baked_good)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message": "Baked Good Deleted"
            }

            response = make_response(jsonify(response_body), 200)
            response.headers["Contente-Type"] = 'application/json'

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
