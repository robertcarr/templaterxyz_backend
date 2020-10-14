import sys
import os
import logging

import MySQLdb
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import environ

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

env = environ.Env()
env.read_env(os.path.join(settings.BASE_DIR, '.env'))
db_conf = env.db()


class Command(BaseCommand):
    TIMEOUT = 5
    help = 'Manage Remote Database (e.g. Zappa/Lambda)'

    def add_arguments(self, parser):
        parser.add_argument('-s', '--show', action='store_true', default=False,
                            help='Show all databases SHOW ALL DATABASES')
        parser.add_argument('-i', '--init', action='store_true', help='CREATE Database and GRANT permissions')
        parser.add_argument('-c', '--command', nargs='+', type=str, help='Run SQL command on remote database server')
        parser.add_argument('-d', '--database', type=str, help="Remote Database to work with")

    def run_command(self, cmd, db=None):
        """ run command on remote db """
        try:
            logger.info(f"cmd: {cmd}")
            db = self._connect_to_db()
            c = db.cursor()
            c.execute(cmd)
            logger.info(c.fetchall())
            c.close()
        except Exception as e:
            logger.error(f"Error {e}")

    def init_db(self):
        """ initialize the database and grant any permissions """
        try:
            db = self._connect_to_db()
            c = db.cursor()
            logger.debug(f"Creating Database {db_conf['NAME']}")
            c.execute(f"CREATE DATABASE {db_conf['NAME']};")
            logger.info(c.fetchall())
            logger.info(f"Granting to {db_conf['USER']} on database {db_conf['NAME']}")
            c.execute(f"GRANT ALL PRIVILEGES ON {db_conf['NAME']}.* TO '{db_conf['USER']}' IDENTIFIED BY '{db_conf['PASSWORD']}';")
            logger.info(c.fetchall())
            c.close()
            logger.info('database closed')
        except Exception as e:
            logger.error(f"Error {e}")
            sys.exit()

    def show_databases(self):
        """ show all databases """
        try:
            logger.info("Show all databases")
            db = self._connect_to_db()
            c = db.cursor()
            c.execute('SHOW DATABASES;')
            logger.info(c.fetchall())
            c.close()
        except Exception as e:
            logger.error(f"Error: {e}")

    def _connect_to_db(self):
        """Connect and return db handle & optionally a specific database"""
        print(self._db)
        try:
            logger.info(f"Connecting to [{db_conf['NAME']}]")
            logger.info(f"Host to [{db_conf['HOST']}]")
            options = dict({'host': db_conf['HOST'],
                            'user': db_conf['USER'],
                            'password': db_conf['PASSWORD']})
            if self._db:
                options['db'] = self._db
            dbh = MySQLdb.connect(**options)
            #db = MySQLdb.connect(host=db_conf['HOST'],
            #                     user=db_conf['USER'],
            #                     password=db_conf['PASSWORD'],
            #                     connect_timeout=self.TIMEOUT)
            logger.info("connected to db")
            return dbh
        except Exception as e:
            logger.error(f"Error connecting to db [{db_conf['NAME']}: error: {e}")
            sys.exit()

    def handle(self, *args, **kwargs):
        if kwargs['database']:
            self._db = kwargs['database']

        if kwargs['init']:
            self.init_db()
            return
        if kwargs['show']:
            self.show_databases()
            return
        if kwargs['command']:
            cmd = ' '.join(list(kwargs['command']))
            self.run_command(cmd)
            return
