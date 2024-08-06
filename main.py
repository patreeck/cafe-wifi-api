import json
import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean

app = Flask(__name__)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        # Convert the Cafe object to a dictionary using dictionary comprehension
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# Uncomment the following lines to create the database tables
# with app.app_context():
#     db.create_all()

@app.route("/")
def home():
    # Render the homepage
    return render_template("index.html")


@app.route("/random")
def get_random_cafe():
    # Get all cafes from the database
    result = db.session.execute(db.select(Cafe))
    all_cafe = result.scalars().all()
    # Select a random cafe
    random_cafe = random.choice(all_cafe)
    # Return the random cafe as a JSON object
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def get_all_cafe():
    # Get all cafes from the database, sorted by name
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    # Return all cafes as a JSON array
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route("/search")
def get_search_cafe():
    # Get the location query parameter
    query_location = request.args.get("loc")
    # Search for cafes with the specified location
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    all_cafes = result.scalars().all()
    # Return the cafes if found, otherwise return an error message
    if all_cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error={"Not Found , 404": "Sorry, we don't have a cafe at that location."})


# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def post_new_cafe():
    # Create a new cafe object from form data
    new_cafe = Cafe(name=request.form.get("name"),
                    map_url=request.form.get("map_url"),
                    img_url=request.form.get("img_url"),
                    location=request.form.get("loc"),
                    seats=request.form.get("seats"),
                    has_toilet=bool(request.form.get("toilet")),
                    has_wifi=bool(request.form.get("wifi")),
                    has_sockets=bool(request.form.get("sockets")),
                    can_take_calls=bool(request.form.get("calls")),
                    coffee_price=request.form.get("coffee_price"))
    # Add the new cafe to the database and commit the transaction
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:id>", methods=["PATCH"])
def update_price(id):
    # Get the new price from the query parameters
    new_price = request.args.get('new_price')
    # Find the cafe by ID or return 404 if not found
    update_cafe = db.get_or_404(Cafe, id)
    if update_cafe:
        # Update the coffee price and commit the transaction
        update_cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"Success": "Price updated successfully"}), 200
    else:
        return jsonify(response={"Failure": "Cafe not found for this ID"}), 404


# HTTP DELETE - Delete Record
@app.route("/delete-cafe/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    # Get the secret key from the query parameters
    secret_key = request.args.get('secret_key')
    # Find the cafe by ID or return 404 if not found
    delete_cafe = db.get_or_404(Cafe, cafe_id)
    if secret_key == "mysecretkey":
        # Delete the cafe from the database and commit the transaction
        db.session.delete(delete_cafe)
        db.session.commit()
        return jsonify(response={"Success": "Cafe deleted successfully"}), 200
    else:
        return jsonify(response={"Failure": "Wrong secret key!"}), 404


if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
