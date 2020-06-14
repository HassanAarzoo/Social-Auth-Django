
Create a Python Virtual Environment

Eg command to create a Virtual Environment 
```
python3 -m venv virtualenvironment
```
Activate Virtual Environment
```
source virtualenvironment/bin/activate
```

Install requirements using

```
pip install -r requirements.txt
```

Steps to install Postgress :-
```
1. sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib
2. sudo su - postgres
3. CREATE DATABASE social_login_django;
4. CREATE USER social_user WITH PASSWORD 'social';
5. ALTER ROLE social_user SET client_encoding TO 'utf8';
6. ALTER ROLE social_user SET default_transaction_isolation TO 'read committed';
7. GRANT ALL PRIVILEGES ON DATABASE social_login_django TO social_user;
8. \q
9. Exit

```
Run migrations

```
python manage.py makemigrations
python manage.py migrate
```


List Of API End Points for the project

Login
https://localhost:8000/login/

Set Password is possible after you have logged in through Oauth or at the sign up page you can give a new password
https://localhost:8000/update_pass/ 
THis API would need user password and email field to update

To get data of all user
https://localhost:8000/all_users/

To get data of single user
https://localhost:8000/single_user/<id>/
Eg https://localhost:8000/single_user/1/

To update phone number, 
https://localhost:8000/update_phone/
Enter phone number and email of the user 

To search a user through a phone number
https://localhost:8000/search_user/<phone>
Eg https://localhost:8000/search_user/+918100181913

To get details provided by oauth 
https://localhost:8000/get_socialdetails/<email_address>/
Eg https://localhost:8000/get_socialdetails/hassan.aarzoo@gmail.com/



