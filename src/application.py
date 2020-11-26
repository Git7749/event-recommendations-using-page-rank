from flask import Flask, render_template, url_for, request, redirect, json
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# from flask import Flask, render_template, json, url_for

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    users = '[{"id":"1", "name" : "kumar"}, {"id":"2" ,"name" : "divya"},{"id":"3" , "name": "rohit"}]'
    tasks = json.loads(users)
    return render_template('index.html', tasks=tasks)

@app.route('/recommend', methods=['Post'])
def recommendations():
    events = '[{"id":"11", "name" : "sun burn"}, {"id":"12" ,"name" : "kochela"},{"id":"13" , "name": "sreemantam"}]'
    tasks = json.loads(events)
    return render_template('events.html', tasks=tasks)

@app.route('/hotels', methods=['GET'])
def hotel():
    hotels = '[{"id":"21", "name" : "novotel"}, {"id":"22" ,"name" : "marriot"},{"id":"23" , "name": "taj"}]'
    tasks = json.loads(hotels)
    return render_template('hotels.html', tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)