# messenger_api

RESTful API for a social media platform. 
The API allow users to create profiles, create and retrieve posts, and perform basic social media actions.


## Installation

Requirement : Python 3

Documentation : Swagger 😎

```shell
git clone https://github.com/Anatolii-Poznyak/messenger_api
cd messenger_api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
copy .env.sample -> .env and add your values there
python manage.py migrate
python manage.py runserver # Starts Django Server
```
