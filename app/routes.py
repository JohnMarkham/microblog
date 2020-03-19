from flask import render_template, flash, redirect
from app import my_app
from app.forms import LoginForm

#This is the URL /lgoinsss, and login is the name referened in url_for('login')
@my_app.route('/loginsss', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, rembemer_me={}'.format(form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title = 'Sign In', form = form)

@my_app.route('/')
@my_app.route('/index')
def index():
    user = {"username":"John Markham"}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool'
        }
    ]
    return render_template('index.html', title='Home', user = user, posts = posts)
