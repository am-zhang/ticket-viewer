# zendesk-ticket-viewer-f20

This ticket viewer connects to Zendesk API and requests all tickets from an account. It displays all the tickets on a web page and allows the user to page through tickets. 


The program can be run in a virtual environment with the following commands:

```
sudo apt-get install python3-venv

python3 -m venv venv

source venv/bin/activate
```


The program also relies on a few packages which can be installed with the following command:

`pip install -r requirements.txt`


In order to populate tickets from the users account, a .env file must be created in the following format:

```
ZENDESK_USERNAME=user@email.com

ZENDESK_PASSWORD=userpassword

ZENDESK_SUBDOMAIN=usersubdomain
```


The viewer can be run with the following command:

`python viewer.py`


You should then be able to access the Flask app at: http://localhost:5000/


Finally, test cases can be run with the following command:

`python viewer.test.py`


Note: Individual ticket view is powered by Fancybox, a Javascript lightbox library licensed under the GPLv3 license. More documentation can be found here: https://fancyapps.com/fancybox/3/.
