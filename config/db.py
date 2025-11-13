import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base

Base = declarative_base()

logging.basicConfig(level=logging.INFO)

MYSQL_URI = os.getenv('MYSQL_URI')
SQLITE_URI = 'sqlite:///product_local.db'
SCHEMA_SQL_PATH = os.path.join(os.path.dirname(__file__), '..', 'database.sql')


def get_engine():
    """
    Intenta crear una conexión con MySQL. Si falla, usa SQLite local.
    """
    if MYSQL_URI:
        try:
            engine = create_engine(MYSQL_URI, echo=True)
            conn = engine.connect()
            conn.close()
            logging.info('Conexión a MySQL exitosa.')
            return engine
        except OperationalError:
            logging.warning('No se pudo conectar a MySQL. Usando SQLite local.')

    engine = create_engine(SQLITE_URI, echo=True)

    """ Ejecutar el SQL del archivo database.sql """
    if os.path.exists(SCHEMA_SQL_PATH):
        with open(SCHEMA_SQL_PATH, 'r', encoding='utf-8') as f:
            sql_commands = f.read()
        with engine.connect() as conn:
            for command in sql_commands.split(';'):
                cmd = command.strip()
                if cmd:
                    conn.execute(text(cmd))
            conn.commit()
        logging.info('Base de datos SQLite inicializada con datos de database.sql')

    return engine


engine = get_engine()
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


def get_db_session():
    return Session()