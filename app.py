from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import desc, select
from model.base import Base
from model.transaction import Transaction
import datetime

INCOME = "income"
SPEND = "spend"
DATABASE_URI = "sqlite:///test.db"

class Month:
    def __init__(self, name, id):
        self.id = id
        self.name = name
months = []
months.append(Month(name="january",id=1))
months.append(Month(name="february",id=2))
months.append(Month(name="march",id=3))
months.append(Month(name="april",id=4))
months.append(Month(name="may",id=5))
months.append(Month(name="june",id=6))
months.append(Month(name="july",id=7))
months.append(Month(name="august",id=8))
months.append(Month(name="septmeber",id=9))
months.append(Month(name="october",id=10))
months.append(Month(name="november",id=11))
months.append(Month(name="december",id=12))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
db = SQLAlchemy(model_class=Base)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def get_transactions():
    #TODO: check this: request.args.get("")
    total_income = 0
    total_spend = 0
    transactions = []
    actual_year = datetime.datetime.now().year
    years = [actual_year]
    query_result = db.session.execute(select(Transaction).order_by(desc(Transaction.date))).scalars()
    
    for i in range(9):
        actual_year -= 1
        years.append(actual_year)

    for i in query_result:
        transactions.append(i)
        if i.type == INCOME:
            total_income += i.amount
        else:
            total_spend += i.amount

    return render_template("index.html", transactions=transactions, total_income=total_income, total_spend=total_spend, months=months, years=years)

@app.route("/login", methods=["GET", "POST"])
def login():
    #TODO: Implement this
    if request.method == "POST":
        username = request.form["username"]
        passwd = request.form["passwd"]
        print(username, passwd)
        return f"{username} | {passwd}"
    else:
        return render_template("auth/login.html")

@app.route("/create", methods=["GET","POST"])
def post_transaction():
    if request.method == "GET":
        return render_template("transactions/create.html")
    else:
        transaction_type = request.form["type"]
        amount = request.form["amount"]
        method = request.form["method"]
        date = request.form["date"]
        description = request.form["description"]
    
        print(description)
        #TODO:validate fields
        transaction = Transaction(amount=amount,method=method,date=date, type=transaction_type, description=description)
        try:
            db.session.add(transaction)
            db.session.commit()
        except Exception:
            #TODO: Send error message
            print("HANDLE ERROR: *********")
            pass

    return redirect("/")