Cafe & Wifi API


A Flask-based API for managing a database of cafes. Includes endpoints to retrieve, add, update, and delete cafes. Features an interactive web interface for searching cafes by location. Utilizes SQLAlchemy for database operations and returns data in JSON format.




Features


Database Management: Create, read, update, and delete cafe records using SQLAlchemy.


API Endpoints:

GET /random: Retrieve a random cafe.

GET /all: Retrieve all cafes sorted by name.

GET /search: Search for cafes by location.

POST /add: Add a new cafe.

PATCH /update-price/<id>: Update the coffee price of a specific cafe.

DELETE /delete-cafe/<cafe_id>: Delete a specific cafe from the database.

Interactive Web Interface: Search for cafes by location and view results without reloading the page.

JSON Responses: Easily consumable JSON data format.


![image](https://github.com/user-attachments/assets/2781c3ec-449f-4d19-a48d-d13509ec991f)

