import os

from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

DATABASE_URL = os.getenv("DATABASE_URL")

RABBIT_HOST = os.getenv("RABBIT_HOST")
RABBIT_PORT = os.getenv("RABBIT_PORT")
RABBIT_EXCHANGE = os.getenv("RABBIT_EXCHANGE")
RABBIT_QUEUE = os.getenv("RABBIT_QUEUE")
RABBIT_ROUTING_KEY = os.getenv("RABBIT_ROUTING_KEY")
