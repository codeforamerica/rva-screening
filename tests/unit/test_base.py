from app import create_app as _create_app
from app import db
from config import TestConfig
from flask_testing import TestCase
from sqlalchemy.engine import reflection
from sqlalchemy.schema import (
    MetaData,
    Table,
    DropTable,
    ForeignKeyConstraint,
    DropConstraint,
)

class BaseTestCase(TestCase):

  def create_app(self):
    return _create_app(config=TestConfig)

  def setUp(self):
    db.create_all()

  def tearDown(self):
    db.session.remove()

    # Replacement for db.session.drop_all()
    # http://www.mbeckler.org/blog/?p=218
    engine = db.get_engine(self.app)
    conn = engine.connect()
    trans = conn.begin()
    inspector = reflection.Inspector.from_engine(engine)
    metadata = MetaData()

    tbs = []
    all_fks = []

    for table_name in inspector.get_table_names():
        fks = []
        for fk in inspector.get_foreign_keys(table_name):
            if not fk['name']:
                continue
            fks.append(
                ForeignKeyConstraint((),(),name=fk['name'])
                )
        t = Table(table_name,metadata,*fks)
        tbs.append(t)
        all_fks.extend(fks)

    for fkc in all_fks:
        conn.execute(DropConstraint(fkc))

    for table in tbs:
        conn.execute(DropTable(table))

    trans.commit()

    engine.dispose()

  def login(self, email='richmond@codeforamerica.org', password='password'):
    return self.client.post('/login', data=dict(
      email=email,
      password=password
    ), follow_redirects=True)

  def logout(self):
    return self.client.get('/logout', follow_redirects=True)


