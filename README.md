# Cat API
Cat is an API written in python using fastAPI. It performs crud operations on cat breeds.
Working sample [Cat API](https://cat.jcvic.com)

## Usage
- Without Docker
    * Create a virtual environment.
    * Install all requirements in ```requirements.txt```.
    * Create a ```.env``` in root folder if not available and set a valid postgres url to ```DATABASE_URL```.
    * Example ```DATABASE_URL=postgresql+asyncpg://user:password@app_db:5432/app_db```,
       Note that database is async.
    * Run migrations (alembic) using
    * ```alembic revision --autogenerate -m "initial"```
       ```alembic upgrade head```
    * Finally execute ```uvicorn app.main:app``` to start application or pytest to start test.
- With Docker
    * Run docker ```compose up --build``` to start both test and application.
    * Run docker ```compose up --build web``` to start only application.
    * Run docker ```compose up --build test``` to start only test.

* Run ```python3 generate_data.py``` to generate sql test data file
## Documentation
Detailed documentation of API can be accessed using swagger by going to ```/docs``` on respective domain.
