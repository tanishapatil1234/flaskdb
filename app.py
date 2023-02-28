from flask import Flask, request, jsonify
import json
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/average/*": {"origins": "*"}})
cors = CORS(app, resources={r"/getrev/*": {"origins": "*"}})
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/reviews/<int:id>', methods=['PUT'])
def update_review(id):
    # get the data from the request body
    data = request.get_json()
    # create a connection to the database
    conn = sqlite3.connect('reviews.sqlite')
    # execute the update query
    cursor = conn.cursor()
    cursor.execute('UPDATE reviews SET name=?, rate=?, review=? WHERE id=?', (data['name'], data['rate'], data['review'], id))
    conn.commit()
    # check if the query affected any rows
    if cursor.rowcount == 0:
        return {'message': 'Review not found.'}, 404
    # close the cursor and connection objects
    cursor.close()
    conn.close()
    return {'message': 'Review updated successfully.'}





def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('reviews.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    conn = db_connection()
    cursor = conn.cursor

    if request.method == "GET":
        cursor = conn.execute("SELECT * FROM reviews")
        reviews = [
            dict(id=row[0], name=row[1], review=row[2], rate=row[3])
            for row in cursor.fetchall()
        ]
        if reviews is not None:
            return jsonify(reviews)

    if request.method == 'POST':
        print("POst method works")
        new_name = request.json['name']
        new_review = request.json['review']
        new_rate = request.json['rate']
        sql = """INSERT INTO reviews (name, review, rate)
                 VALUES (?, ?, ?)"""
        cursor = conn.execute(sql, (new_name, new_review, new_rate))
        conn.commit()
        return f"Review created successfully", 201

@app.route('/delete/<id>', methods = ["GET"])
def delete_review(id):
    message = {}
    if request.method == 'GET':
        try:
            conn = db_connection()
            conn.execute("DELETE from reviews WHERE id = ?",
                     (id,))
            conn.commit()
            message["status"] = "User deleted successfuly"
        except:
            message["status"] = "error cant delete user"
        return message

@app.route('/getrev', methods=['GET'])
def getreviews():
   if request.method == "GET": 
        conn = db_connection()
        cursor = conn.cursor
        rate = None
        cursor = conn.execute("SELECT * FROM reviews")
        reviews = [
            dict(id=row[0], name=row[1], review=row[2], rate=row[3])
            for row in cursor.fetchall()
        ]
        if reviews is not None:
            return jsonify(reviews)
    

    


@app.route('/average', methods=['GET'])
def average_rate():
   if request.method == "GET": 
        conn = db_connection()
        cursor = conn.cursor
        rate = None
        cursor = conn.execute("SELECT round(avg(rate),2) FROM reviews")
        result = cursor.fetchall()
        if result is not None:
            for row in result:
                rate = row[0]
           # response = 
           # response.headers.add('Access-Control-Allow-Origin', '*')
            return str(rate)
        else:
            return "Something wrong", 404

@app.route('/rateslist', methods=['GET'])
def index():
    if request.method == "GET":
        conn = sqlite3.connect('reviews.sqlite')
# Create a cursor object
        cursor = conn.cursor()
# Execute a SELECT statement to retrieve data from a specific column
        cursor.execute('SELECT rate FROM reviews')
# Fetch all the rows and store the data in a list
        column_data = [row[0] for row in cursor.fetchall()]
# Close the cursor and connection objects
        cursor.close()
        conn.close()
# Print the data stored in the list
        return column_data






if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)