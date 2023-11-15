from flask import Flask, abort, redirect, render_template, request

app = Flask(__name__)

# config database

@app.get('/')
def index():
    return render_template('login.html')

@app.route('/create_account')
def create_account():
    return render_template('create_account.html')
