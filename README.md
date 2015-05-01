# rva-screening

### What

A repository of early prototyping and design ideas for an application that would allow safety net health services in Richmond, VA to share income verification screening.

### Status

This project is in an early design stage. In addition to code, it contains issues used to discuss potential features and links to documentation of the design process.

### Why

Assumptions that led to this app idea:

* Financial eligibilty screening is done redundantly for a given patient who applies to multiple safety net services.
* Financial eligibility screening is a significant source of delay between the time a patient is referred to a safety net health service and the time of their first treatment.
* Creating a more standardized process for financial elgibility will help clients and case managers to more easily discover services that a client would be eligible for.
* Reducing the time spent on financial eligibility screening would be helpful to clients as well as safety-net service providers.

### Who

The [2015 Code for America Fellows working in Richmond, VA with RVA Community Partners](http://www.codeforamerica.org/governments/rva-community-partners/):

Ben Golder ([bengolder](//github.com/bengolder))  
Emma Smithayer ([esmithayer](//github.com/esmithayer))  
Sam Matthews ([svamatthews](//github.com/svmatthews))  

### How (Installation)

**Site & Server (Flask)**
* Install MySQL (http://dev.mysql.com/downloads/mysql/) and start your server.
* Set the root MySQL password to "password": ```mysqladmin -u root -p “password”```
* Create a database called rva_screening.
* Install requirements: ```pip install -r requirements.txt```
* Create migrations folder: ```python db.py db init```
* Create migration based on current models: ```python db.py db migrate```
* Apply migration to database: ```python db.py db upgrade```
* Create a user account for login: ```python add_user.py```
* Start server: ```python run.py```

After pulling down new code:

```pip install -r requirements.txt```

```python db.py db migrate```

```python db.py db upgrade```

**Assets**

All assets build from `app/static/` using Flask-Assets and webassets. They are bundled into `public/` and retrieved on page loads.

The front-end currently depends on some 3rd party assets. To install these, use `npm`:

```
cd ./app/static/
npm install
```

### Contribute

In this early stage, you should email us (the Richmond CfA Fellows Team) if you're interested in helping with the project:
[richmond@codeforamerica.org](mailto:richmond@codeforamerica.org).

