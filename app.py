import os
import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.environ.get('MONGODB_URL'))
    app.db = client.microblog

    @app.route('/', methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            entry_content = request.form.get('content')
            formatted_date = datetime.datetime.today().strftime('%Y-%m-%d')
            app.db.entries.insert({'content': entry_content, 'date': formatted_date})

        entries = [
            (
                e['content'],
                e['date'],
                datetime.datetime.strptime(e['date'], '%Y-%m-%d').strftime('%b %d')
            )
                for e in app.db.entries.find({})]
        return render_template('home.html', entries = entries)
    return app
