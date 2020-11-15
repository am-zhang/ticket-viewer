from flask import Flask, render_template, send_file
import requests
import os
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__)
load_dotenv(find_dotenv()) # fetches username and password and subdomain from .env
app.config['zendesk_username'] = os.environ['ZENDESK_USERNAME']
app.config['zendesk_password'] = os.environ['ZENDESK_PASSWORD']
app.config['zendesk_subdomain'] = os.environ['ZENDESK_SUBDOMAIN']

@app.route('/favicon.ico')
def icon():
    return send_file('static/zendesk-favicon.ico') # custom favicon

@app.route('/')
def ticket_list():
    tickets = []
    url = 'https://' + app.config['zendesk_subdomain'] + '.zendesk.com/api/v2/tickets.json'
    while url:
        r = requests.get(url, auth=(app.config['zendesk_username'], app.config['zendesk_password']))
        if r.status_code != 200: # checks that the API is available
            return render_template('error.jinja2', code=r.status_code) # error page
        response_json = r.json()
        tickets += response_json['tickets']
        url = response_json['next_page']
    return render_template('index.jinja2', tickets=tickets) # viewer page

if __name__ == '__main__':
    app.run(debug=True)

