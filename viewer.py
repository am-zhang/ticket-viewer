from flask import Flask, render_template, send_file
import requests
import os
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__)
load_dotenv(find_dotenv())
zendesk_username = os.environ['ZENDESK_USERNAME']
zendesk_password = os.environ['ZENDESK_PASSWORD']

@app.route('/favicon.ico')
def icon():
    return send_file('static/zendesk-favicon.ico')

@app.route('/')
def ticket_list():
    tickets = []
    url = 'https://azic.zendesk.com/api/v2/tickets.json'
    while url:
        r = requests.get(url, auth=(zendesk_username, zendesk_password))
        if r.status_code != 200:
            return render_template('error.jinja2')
        response_json = r.json()
        tickets += response_json['tickets']
        url = response_json['next_page']
    return render_template('index.jinja2', tickets=tickets)

if __name__ == '__main__':
    app.run()

