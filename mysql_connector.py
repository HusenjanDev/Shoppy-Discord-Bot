import mysql.connector
from datetime import datetime

class mysql_connection():
    def __init__(self, _host, _port, _user, _password):

        self.connection = mysql.connector.connect(
            host = _host,
            port = _port,
            user = _user,
            password = _password
        )

        self.cursor = self.connection.cursor()
    
    def ping(self):
        self.connection.ping(reconnect = True, attempts = 1, delay = 0)

    def query(self, sql):
        self.cursor.execute(sql)

    def fetchone(self):
        return self.cursor.fetchone()
    
    def fetchall(self):
        return self.cursor.fetchall()

    def create_database(self, database):
        self.query('create database if not exists {0}'.format(database))

        self.connection.commit()
    
    def create_table(self, database, table):
        self.query('use {0}'.format(database))

        self.query('''
            create table if not exists {0} (
                discord_username varchar(40) default null,
                discord_id varchar(40) default null,
                order_id varchar(40) default null,
                config_name varchar(30) default null,
                date date default null
                )'''.format(table))
        
        self.connection.commit()

    def insert(self, database, table, discord_username, discord_id, order_id, config_name):
        self.query('use {0}'.format(database))

        self.query('''insert into {0} (discord_username, discord_id, order_id, config_name, date) values ("{1}", "{2}", "{3}", "{4}", "{5}")'''.
            format(table, discord_username, discord_id, order_id, config_name, datetime.now().strftime('%Y-%m-%d')))
        
        self.connection.commit()

    def delete(self, database, table, order_id):
        self.query('use {0}'.format(database))

        self.query('delete from {0} where order_id = "{1}"'.format(table, order_id))

        self.connection.commit()
    
    def auth(self, database, table, discord_username, discord_id, order_id, config_name):
        self.ping()
        
        self.query('use {0}'.format(database))

        self.query('select order_id from {0} where order_id = "{1}"'.format(table, order_id))

        auth = self.fetchone()

        if not auth:

            self.insert(database, table, discord_username, discord_id, order_id, config_name)

            return 0
        
        else:
            
            return -1
    
    def get_order_information(self, database, table, order_id):
        self.ping()
        
        self.query('use {0}'.format(database))

        self.query('select discord_username, config_name from {0} where order_id = "{1}"'.format(table, order_id))

        row = self.fetchone()

        if not row:

            return -1
        
        else:

            return row