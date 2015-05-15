from app import app
app.debug = True
app.jinja_options = {'extensions': ['jinja2.ext.with_']}
app.run()
