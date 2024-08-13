from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prompts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
random.seed(datetime.now().time())

class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String(250), nullable=True)

def get_daily_prompt(category=None):
    if category:
        prompts = Prompt.query.filter_by(category=category).all()
    else:
        prompts = Prompt.query.all()
    
    if not prompts:
        return "No prompts available"

    return random.choice(prompts).text

@app.route('/')
def index():
    category = request.args.get('category')
    daily_prompt = get_daily_prompt(category)
    return render_template(
        'index.html', 
        prompt=daily_prompt, 
        selected_category=category
    )

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
