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


@app.route('/edicao/', methods=['GET'])
def edit():

    return render_template('edit.html')


@app.route('/tabela/', methods=['GET'])
def tabela():
    try:
        if not session.database.connection.is_connected():
            session.reconnectDatabase()
    except:
        pass
    
    return render_template('visualization.html')

@app.route('/visualizar_cadastro/', methods=['GET'])
def visualizar_cadastro():
    try:
        if not session.database.connection.is_connected():
            session.reconnectDatabase()
    except:
        pass
    id = request.args['id']
    
    sql = f'SELECT * FROM cadastros WHERE id = {id}'
    data = session.database.run(sql)[0]
    
    
    return render_template('edit.html', id=id)


@app.route('/try_signup/', methods=['POST'])
def signup_form():
    try:
        if not session.database.connection.is_connected():
            session.reconnectDatabase()
    except:
        pass
    
    empresa = request.form['empresa']
    documento = request.form['cnpj']
    pessoa = 'juridica'
    if not empresa:
        empresa = 'Pessoa física'
        documento = request.form['cpf']
        pessoa = 'fisica'

    try:
        data = {
            'nome': request.form['nome'],
            'email': request.form['email'],
            'documento': documento,
            'telefone': request.form['telefone'],
            'status': 'Aguardando',
            'empresa': empresa,
            'rua': request.form['rua'],
            'numero': request.form['numero'],
            'bairro': request.form['bairro'],
            'cidade': request.form['cidade'],
            'estado': request.form['estado'],
            'contract-type': request.form['contract-type'],
            'contract-validity': request.form['contract-validity'],
            'contract-value': request.form['contract-value'],
            'url': request.form['url'],
            'pessoa': pessoa
            
        }
        session.signup(data)
        print(data)
        return 'Sucesso'
    except Exception as error:
        print(error)
        return 'Erro'


@app.route('/get_table_data/', methods=['GET'])
def get_table_data():
    try:
        if not session.database.connection.is_connected():
            session.reconnectDatabase()
    except:
        pass
    data = session.database.fetchTable(0, 'cadastros')
    return str(data)


@app.route('/get_added_buttons/', methods=['GET'])
def get_added_buttons():
    try:
        if not session.database.connection.is_connected():
            session.reconnectDatabase()
    except:
        pass
    
    sql = f'SELECT * FROM status_criados ORDER BY id ASC'
    status_criados = session.database.run(sql)
    return str(status_criados)


@app.route('/new_button/', methods=['POST'])
def new_button():
    try:
        if not session.database.connection.is_connected():
            session.reconnectDatabase()
    except:
        pass
    
    button_name = request.form['button_name']
    id = request.form['id']
    sql = f'INSERT INTO status_criados (id,status) VALUES ({id},"{button_name}")'
    session.database.run(sql=sql, commit=True)
    return 'oi'


@app.route('/change_status/', methods=['POST'])
def change_status():
    try:
        if not session.database.connection.is_connected():
            session.reconnectDatabase()
    except:
        pass
    
    if not eval(request.form['mass']):
        sql = f'UPDATE cadastros SET status = "{request.form["status"]}" WHERE id = {request.form["id"]}'
        session.database.run(sql, commit=True)
    else:
        for cadastro_id in eval(request.form['ids']):
            sql = f'UPDATE cadastros SET status = "{request.form["status"]}" WHERE id = {cadastro_id}'
            session.database.run(sql, commit=True)

    return 'oi'

@app.route('/change_config/', methods=['POST'])
def change_config():
    id = request.form['id']
    checked = request.form['checked']

    sql = f"UPDATE config SET VALUE = '{str(checked)}' WHERE element = '{id}';"
    try:
        session.database.run(sql, commit = True)
        return 'True'
    except Exception as error:
        print(error)
        return error
    
@app.route('/get_config/', methods=['GET'])
def get_config():
    try:
        if not session.database.connection.is_connected():
            session.reconnectDatabase()
    except:
        pass
    
    sql = 'SELECT * FROM config ORDER BY id ASC;'
    data = session.database.run(sql)
    return str(data)


# end of file
if __name__ == '__main__':
    context = ('../ssl/certs/sistema_g2corretora_com_br_d32ab_01c35_1680429502_8e0dc33bedc848d2c3f2bc77dd27a358.crt', '../ssl/keys/d32ab_01c35_7c2f3e1a175ba700fdad9506f704b0d3.key')
    app.run(debug=True, host="0.0.0.0", port="5002", ssl_context=context)
