from flask import Flask, request, url_for, redirect, render_template
from src.session_handler import Session, Connection
from src.mysql_handler import Mysql

session = Session()
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/cadastro/', methods=['GET'])
def cadastro():
    
    return render_template('signup.html')
    
@app.route('/config/', methods=['GET'])
def config():
    
    return render_template('config.html')
    
@app.route('/tabela/', methods=['GET'])
def tabela():
    
    return render_template('visualization.html')

@app.route('/try_signup/', methods=['POST'])
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
        return 'Erro'
    
@app.route('/get_table_data/', methods=['GET'])
def get_table_data():
    data = session.database.fetchTable(0, 'cadastros')
    return str(data)

# end of file
app.run(debug=True, host="0.0.0.0", port="5001")
