from flask import Flask, request
from flask_cors import CORS
from database import Database

FRONTEND_URL = r"https://transfercreditneu.acserver.net"

app = Flask(__name__)

CORS(app,
     resources={r"/api*":{"origins":FRONTEND_URL}}
     
     )

db = Database()

# @app.route('/')
# def hello_world():
#     return "hello world\nThis is the flask app"

@app.get('/api/course')
def get_course():
    code = request.args.get('class_code')
    responce = db._find_courses_by_code(code)
    print("responce", responce)
    return responce

@app.get('/api/courseslist')
def get_course_list():
    responce = db.get_codes_by_dept_dict()
    return responce

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')