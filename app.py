from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config.from_object('config.Config')
db=SQLAlchemy(app)
@app.route('/')
def hello():
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)