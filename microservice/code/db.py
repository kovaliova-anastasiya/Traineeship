from pathlib import Path
import os
from dotenv import load_dotenv
import boto3
from boto3.resources.base import ServiceResource

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION')


def initialize_db() -> ServiceResource:
    ddb = boto3.resource('dynamodb')
    return ddb
