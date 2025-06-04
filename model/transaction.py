from sqlalchemy.orm import Mapped, mapped_column
from model.base import Base

class Transaction(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int] = mapped_column(nullable=False)
    method: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

    def __str__(self):
        return f"<Transaction id={self.id}, type={self.type}, amount={self.amount}> \
            method={self.method}, date={self.date}, description={self.description}"