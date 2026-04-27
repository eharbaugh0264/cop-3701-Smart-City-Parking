Prerequisites:
-Have a Database Schema with the required tables

-Have local Python compiler that has the required app.py 

-Make sure the imports are installed into your local machine of choice streamlit, oracledb, and pandas

Setup Order:
-Create the database using the create_db.sql file
-Modify in dataload.py the DB_User, DB_Password, and LIB_DIR variables to match your client and login credentials

Run Instructions
-Run “streamlit python app.py” in your local environment, or similarly  "py -m streamlit run *app.py" replacing the * with an absolute file path

-once the streamlit tab opens in your browser copy and paste your database username and password and press enter

-once connected to the database you can click on the dropdown menu to switch between features

-In the features you can select the desired input and click “Run” to return the query result
