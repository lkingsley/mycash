from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import desc, select, exc
from model.base import Base
from model.transaction import Transaction
import datetime

INCOME = "income"
SPEND = "spend"
DATABASE_URI = "sqlite:///test.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
db = SQLAlchemy(model_class=Base)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def list_transactions():
    #TODO: check this: request.args.get("")
    total_income = 0
    total_spend = 0
    transactions = []
    actual_year = datetime.datetime.now().year
    years = [actual_year]
    query_result = db.session.execute(select(Transaction)
        .order_by(desc(Transaction.date))).scalars()
    #TODO: find alternative
    for i in range(9):
        actual_year -= 1
        years.append(actual_year)

    for i in query_result:
        transactions.append(i)
        if i.type == INCOME:
            total_income += i.amount
        else:
            total_spend += i.amount

    return render_template(
        "index.html", transactions=transactions, total_income=round(total_income, 2),
        total_spend=round(total_spend, 2), years=years
    )

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

@app.route("/create", methods=["GET", "POST"])
def create_transaction():
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
        transaction = Transaction(
            amount=amount, method=method, date=date,
            type=transaction_type, description=description
        )
        try:
            db.session.add(transaction)
            db.session.commit()
        except Exception:
            #TODO: Send error message
            print("HANDLE ERROR: *********")
            pass

    return redirect("/")

@app.route("/<int:id>/edit", methods=["GET", "POST"])
def edit_transaction(id):
    try:
        transaction = db.session.execute(select(Transaction)
            .filter_by(id=id)).scalar_one()
        
        if request.method == "GET":
            return render_template("transactions/edit.html", g=transaction)
        else:
            transaction.amount = request.form["amount"]
            transaction.date = request.form["date"]
            transaction.type = request.form["type"]
            transaction.method = request.form["method"]
            transaction.description = request.form["description"]
            db.session.commit()
            return redirect("/")
    except exc.NoResultFound:
        #TODO:implement something here
        return f"transaction {id} not found"
        
@app.route("/<int:id>/delete", methods=["GET", "POST"])
def delete_transaction(id):
    if request.method == "GET":
        return f"<p>Proceed deleting transaction {id}?</p> \
        <form method=\"post\"> \
        <button formaction=\"/{id}/delete\" type=\"submit\">Yes</button> \
        <button formaction=\"/\" formmethod=\"get\" type=\"submit\">No</button> \
        </div> \
        </form>"
    elif request.method == "POST":
        transaction = db.get_or_404(Transaction, id)
        db.session.delete(transaction)
        db.session.commit()
        return redirect("/")