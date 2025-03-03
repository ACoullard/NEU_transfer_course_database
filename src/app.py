from flask import Flask, request
from database import Database

class Server:
    app = Flask(__name__)
    def __init__(self):
        
        self.db = Database()

    @app.route('/')
    def hello_world():
        return str()

    @app.get('/api')
    def get_api():
        code = request.args.get('class_code')
        return db._find_courses_by_code(code)