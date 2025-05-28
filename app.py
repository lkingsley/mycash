from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy 
from model.income import Income
from model.spend import Spend

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

@app.route("/")
def incomes():
    transaction1 = Income(200, "cash", "2025-05-28")
    transaction2 = Income(200, "cash", "2025-05-28")
    return render_template("index.html", transactions=[transaction1,transaction2])

@app.route("/", methods=["POST"])
def transactions():
    type = request.form["type"]
    amount = request.form["amount"]
    method = request.form["method"]
    date = request.form["date"]
    if type == "income":
        transaction = Income(amount, method, date)
    else:
        transaction = Spend(amount, method, date)
    print(transaction)
    return str(transaction)