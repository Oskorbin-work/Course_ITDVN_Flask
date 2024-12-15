from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import  MetaData, Column, Integer, String, ForeignKey, func,DateTime
from sqlalchemy.orm import  relationship, DeclarativeBase


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


db = SQLAlchemy(model_class=Base)

class User(db.Model):
    __tablename__: str = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    carts = relationship("Cart", back_populates="user")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    # softly delete
    deleted_at = Column(DateTime, default=None, nullable=True)



class Product(db.Model):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    carts = relationship("Cart",secondary ="products_carts", back_populates="products")

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    # softly delete
    deleted_at = Column(DateTime, default=None, nullable=True)

class Category(db.Model):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = (String)
    description = (String)

    products = relationship("Product", back_populates="category")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    # softly delete
    deleted_at = Column(DateTime, default=None, nullable=True)

class Cart(db.Model):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="carts")
    products = relationship("Product",secondary ="products_carts", back_populates="carts")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    # softly delete
    deleted_at = Column(DateTime, default=None, nullable=True)

    @property
    def total_price(self):
        return sum(product.price for product in self.products)

class ProductCart(db.Model):
    __tablename__ = "products_carts"
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), primary_key=True)
    quantity = Column(Integer,default=1)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    # softly delete
    deleted_at = Column(DateTime, default=None, nullable=True)

"""class Expense(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    amount: Mapped[float] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="expenses")

    def __repr__(self):
        return f"Expense(title='{self.title}', amount={self.amount})"


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()

    expenses: Mapped[list["Expense"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"User(username={self.username}"
"""