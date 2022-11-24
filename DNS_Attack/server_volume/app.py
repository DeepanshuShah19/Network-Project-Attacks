from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
app = Flask(__name__)

@app.route('/login', methods=['GET'])
def login():
    return jsonify({'message' : 'Hello, World!'})

@app.route('/')
def home():
   return render_template('index.html')
   
if __name__ == "__main__":
    app.run(debug=True)
