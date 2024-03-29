# SE_Django_project

A Django Application for Group App.

### Application configuration guide 

1. Create database in mySQL and import data 
```bash
mysql -u root -p -e "CREATE DATABASE ipr_database_DEV;"
mysql -u root -p ipr_database_DEV < ipr_database_DEV_dump.sql
```

2. Configure a virtualenv 
```bash
python -m venv venv

# activate your virtual environment 
# linux / MacOS: 
source venv/bin/activate

# install required packages 
pip install -r requirements.txt
```

3. Create .env file in the root of the project and put your environmental variables there.
```

SECRET_KEY=secret key jakis (wpisz w google secret key django generator)
SQL_DB_NAME=ipr_database_DEV
SQL_DB_USER=root
SQL_DB_PASSWORD=haslo_do_serwera_sql
SQL_DB_HOST=localhost
```

5. Run the code (from the root of the project):
```
# run "run" file: 
bash run
```


5. If any migration in database is needed, run the code: 

```shell
#import env variables

# run "migrate" files
python manage.py migrate 
```

Enjoy! 
