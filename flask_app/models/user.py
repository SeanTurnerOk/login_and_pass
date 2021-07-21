from flask_app.config.SQLconnector import MySQLConnection
import re
from flask import flash
class User:
    def __init__(self, data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.updated_at=data['updated_at']
        self.created_at=data['created_at']
    @classmethod
    def get_all(cls):
        query="SELECT * FROM users"
        results=MySQLConnection.connectToMySQL('usersandpass').query_db(query)
        users=[]
        for each in results:
            users.append(cls(each))
        return users
    @classmethod
    def getByEmail(cls,email):
        query='SELECT * FROM users WHERE email = %(email)s'
        return MySQLConnection.connectToMySQL('usersandpass').query_db(query, email)
    @classmethod
    def save(cls, data):
        data['id']=len(cls.get_all())+1
        query="INSERT INTO users (id, first_name, last_name, password, email) VALUES (%(id)s, %(first_name)s, %(last_name)s, %(password)s, %(email)s)"
        return MySQLConnection.connectToMySQL('usersandpass').query_db(query, data)
    @staticmethod
    def validate_user(user):
        is_valid=True
        if len(user['first_name'])< 3:
            flash('First name must be at least three characters')
            is_valid=False
        if len(user['last_name'])< 3:
            flash('Last name must be at least three characters')
            is_valid=False
        if len(user['email'])< 3:
            flash('Email must be at least three characters')
            is_valid=False
        if len(user['password'])< 3:
            flash('Password must be at least three characters')
            is_valid=False
        if not re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$').match(user['email']):
            flash('Invalid email address!')
            is_valid = False
        return is_valid