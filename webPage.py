from flask import Flask, render_template, redirect, url_for, request, jsonify
import requests
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from Solver import *
from sqlalchemy.sql import func
import json


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

BASE = "http://127.0.0.1:5000/"

class FunctionModel(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    expres = db.Column(db.String(100), nullable=False)
    solution = db.Column(db.Float, nullable=True)
    iterations = db.Column(db.Integer, nullable=False)
    t = db.Column(db.Float, nullable=False)
    accuracy = db.Column(db.Float, nullable=True)
    solved = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Solve(solution = {solution}, expres{expres}, iterations = {iterations}, t = {t}, accuracy = {accuracy}, solved = {solved}, message = {message})"

db.create_all() #Just one time to not override
resource_fields = {
    'id': fields.Integer,
    'expres': fields.String,
    'solution': fields.Float,
    'iterations': fields.Integer,
    't': fields.Float,
    'accuracy': fields.Float,
    'solved': fields.Integer,
    'message': fields.String
} 

class Solve(Resource):
    #@app.route("/<int:x0>/<string:func>")
    @marshal_with(resource_fields)
    def put(self, x0, func):
        parse(func)
        fObj = Solver11(x0,f)
        function = FunctionModel(expres=func, solution=fObj.sol, iterations=fObj.it, t=fObj.t, accuracy=fObj.acc, solved=fObj.solved, message=fObj.message)
        db.session.add(function)
        db.session.commit()
        return function, 201
class GetResponse(Resource):
    @marshal_with(resource_fields)
    def get(self, func):
        result = FunctionModel.query.filter_by(expres=func).first()
        if not result:
            abort(404, message="No se encontro ninguna funcion con esa id")
        return result
class GetStats(Resource):
    def get(self):
        sol = FunctionModel.query.filter_by(solved=1).count()
        notSol = FunctionModel.query.filter_by(solved=0).count()
        if (not sol or not notSol):
            abort(404, message="No se encontro ninguna funcion con esa id")
        solPer = (sol / (sol + notSol)) * 100
        return {"porcentaje resuelto": str(round(solPer, 2)) + '%'}

#Falta xs
api.add_resource(Solve, "/solve/<float:x0>/<string:func>")
api.add_resource(GetResponse, "/solve/<string:func>")
api.add_resource(GetStats, "/getStats")

'''@app.route("/<name>")
def Home(name):
    return render_template("home.html", content=name)'''

@app.route("/", methods = ["PUT", "GET", "POST"])
def Home():
    if request.method == "POST":
        eq = request.form["eq"]
        x0 = request.form["x0"]
        return redirect(url_for("solving", x0=x0, func=eq))
    else:
        return render_template("home.html")
@app.route("/solve/<float:x0>/<string:func>", methods = ["PUT", "GET", "POST"])
def solving(x0, func):
    response = requests.put(BASE + "solve/" + str(x0) + "/" + func)
    jsonStr = json.dumps(response.json())
    data = json.loads(jsonStr)
    if data["message"] == "No solution found":
        return render_template("res.html", message=data["message"],func=func, resultado="no hay", p=data["accuracy"], id=data["id"], it=data["iterations"], t=data["t"])
    return render_template("res.html", message=data["message"], func=func, resultado=data["solution"], p=data["accuracy"], id=data["id"], it=data["iterations"], t=data["t"])
@app.route("/getStats", methods = ["GET"])
def showStats():
    response = requests.get(BASE + "/getStats")
    return render_template("stats.html", solved=response)
if __name__ == '__main__':
    app.run(debug=True)