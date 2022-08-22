from flask import Flask, request, url_for, redirect, render_template
from src.session_handler import Session, Connection
from src.mysql_handler import Mysql

session = Session()
app = Flask(__name__)

@app.route('/home/', methods=['GET'])
def home():
    
    return render_template('home.html')

@app.route('/signup/', methods=['POST'])
def signup_form():
    try:
        data = {
            'nome': request.form['nome'],
            'email': request.form['email'],
            'documento': request.form['documento'],
            'cep': request.form['cep'],
        }
        session.signup(data)
        return 'Sucesso'
    except Exception as error:
        print(error)
        return error

# end of file
app.run(debug=True, host="0.0.0.0", port="5001")
