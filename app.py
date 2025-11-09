from flask import Flask, render_template, jsonify, abort, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://slyn:IOJaBjIcTPmozPSV7gYaPG3r9HHluXIm@dpg-d48adc6mcj7s73drv23g-a/fox_store'
app.config['SECRET_KEY'] = '5bae2b11e01ff0c318ed744434506229b46a298c7e7ef52a2f3bb171130c65cf'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 300,
    'pool_pre_ping': True
}

db = SQLAlchemy(app)
migrate = Migrate(app, db)


import models


import routes

if __name__ == '__main__':
    app.run(debug=True)