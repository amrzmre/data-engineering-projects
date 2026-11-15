import logging
import os
import subprocess
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def wait_for_postgres(host, dbname, user, max_retries=5, delay_seconds=5):
    """Wait for PostgreSQL to become available."""
    retries = 0
    while retries < max_retries:
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host, "-d", dbname, "-U", user],
                check=True, capture_output=True, text=True
            )
            if "accepting connections" in result.stdout:
                logger.info(f"Successfully connected to PostgreSQL at {host}!")
                return True
        except subprocess.CalledProcessError as e:
            retries += 1
            logger.warning(
                f"PostgreSQL at {host} not ready yet ({e}). "
                f"Retrying in {delay_seconds}s... (Attempt {retries}/{max_retries})"
            )
            time.sleep(delay_seconds)
    logger.error(f"Max retries reached waiting for {host}. Exiting.")
    return False


# Configuration for the source PostgreSQL database
source_config = {
    'dbname': os.environ.get('SOURCE_DB_NAME', 'source_db'),
    'user': os.environ.get('SOURCE_DB_USER', 'postgres'),
    'password': os.environ.get('SOURCE_DB_PASSWORD', 'secret'),
    'host': os.environ.get('SOURCE_DB_HOST', 'source_postgres'),
}

# Configuration for the destination PostgreSQL database
destination_config = {
    'dbname': os.environ.get('DEST_DB_NAME', 'destination_db'),
    'user': os.environ.get('DEST_DB_USER', 'postgres'),
    'password': os.environ.get('DEST_DB_PASSWORD', 'secret'),
    'host': os.environ.get('DEST_DB_HOST', 'destination_postgres'),
}

DUMP_FILE = "/tmp/data_dump.sql"

# Wait for both PostgreSQL databases before running the ELT process
if not wait_for_postgres(host=source_config['host'], dbname=source_config['dbname'], user=source_config['user']):
    exit(1)

if not wait_for_postgres(host=destination_config['host'], dbname=destination_config['dbname'], user=destination_config['user']):
    exit(1)

logger.info("Starting ELT script...")

# Use pg_dump to dump the source database to a SQL file.
# --clean --if-exists makes the dump safe to re-apply: it emits
# DROP ... IF EXISTS statements before each CREATE, so re-running
# this script doesn't fail on "relation already exists".
dump_command = [
    'pg_dump',
    '-h', source_config['host'],
    '-U', source_config['user'],
    '-d', source_config['dbname'],
    '--clean', '--if-exists',
    '-f', DUMP_FILE,
    '-w'
]
subprocess.run(dump_command, env={'PGPASSWORD': source_config['password']}, check=True)
logger.info(f"Dumped source database to {DUMP_FILE}")

# Use psql to load the dumped SQL file into the destination database
load_command = [
    'psql',
    '-h', destination_config['host'],
    '-U', destination_config['user'],
    '-d', destination_config['dbname'],
    '-a', '-f', DUMP_FILE
]
subprocess.run(load_command, env={'PGPASSWORD': destination_config['password']}, check=True)
logger.info("Loaded data into destination database")

logger.info("ELT script finished successfully.")