import socket
import psycopg2
from psycopg2 import pool
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
import os

load_dotenv()

# Determina o ambiente de execução e configura o logging apropriadamente
hostname = socket.getfqdn()
if "bayer.cnb" in hostname:
    # Ambiente local: configura o logging para salvar em um arquivo na pasta local
    log_filename = 'database_operations.log'
    handler = RotatingFileHandler(log_filename, maxBytes=10000000, backupCount=3)
elif "ec2.internal" in hostname:
    # Ambiente EC2: configura o logging para enviar para o AWS S3
    log_filename = 'database_operations.log'  # O nome do arquivo a ser enviado para o S3
    handler = RotatingFileHandler(log_filename, maxBytes=10000000, backupCount=3)  # Um handler genérico como placeholder
else:
    raise EnvironmentError("Unknown execution environment")

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[handler]
)

logger = logging.getLogger(__name__)

class DatabaseConnector:
    """
    DatabaseConnector is a class that provides connections to a PostgreSQL database
    with separate endpoints for read and write operations.
    """

    def __init__(self, minconn=1, maxconn=10):
        """
        Initializes the DatabaseConnector instance with separate read and write connection pool.
        """
        self.database = os.getenv('DATABASE')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('PASSWORD')
        self.read_host, self.read_port = self._determine_host_and_port(read=True)
        self.write_host, self.write_port = self._determine_host_and_port(read=False)
        self.minconn = minconn
        self.maxconn = maxconn
        self.read_connection_pool = self._create_connection_pool(self.read_host, self.read_port)
        self.write_connection_pool = self._create_connection_pool(self.write_host, self.write_port)

    def _determine_host_and_port(self, read):
        """
        Determines the appropriate database host and port based on the execution environment and operation type.
        """
        hostname = socket.getfqdn()
        if "bayer.cnb" in hostname:
            return (os.getenv('READ_HOST_LOCAL'), os.getenv('LOCAL_PORT')) if read else (os.getenv('WRITE_HOST_LOCAL'), os.getenv('LOCAL_PORT'))
        elif "ec2.internal" in hostname:
            return (os.getenv('READ_HOST_EC2'), os.getenv('EC2_PORT')) if read else (os.getenv('WRITE_HOST_EC2'), os.getenv('EC2_PORT'))
        else:
            raise EnvironmentError("Unknown execution environment")

    def _create_connection_pool(self, host, port):
        """
        Creates a pool of database connections for the given host and port.
        """
        return psycopg2.pool.SimpleConnectionPool(
            self.minconn,
            self.maxconn,
            database=self.database,
            user=self.user,
            password=self.password,
            host=host,
            port=port
        )

    def execute_query(self, query, params=None, user="Unknown"):
        """
        Executes a database query using the read connection pool and returns the results.
        """
        with self.get_connection(read=True) as connection:
            try:
                with connection.cursor() as cursor:
                    logger.info(f"User '{user}' is executing query: {query}")
                    cursor.execute(query, params)
                    results = cursor.fetchall()
                    return results
            except Exception as e:
                logger.error(f"User '{user}' encountered an error while executing the query: {e}")
                return None

    def execute_update(self, query, params=None, user="Unknown"):
        """
        Executes an update, insert, or delete query using the write connection pool.
        """
        with self.get_connection(read=False) as connection:
            try:
                with connection.cursor() as cursor:
                    logger.info(f"User '{user}' is executing update: {query}")
                    cursor.execute(query, params)
                    connection.commit()
            except Exception as e:
                connection.rollback()
                logger.error(f"User '{user}' encountered an error while executing the update: {e}")

    def get_connection(self, read=True):
        """
        Gets a connection from the appropriate connection pool based on the operation type.
        """
        return self.read_connection_pool.getconn() if read else self.write_connection_pool.getconn()

    def release_connection(self, connection, read=True):
        """
        Releases a connection back to the appropriate connection pool.
        """
        if read:
            self.read_connection_pool.putconn(connection)
        else:
            self.write_connection_pool.putconn(connection)

    def close_all_connections(self):
        """
        Closes all connections in both the read and write connection pools.
        """
        self.read_connection_pool.closeall()
        self.write_connection_pool.closeall()

# Usage example:
# database_connector = DatabaseConnector(database="yourdbname", user="yourdbuser", password="yourdbpassword", port="5432")
# query = "SELECT * FROM your_table"
# results = database_connector.execute_query(query, user="john_doe")
# for row in results:
#     print(row)
# database_connector.close_all_connections()



