# crawler test project

# Table of Contents

- [Description](#description)
- [Dependencies](#dependencies)
- [Deployment](#deployment)
- [Usage](#usage)

## description

a test crawler project to demonstrate crawling using python requests and beautifulsoup4 module.

## dependencies

- mysql-server == 5.5+
- python == 2.7
- virtualenvwrapper == 4.3.1-2 (optional, for creating virtual environments)

### required python packages

- beautifulsoup4==4.6.0
- PyMySQL==0.8.0
- requests==2.18.4
- SQLAlchemy==1.2.0
- ipdb==0.10.3

## deployment

make sure that python2.7 is installed on the target machine (Ubuntu machine),

- clone the repository on the local machine.
- install mysql-server package and set the user and password with required access.

```sh
sudo apt-get install mysql-server
```

- switch to your python virtual environment, go to your project directory and run below
command for python packages instllation, for next steps, make sure you are executing
commands in your virtual environment.

```sh
pip install -r requirements.txt
```

- get inside the project root directory and go to crawlers/lib/settings.py and set database variables mentioned below as per your environment. Dont touch the MYSQL_CHARSET variable, it is important for resolving unicode issues in crawled data.

```python
# mysql database params
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'XXXX'
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_DB = 'crawler_db'
```

- log into mysql server and create the database with the name as per you set in the previous step.

```sql
create database <databasename>;
```

- while in the project directory, go to /crawlers/lib and run below command
which will take care of creating required database tables.

```sh
python models.py
```

- to ensure that there are no unicode errors while storing data in mysql db, switch
to project directory and run /crawlers/change_charset.sql against your mysql server like
below.

```sh
mysql -u <user> -D <database> -p < crawlers/change_charset.sql
```

- all setup, the crawler is now deployed.

## usage

Go inside the project directory, switch to /crawlers directory and run below command, make
sure you are inside your virtual environment of python.

```sh
python indeed_crawler.py
```
The crawling should have started and would be running flawlessly.
