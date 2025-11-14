import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Configurar logging más silencioso para producción
log_level = logging.WARNING if os.getenv('FLASK_ENV') == 'production' else logging.INFO
logging.basicConfig(level=log_level)
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.pool').setLevel(logging.WARNING)

MYSQL_URI = os.getenv('MYSQL_URI')
SQLITE_URI = 'sqlite:///product_local.db'
SCHEMA_SQL_PATH = os.path.join(os.path.dirname(__file__), '..', 'database.sql')


def get_engine():
    """
    Intenta crear una conexión con MySQL. Si falla, usa SQLite local.
    """
    is_production = os.getenv('FLASK_ENV') == 'production'
    echo_sql = False if is_production else True
    
    if MYSQL_URI:
        try:
            engine = create_engine(MYSQL_URI, echo=echo_sql)
            conn = engine.connect()
            conn.close()
            logging.info('Conexión a MySQL exitosa.')
            return engine
        except OperationalError:
            logging.warning('No se pudo conectar a MySQL. Usando SQLite local.')

    engine = create_engine(SQLITE_URI, echo=echo_sql)

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
        logging.info('Base de datos SQLite inicializada')

    return engine


engine = get_engine()
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


def get_db_session():
    return Session()