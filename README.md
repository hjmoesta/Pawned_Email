# PAWNED EMAIL

## Description
This is a Django project that is used to figure out what accounts associated with the given email have been breached. Using the haveibeenpwned [api](https://haveibeenpwned.com/API/v2). With an API key and the email, the api is able to recieve a json file that contains the names of the companies that have been breached.

## User Usage
There are two types of pages where the user is asked for input. There is a signup page which is located at tester/signup.html. This page prompts a new user to provide an email and a password. With this, the email and password are logged into a sqlite local database, and there is a new database created with the username of the email. For example, if someone signed up with the information
```bash
email: example@gmail.com
password: passwordexample123
```
then in the local database called wifi_login under the users table, the email and passsword will be logged. Simultaniously there will be a new sqlite table created with the name example which stores the companies that have been breached under that username.

The other option is to login. What this does is checks the user table to see if the provided username and password exist. If they do then the user is taken to the conent page which displays the information from the associated sqlite table. The companys are stored in a table so that whenever someone logs in, we do not need to ping the api again for the same content, instead, the content is saved. 

## Installation
In order to install this, download this repository into your mysite under a folder titled tester. If you wish to change the name of the folder ensure that you change the name in the mysite/url and project_name/url. Next you will need to get a API key. To do so navigate to the [api key](https://haveibeenpwned.com/API/Key) page and provide information. Once you have a key, store the key in a file called api_key.py as api_key. If you want to change this feel free change the structure.