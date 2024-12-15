"""Додати поля (created_at, updated_at, deleted_at) до таблиць, створених під час виконання
домашньої роботи попереднього уроку, створити файл міграції, провести міграцію за допомогою
flask-migrate."""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func, and_,DateTime
from sqlalchemy.orm import sessionmaker, relationship, selectinload, DeclarativeBase

def print_name_user_check_number(user,card):
    print(f"Клиент: {user.name}")
    print(f"Номер чека: {card.id}")


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__: str = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    carts = relationship("Cart", back_populates="user")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    # softly delete
    deleted_at = Column(DateTime, default=None, nullable=True)



class Product(Base):
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

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = (String)
    description = (String)

    products = relationship("Product", back_populates="category")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    # softly delete
    deleted_at = Column(DateTime, default=None, nullable=True)

class Cart(Base):
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

class ProductCart(Base):
    __tablename__ = "products_carts"
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), primary_key=True)
    quantity = Column(Integer,default=1)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    # softly delete
    deleted_at = Column(DateTime, default=None, nullable=True)


engine = create_engine("sqlite:///:memory:", echo=True)
engine.echo = False
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

user1 = User(name="Вася")
user2 = User(name="Петя")
user3 = User(name="Кошка")
product_1 = Product(name = "Салат", price ="100")
product_2 = Product(name = "Мясо", price ="150")
product_3 = Product(name = "Рыба", price ="200")
cart1,cart2 = Cart(user = user1, products=[product_1,product_2,product_3]), Cart(user = user1, products=[product_1,product_2,product_3])
cart3 = Cart(user = user2,products=[product_1,product_2,product_3])


session.add_all([user1,user2,user3, product_1, product_2, product_3,cart1,cart2,cart3])
session.commit()

engine.echo = True

query = session.query(User, Cart, Product, func.count(Product.id).label('quantity')) \
            .select_from(User) \
            .join(Cart).join(ProductCart, ProductCart.product_id == Product.id) \
            .filter(ProductCart.cart_id == Cart.id) \
            .group_by(Cart.id, Product.name, Product.price)\
            .order_by(Cart.id)\
            .options(selectinload(Cart.products))

result = query.all()

current_id_cart = result[0][1].id
first_for = True
total_price = 0
for user, cart, product, quantity in result:
    if first_for:
        print("\n––––––––––------------------")
        print_name_user_check_number(user,cart)
        first_for=False
    if current_id_cart != cart.id:
        current_id_cart = cart.id
        print(f"                         \nСумма: {total_price}")
        total_price = 0
        print("\n––––––––––------------------")
        print_name_user_check_number(user,cart)
    else:
        print(f"  Блюдо: {product.name} (Цена: {product.price}, Количество: {quantity})")
        total_price+=product.price
print(f"                         \nСумма: {total_price}")
"""users = session.query(User).options(selectinload(User.carts)).all()
print("–––––Имена клиентов и имена заказов (включая что заказали)–––––")
if len(users) == 0:
    print("Клиентов нету", end="")
else:
    for user in users:
        print("Клиент: " + user.name, end=":\n")
        if len(user.carts) == 0:
            print("    Заказов нету", end="")
        else:
            for cart in user.carts:
                print("    Номер заказа: " + str(cart.id), end=",\n")
                if len(cart.products) == 0:
                    print("        Заказ пуст", end="")
                else:
                    for product in cart.products:
                        quantity = product.carts[0]
                        print("        Блюдо: " + product[1])
        print("\n––––––––––------------------")"""
print("–––––Конец–––––")




