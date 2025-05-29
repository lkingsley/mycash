from flask import Flask, redirect, request, render_template
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = Flask(__name__)
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db.init_app(app)


class Transact(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[str] = mapped_column(nullable=False)
    method: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(nullable=False)


with app.app_context():
    db.create_all()

@app.route("/")
def incomes():
    transactions = db.session.execute(select(Transact)).scalars()
    return render_template("index.html", transactions=transactions)

@app.route("/", methods=["POST"])
def transactions():
    type = request.form["type"]
    amount = request.form["amount"]
    method = request.form["method"]
    date = request.form["date"]

    transaction = Transact(amount=amount,method=method,date=date)
    db.session.add(transaction)
    db.session.commit()
    return redirect("/")