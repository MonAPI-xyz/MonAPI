## How to start development server
> Please adjust command `pip` and `python` accordingly to your machine (can be `pip3` or `python3`)
1. Install python virtualenv package if you don't have on local by running `python -m pip install virtualenv`
2. Create new virtual environment for this python project by running `virtualenv venv`
3. Activate python environment by running `venv\Scripts\activate` for Windows or  `source venv/bin/activate` for Mac and Linux
4. Clone this repository to your local machine
5. Change directory of CLI to project root folder
6. Copy `.env.example` file to `.env` on the project root folder
7. Run `pip install -r requirements.txt` to install all needed requirements for this project
8. Run database migrations by using `python manage.py migrate`
9. Run local server by using `python manage.py runserver`
10. You can access local server on http://localhost:8000 or http://127.0.0.1:8000

## How to run tests
1. You can run `python manage.py test` or using make command `make test`

## How to run test coverage report
1. You can run `make test-cover`
