from flask import Flask, render_template, request, redirect
from flask import url_for, flash, abort, session, jsonify
import json
import os
import time

app = Flask(__name__)
app.config.from_object('config.Config')


@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/news')
def news():
    all_news = []
    if os.path.exists('news.json'):
        with open('news.json') as news_file:
            saved_news = json.load(news_file)
            for news in saved_news.values():
                print(news)
                all_news.append(news)
    session['all_news'] = all_news
    return render_template('news.html')


@app.route('/contact_us', methods=['GET', 'POST'])
def contactUs():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_no = request.form['phone_no']
        message = request.form['message']
        contacts = {}
        current_time = time.time()
        if os.path.exists('contact_us.json'):
            with open('contact_us.json') as contact_file:
                contacts = json.load(contact_file)
        contacts[current_time] = {'name':name, 'email':email, 'phone_no':phone_no, 'message':message}
        with open('contact_us.json', 'w') as contact_file:
            json.dump(contacts, contact_file)
        return redirect(url_for('contactUs'))
    return render_template('contact_us.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        full_name = first_name + " " + last_name
        users = {}

        if os.path.exists('users.json'):
            with open('users.json') as users_file:
                users = json.load(users_file)
                if full_name in users.keys():
                    session['user'] = first_name
                    return redirect(url_for('home'))
        flash('Invalid login.')
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        full_name = first_name + " " + last_name
        users = {}
        if os.path.exists('users.json'):
            with open('users.json') as users_file:
                users = json.load(users_file)
                if full_name not in users.keys():
                    users[full_name] = {'first_name' : first_name, 'last_name' : last_name}
                    with open('users.json', 'w') as users_file:
                        json.dump(users, users_file)
                    session.user = first_name
                    return redirect(url_for('home'))
        flash('use another name')
        return redirect(url_for('register'))
    return render_template('register.html')


@app.route('/add_news', methods=['GET','POST'])
def addNews():
    if request.method == 'POST':
        headline = request.form['headline']
        category = request.form['category']
        author = request.form['author']
        description = request.form['description']
        news = {}
        current_time = time.time()
        if os.path.exists('news.json'):
            with open('news.json') as news_file:
                news = json.load(news_file)
        news[current_time] = {'headline':headline, 'description':description, 'category':category, 'author':author}
        with open('news.json', 'w') as news_file:
            json.dump(news, news_file)
        return redirect(url_for('addNews'))
    return render_template('add_news.html')

if __name__ == '__main__':
    app.run(debug =True)
