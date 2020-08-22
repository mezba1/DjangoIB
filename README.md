# DjangoIB

Image-based bulletin board.

## Getting started

### Prerequisites

- Python (3.8)
- Node.js (12.16) and Yarn
- Imgur API Client ([register here](https://api.imgur.com/oauth2/addclient))

Clone the repository:

```
git clone https://github.com/mezba1/DjangoIB.git
cd DjangoIB
```

Install requirements:

```
pip install -r requirements.txt
yarn install
```

Build assets:

```
yarn build
```

### Configuration

Create _.env_ file:

```js
touch .env

// or

cp .env.sample .env
```

Following configuration variables can be set with ```.env```:

| Variable        | Description | Default  |
| :--- | :---: | ---:|
| ```ADMIN_INITIAL_PASSWORD``` | Password for initial admin account, will be used during installation. | ```admin``` |
| ```ALLOWED_HOSTS``` | Comma separated list of strings representing the host/domain names that DjangoIB can serve ([more](https://docs.djangoproject.com/en/3.0/ref/settings/#allowed-hosts)). | Empty |
| ```APP_NAME``` | Name of the app. | ```DjangoIB``` |
| ```APP_LOGO``` | Image shown at the top of index page. | [```djangoib_logo.png```](src/static/images/djangoib_logo.png) |
| ```DATABASE_URL``` | Database connection url. | ```sqlite:///db.sqlite3``` |
| ```IMGUR_CLIENT_ID``` | Imgur client id. | Empty |
| ```PY_ENV``` | Specifies the environment in which DjangoIB is running such as ```development```, ```staging``` and ```production```. | ```development``` |
| ```SECRET_KEY``` | Secret key ([more](https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-SECRET_KEY)). | ```djangoib-secret``` |

Initialize:

```
python src/manage.py migrate
python src/manage.py initadmin
```

### Run

```
python src/manage.py runserver
```

Open [http://localhost:8000](http://localhost:8000/) in your browser to see the board.
Navigate to [http://localhost:8000/admin](http://localhost:8000/admin/) to access the admin panel.

## Demo

Want to see DjangoIB in action? [Click me](https://topiary.herokuapp.com/).

Alternatively, you can deploy your own copy of DjangoIB on Heroku using this button:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
