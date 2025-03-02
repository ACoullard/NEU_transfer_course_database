from flask import Flask, request


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world'

@app.get('/api')
def get_api():
    param = request.args.get('param')
    return {'test': 10}