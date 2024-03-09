from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from flask_bootstrap import Bootstrap5
from forms import CreateCafeForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'


# Connect to Database
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)
Bootstrap5(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=True)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


def to_bool(input_string):
    if input_string == "True":
        return True
    else:
        return False


@app.route("/")
def home():
    result = db.session.execute(db.select(Cafe))
    cafes = result.scalars().all()

    # .where(User.id == Address.user_id).order_by(Address.id).scalars().all()


    return render_template("index.html", all_cafes=cafes)


@app.route("/new-cafe", methods=["GET", "POST"])
def add_new_cafe():
    form = CreateCafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name = form.name.data,
            map_url = form.map_url.data,
            img_url = form.img_url.data,
            location = form.location.data,
            has_sockets = to_bool(form.has_sockets.data),
            has_toilet = to_bool(form.has_toilet.data),
            has_wifi = to_bool(form.has_wifi.data),
            can_take_calls = to_bool(form.can_take_calls.data),
            seats = form.seats.data,
            coffee_price = form.coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add-cafe.html", form=form)


@app.route("/edit-cafe/<int:cafe_id>", methods=["GET", "POST"])
def edit_cafe(cafe_id):
    cafe = db.get_or_404(Cafe, cafe_id)
    edit_form = CreateCafeForm(
        name=cafe.name,
        map_url=cafe.map_url,
        img_url=cafe.img_url,
        location=cafe.location,
        has_sockets=cafe.has_sockets,
        has_toilet=cafe.has_toilet,
        has_wifi=cafe.has_wifi,
        can_take_calls=cafe.can_take_calls,
        seats=cafe.seats,
        coffee_price=cafe.coffee_price
    )
    if edit_form.validate_on_submit():
        cafe.name = edit_form.name.data
        cafe.map_url = edit_form.map_url.data
        cafe.img_url = edit_form.img_url.data
        cafe.location = edit_form.location.data
        cafe.has_sockets = to_bool(edit_form.has_sockets.data)
        cafe.has_toilet = to_bool(edit_form.has_toilet.data)
        cafe.has_wifi = to_bool(edit_form.has_wifi.data)
        cafe.can_take_calls = to_bool(edit_form.can_take_calls.data)
        cafe.seats = edit_form.seats.data
        cafe.coffee_price = edit_form.coffee_price.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add-cafe.html", form=edit_form)


@app.route("/delete/<int:cafe_id>")
def delete_cafe(cafe_id):
    cafe_to_delete = db.get_or_404(Cafe, cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
