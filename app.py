# Code_ver1.0 by Shuvamoy Bhattacharya on 17Feb2020
#-----------------------------------------------------
# Prerequisite: 
# Install Python 3.8 
# pip install flask
# pip install flask sqlite3
#-----------------------------------------------------

from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import sqlite3
import json
import os


app = Flask(__name__)

# Set the Database Connection
def get_db_connection():
    conn = sqlite3.connect('sb_formdata.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS sbforms (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE,
                        age INTEGER,
                        address TEXT
                    )''')
    conn.commit()
    conn.close()



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    # Extracting data from the form
    name = request.form['name']
    email = request.form['email']
    age = int(request.form['age'])
    address = request.form['address']
    
    # Creating a dictionary to store the data
    sb_form_data = {
        "name": name,
        "email": email,
        "age": age,
        "address": address
    }

    # Convert dictionary to JSON string and print it
    json_str = json.dumps(sb_form_data)
    print("\nConverted JSON Data: \n", json_str)

    
    json_directory = "JSON_Files"
    # Check if the directory exists
    if not os.path.exists(json_directory):
        # If it doesn't exist, create it
        os.makedirs(json_directory)
        print(f"Directory '{json_directory}' was created.")
    else:
        # If it exists, you can print that it already exists
        print(f"Directory '{json_directory}' already exists.")

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")
    json_filename = f"{json_directory}\sb_formdata_{formatted_datetime}.json"

    # Write data to a JSON file
    with open(json_filename, 'w') as json_file:
        json.dump(sb_form_data, json_file, indent=4)

    
    # Insert the values to Database
    create_table()
    # Insert data into the database
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO sbforms (name, email, age, address) VALUES (?, ?, ?, ?)',
                     (name, email, age, address))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error: That email already exists.")
    finally:
        conn.close()
    
    # Returning the data as a JSON response
    # return jsonify(sb_form_data)
    return redirect(url_for('display_json', **sb_form_data))



@app.route('/display_json')
def display_json():
    # users = User.query.all()
    # return render_template('display_json.html', users=users)
    return render_template('display_json.html')


if __name__ == '__main__':
    app.run(debug=True, port=3000)

