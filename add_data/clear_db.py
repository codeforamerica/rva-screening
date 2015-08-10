#!/usr/bin/env python
import sys
import os
import subprocess

from flask import current_app
from contextlib import closing
from sqlalchemy.engine import reflection
from sqlalchemy.schema import (
    MetaData,
    Table,
    DropTable,
    ForeignKeyConstraint,
    DropConstraint,
)

from app import create_app, db

# Clear the database by deleting all tables and recreating them
# Exception: don't clear the alembic_version table--that messes
# up the migration history.
def main(app=create_app(), options=[]):

  with app.app_context():

    engine = db.get_engine(app)
    conn = engine.connect()
    trans = conn.begin()
    inspector = reflection.Inspector.from_engine(engine)
    metadata = MetaData()

    tbs = []
    all_fks = []

    for table_name in inspector.get_table_names():
      if table_name != 'alembic_version':
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
    db.create_all()
    engine.dispose()

    # Audit triggers aren't in SQLAlchemy schema definition, so create_all
    # won't recreate them. Run the separate script to add them.
    if '-local' in options:
      os.system('psql -d {} -a -f app/audit_triggers.sql'.format(engine.url.database))

    print "Deleted all existing data"

if __name__ == '__main__':
  sys.exit(main(create_app(), sys.argv[1:]))
