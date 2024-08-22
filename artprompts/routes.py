from flask import render_template, redirect, url_for, flash, request
from app import app
from artprompts.models import db
from artprompts.forms import SignupForm, LoginForm
from artprompts.models import User, Prompt, Subscriber
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))



# TODO: This needs to be cleaned up
from datetime import datetime
import random
random.seed(datetime.now().time())

def get_daily_prompt(category=None):
    if category:
        prompts = Prompt.query.filter_by(category=category).all()
    else:
        prompts = Prompt.query.all()
    
    if not prompts:
        return "No prompts available"

    return random.choice(prompts).text

@app.route('/about', methods=['GET'])
def about():
    return render_template(
        'about.html',
        active_page='about'
    )

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']
    subscriber = Subscriber(
        email=email
    )
    db.session.add(subscriber)
    db.session.commit()
    # Here, you can add logic to store the email or send a confirmation email
    return redirect(url_for('thank_you'))

@app.route('/thank-you')
def thank_you():
    return redirect(url_for('home'))

@app.route('/')
# @login_required
def home():
    category = request.args.get('category')
    daily_prompt = get_daily_prompt(category)
    return render_template(
        'index.html', 
        prompt=daily_prompt, 
        selected_category=category,
        active_page='home'
    )