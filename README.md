# Python Trading Bot Web App Server

## Description

- This program was created as a REST API server to support a [web app](https://github.com/TreyThomas93/tos-python-bot-web-app) that displays information gathered through the [Python Trading Bot w/ Thinkorswim](https://github.com/TreyThomas93/python-trading-bot-with-thinkorswim) program.

- Program uses JSON Web Token for the authentication process.

## How it works

1. This program is meant to be used in conjunction with the [Python Trading Bot w/ Thinkorswim](https://github.com/TreyThomas93/python-trading-bot-with-thinkorswim) program and this [web app](https://github.com/TreyThomas93/tos-python-bot-web-app).

2. If you have not set up the trading bot yet, I suggest you do that first.

3. If you have set up the program and are good to go, then the next step is to add an .env file to the assets directory. This .env file will contain the MONGO_URI that you stored in the trading bot .env file.

4. After that, you will need to generate an encrypted password. Go into the generate_password.py file located in the root directory and follow the steps.

5. After you generate a hashed password, you will need to store it in your user object in the Password field located in mongo. View image below on the user object structure and setup.

![User Object Structure](assets/img/user.png)

- _These field names are case sensitive and must be verbatim._

6. This hashed password will be used by this program as a secret key and will be used by the web app for login credentials.

7. While you are at it, go ahead and create a username and store it into the Username field in mongo aswell.

8. After that, run the program to check for errors. If no errors, then your server is ready. Now all you have to do is setup the [web app](https://github.com/TreyThomas93/tos-python-bot-web-app).

## Code Counter

Total : 14 files, 923 codes, 37 comments, 339 blanks, all 1299 lines

## Languages

| language | files | code | comment | blank | total |
| :------- | ----: | ---: | ------: | ----: | ----: |
| JSON     |     1 |  474 |       0 |     1 |   475 |
| Python   |    11 |  416 |      37 |   318 |   771 |
| toml     |     1 |   18 |       0 |     4 |    22 |
| Markdown |     1 |   15 |       0 |    16 |    31 |

## Directories

| path          | files | code | comment | blank | total |
| :------------ | ----: | ---: | ------: | ----: | ----: |
| .             |    14 |  923 |      37 |   339 | 1,299 |
| api           |     3 |  279 |      23 |   209 |   511 |
| assets        |     3 |   41 |       6 |    40 |    87 |
| assets\logger |     1 |   35 |       6 |    33 |    74 |
| auth          |     2 |   59 |       0 |    39 |    98 |
| extensions    |     1 |    4 |       0 |     3 |     7 |

