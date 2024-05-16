## Flask Application to Submit the Form Data to SQLite Database
> A simple Flask application that submits form data to an SQLite3 database and simultaneously generates a JSON file containing the same data.


## The Steps:

### i. Install necessary PIP packages (Flask and sqlite3).

+  `pip install flask` <br>
+  `pip install flask sqlite3` <br>

#### ii. Write the Python Code to develop the Web Application


#### iii. Run the Server in Localhost.
+  `>python app.py` <br>

   ![CustomerTableView](static/img/git_images/run_flask_application.png "Run The Flask Web Application") <br>


#### ii. Form Submission
> The Name, Email ID and Age fields are required or mandatory. For the address field, the text area can be expanded in case more information needs to be written.<br>

 ![CustomerTableView](static/img/git_images/Form_Submission.png "Form Submission") <br>


#### iii. Display the Data in JSON Format
 ![CustomerTableView](static/img/git_images/display_in_json_format.png "User Data in JSON format") <br>

#### iv. Generate a JSON file (rename with current date and time) containing the same Form Data.
 ![CustomerTableView](static/img/git_images/json_files.png "JSON files") <br>


#### v. Connect the Database (SQLite3).
 ![CustomerTableView](static/img/git_images/connect_db.png "Database Config") <br>


#### vi. Insert the submitted Form Data to the Database table.
 ![CustomerTableView](static/img/git_images/data_inserted_to_SQlite_database.png "Data inserted to Database Table") <br>

