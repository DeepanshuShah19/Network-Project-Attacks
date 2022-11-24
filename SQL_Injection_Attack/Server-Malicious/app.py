from flask import Flask
from flask import jsonify
from flask import request
import mysql.connector

app = Flask(__name__)

@app.route('/login', methods=['GET'])
def login():
    mydb = mysql.connector.connect(
        host="10.10.0.7",
        user="root",
        password="password",
        database="hr"
        )
        
    mycursor = mydb.cursor()

    user_credentials = request.get_json()
    mycursor.execute(f"SELECT userid, password, fname, lname, gender, dtob, country, user_rating, emailid FROM user_details where userid = '{ user_credentials['userid'] }' and password = '{ user_credentials['password'] }'")
    
    myresult = mycursor.fetchall()

    if len(myresult) == 0:
        print("No matching credentials")
        return jsonify([])
    else:
        response = []
        for row in myresult:
            user_details = {}
            count = 0 
            for field in ['userid', 'password', 'fname', 'lname', 'gender', 'dtob', 'country', 'user_rating', 'emailid']:
                user_details[field] = row[count]
                count+=1

            response.append(user_details)
        return jsonify(response)
    

if __name__ == "__main__":
    app.run(debug=True)
