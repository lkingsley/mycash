from flask import Flask, redirect, request, render_template
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import desc, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

INCOME = "income"
SPEND = "spend"

app = Flask(__name__)
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db.init_app(app)

class Transact(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int] = mapped_column(nullable=False)
    method: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def incomes():
    #TODO: check this: request.args.get("")
    total_income = 0
    total_spend = 0
    transactions = []
    query_result = db.session.execute(select(Transact).order_by(desc(Transact.date))).scalars()
    
    for i in query_result:
        transactions.append(i)
        if i.type == INCOME:
            total_income += i.amount
        else:
            total_spend += i.amount
    return render_template("index.html", transactions=transactions, total_income=total_income, total_spend=total_spend)

@app.route("/transactions", methods=["POST"])
def transactions():
    transaction_type = request.form["type"]
    amount = request.form["amount"]
    method = request.form["method"]
    date = request.form["date"]
    
    #TODO:validate fields
    transaction = Transact(amount=amount,method=method,date=date, type=transaction_type)
    try:
        db.session.add(transaction)
        db.session.commit()
    except Exception:
        #TODO: Send error message
        pass

    return redirect("/")