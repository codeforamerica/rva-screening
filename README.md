# rva-screening

### What

A prototype of an application that will allow safety net health services in Richmond, VA to share patients' financial screening information more easily. For more information, check out our [blog](http://rva.codeforamerica.org).

### Status

This project is in early development. We also discuss potential features and design decisions in the [rva-screening-ui-prototypes](https://github.com/codeforamerica/rva-screening-ui-prototypes) repo.

### Who

The [2015 Code for America Fellows in Richmond, VA](http://www.codeforamerica.org/governments/rva-community-partners/):

Ben Golder ([bengolder](//github.com/bengolder))
Emma Smithayer ([esmithayer](//github.com/esmithayer))
Sam Matthews ([mapsam](//github.com/mapsam))

### How (Installation)

The application is built with Python and [Flask](http://flask.pocoo.org/).

**Environment variables**
* `DATABASE_URL=[db connection string]` — For example, `postgresql://localhost/rva-screening`

**Install**
* Install a PostgreSQL database ([how to](https://github.com/codeforamerica/howto/blob/master/PostgreSQL.md))
* A [virtual environment](https://github.com/codeforamerica/howto/blob/master/Python-Virtualenv.md) will make it easier to manage dependencies.
* Clone the repo: ```git clone https://github.com/codeforamerica/rva-screening```
* Change into the project directory: ```cd rva-screening```
* Install Python requirements: ```pip install -r requirements.txt```
* Install front end requirements: ```npm install``` and `npm install gulp -g`
* Create two databases: 

```bash
createdb rva-screening
createdb rva-screening-test
```

* Add the HSTORE extension

```bash
psql rva-screening -c CREATE EXTENSION hstore;
psql rva-screening-test -c CREATE EXTENSION hstore;
```

* Set up the database: ```make new_db```
* Create mock data, including user accounts: ```make data```
* Start server: ```make run```
* After pulling down new code:

```bash
pip install -r requirements.txt
make db_update
```

**Testing**

To run the tests, you'll need a new database. By default, the code looks for a database called 'screener_test'. Set the TEST_DATABASE_URL environment variable if you choose a different name.

```bash
psql
create database screener_test
```

Run ```make test``` to run all the tests.

### Contribute

At this early stage, you should email us (the Richmond CfA Fellowship Team) if you're interested in helping with the project:
[richmond@codeforamerica.org](mailto:richmond@codeforamerica.org).