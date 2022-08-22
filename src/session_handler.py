from datetime import datetime, timedelta, date
from src.config import TIMELIMIT, database_auth
from src.mysql_handler import Mysql


class Connection():
    def __init__(self, ip, database, id):
        self.id = id
        self.buildAttributes(ip, database)

        self.expira = datetime.now() + timedelta(minutes=TIMELIMIT)

    def isExpired(self):
        if not datetime.now() < self.expira:
            return True

    def buildAttributes(self, ip, database):
        data = database.fetchTable(1, 'Membros', 'ID', self.id)[0]
        self.ip = ip
        self.user = data[1]
        self.password = data[2]
        self.name = data[3]
        self.uf = data[4]
        for item in data[22].split(','):
            self.especialidades.append(item)
        self.solicitacoes = database.fetchTable(
            0, 'Solicitacoes', 'USUARIO', self.id, ordered='ID')
        self.solicitacoes.reverse()

class Session():
    def __init__(self):
        self.connections = []
        self.cadastros = []
        self.solicitacoes_disponiveis = []
        self.database = Mysql()
        self.database.connect(database_auth)
        self.getCadastros()

    def getCadastros(self):
        try:
            if not self.database.connection.is_connected():
                self.reconnectDatabase()
        except:
            pass

        self.cadastros = []
        
        try:
            members = self.database.fetchTable(0, 'cadastros')

            for member in members:
                data = {
                    'id': member[0],
                    'nome': member[1],
                    'email': member[2],
                    'documento': member[3],
                    'cep': member[4],
                }
                self.cadastros.append(data)
        except Exception as error:
            print(error)

    def reconnectDatabase(self):
        self.database.connect(database_auth)

    def getConnection(self, ip):
        for connection in self.connections:
            if connection.ip == ip:
                if not connection.isExpired():
                    return connection
                else:
                    self.connections.remove(connection)

    def signup(self, data):
        try:
            if not self.database.connection.is_connected():
                self.reconnectDatabase()
        except:
            pass
        
        data.update({'id': len(self.cadastros)})
        self.database.insertCadastro(data)
        self.cadastros.append(data)
        return 'Usuário cadastrado', True

