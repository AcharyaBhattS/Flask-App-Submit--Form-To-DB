# Code_ver1.0 by Shuvamoy Bhattacharya on 17Feb2020
#-----------------------------------------------------
# Prerequisite: 
# Install Python 3.8 
# pip install flask
# pip install flask sqlite3
#-----------------------------------------------------

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
# from flask_wtf import CSRFProtect
from datetime import datetime
import sqlite3
import json
import os


app = Flask(__name__)

messages = []

# Set the Database Connection
def get_db_connection():
    conn = sqlite3.connect('sbhatt_db1.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS sbforms (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE,
                        age INTEGER,
                        address TEXT,
                        created_on DATETIME DEFAULT (strftime('%d-%m-%Y %H:%M:%S', 'now', 'localtime'))
                    )''')
    conn.commit()
    conn.close()



# Index
@app.route('/', methods=['GET', 'POST'])
def index():
    create_table()
    conn = get_db_connection()
    cursor = conn.cursor()
    # cursor.execute("SELECT * FROM sbforms")
    cursor.execute("SELECT * FROM sbforms ORDER BY id DESC")
    alldata = cursor.fetchall()
    conn.close()
    # Submission
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        address = request.form['address']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sbforms (name, email, age, address) VALUES (?, ?, ?, ?)",
                       (name, email, age, address))
        conn.commit()
        conn.close()

        # Creating a dictionary to store the data
        sb_form_data = {
            "name": name,
            "email": email,
            "age": age,
            "address": address
        }
        # Convert dictionary to JSON file
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

        return redirect(url_for('index'))

    # Return a blank form for new submissions
    return render_template('index.html', submitteddata=alldata, sldata=None)



# Edit
@app.route('/edit/<int:pk>', methods=['GET', 'POST'])
def edit(pk):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sbforms WHERE id = ?", (pk,))
    selecteddata = cursor.fetchone()
    print("\nselecteddata: ", selecteddata)

    if not selecteddata:
        conn.close()
        return "User data not found", 404

    if request.method == 'POST':
        # Fetch and update the data in POST
        name = request.form['name']
        email = request.form['email']
        age = int(request.form['age'])
        address = request.form['address']
        update_query = "UPDATE sbforms SET name=?, email=?, age=?, address=? WHERE id=?"
        cursor.execute(update_query, (name, email, age, address, pk))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        # Just display data in GET
        cursor.execute("SELECT * FROM sbforms")
        alldata = cursor.fetchall()
        conn.close()
        return render_template('index.html', submitteddata=alldata, sldata=selecteddata)



# Display JSON Data
@app.route('/display_json')
def display_json():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records ORDER BY id DESC LIMIT 1")
    last_record = cursor.fetchone()
    print(last_record)
    return render_template('display_json.html')



# Delete Row data
@app.route('/delete/<int:pk>', methods=['GET', 'POST'])
def delete(pk):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM sbforms WHERE id = ?', (pk,))
    conn.commit()
    conn.close()
    message = "Deleted User Data"
    messages.append(message)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=7000)

