import mysql.connector
import src.config


class Mysql():
    # def __init__(self) -> None:
    #     pass
    
    def run(self, sql, commit = False):
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(sql)
        data = None
        if commit:
            self.connection.commit()   
        else:
            data = cursor.fetchall()
            self.connection.commit()  

        cursor.close()
        return data

    def connect(self, auth):
        ''' Try to connect to a database with auth params defined in config file '''
        try:
            self.connection = mysql.connector.connect(host=auth['host'],
                                                      database=auth['database'],
                                                      user=auth['user'],
                                                      password=auth['password'])
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = self.connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                # cursor.close()
                self.auth = auth

                return self.connection

        except Exception as e:
            print(e)

    def disconnect(self):
        ''' Disconnect from database '''
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")

    def fetchTable(self, rows, table, condition=None, value=None, reversed=None, ordered=None):
        ''' Fetch a number of rows from a table that exists in database.
        Number of rows and table defined in config file.
        if number of rows equals to 0, will try to fetch all rows.'''

        if condition:
            sql = f'SELECT * FROM `{table}` WHERE {condition} = "{value}"'
            if reversed:
                sql = f'SELECT * FROM `{table}` WHERE {condition} = "{value}" ORDER BY {reversed} DESC'
        else:
            sql = f"SELECT * FROM `{table}` WHERE 1"

        if ordered:
            sql = f'{sql} ORDER BY {ordered} ASC'

        cursor = self.connection.cursor(buffered=True)
        cursor.execute(sql)
        if rows > 1:
            records = cursor.fetchmany(rows)
        else:
            records = cursor.fetchall()

        # print(f'Total number of rows in table: {cursor.rowcount}')
        # print(f'Rows fetched: {len(records)}')

        data = []
        for row in records:
            row = list(row)
            data.append(row)

        cursor.close()
        return data

    def insertCadastro(self, data):
        ''' Fun????o utilizada para inserir novo membro no banco de dados.
        DATA requer (ID, USU??RIO, SENHA, NOME, ENDERE??O, TIPO DE MEMBRO) '''

        try:
            sql = f"INSERT INTO cadastros (id, nome, email, documento, empresa, status, vencimento, telefone, pessoa, rua, numero, bairro, cidade, estado, contrato, valor, url) VALUES ({data['id']}, '{data['nome']}', '{data['email']}', '{data['documento']}', '{data['empresa']}', '{data['status']}', '{data['contract-validity']}', '{data['telefone']}', '{data['pessoa']}', '{data['rua']}', '{data['numero']}', '{data['bairro']}', '{data['cidade']}', '{data['estado']}', '{data['contract-type']}', '{data['contract-value']}', '{data['url']}')"
            cursor = self.connection.cursor()
            cursor.execute(sql)
        except:
            sql = f'INSERT INTO cadastros (id, nome, email, documento, empresa, status, vencimento, telefone, pessoa, rua, numero, bairro, cidade, estado, contrato, valor, url) VALUES ({data["id"]}, "{data["nome"]}", "{data["email"]}", "{data["documento"]}", "{data["empresa"]}", "{data["status"]}", "{data["contract-validity"]}", "{data["telefone"]}", "{data["pessoa"]}", "{data["rua"]}", "{data["numero"]}", "{data["bairro"]}", "{data["cidade"]}", "{data["estado"]}", "{data["contract-type"]}", "{data["contract-value"]}", "{data["url"]}")'
            cursor = self.connection.cursor()
            cursor.execute(sql)

        self.connection.commit()
        cursor.close()

    def insertPost(self, data):
        sql = f"INSERT INTO Blog (ID, MEMBRO, TITULO, CONTEUDO, AUTOR, DATA) VALUES {data}"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

    def insertRequest(self, data):
        sql = f"INSERT INTO Solicitacoes (ID, USUARIO, SOLICITACAO, SITUACAO, DATA, URL, PROTOCOLO) VALUES {data}"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

    def updateTable(self, table, id, column, value, id_column):
        command = f'Update {table} set {column} = "{value}" where {id_column} = {id}'
        cursor = self.connection.cursor()
        cursor.execute(command)
        self.connection.commit()
        cursor.close()
        print("Record Updated successfully ")
