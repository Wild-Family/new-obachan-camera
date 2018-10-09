# coding: UTF-8
import os
from dotenv import load_dotenv


load_dotenv()

GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', None)

if GOOGLE_APPLICATION_CREDENTIALS is None:
    print('Specify GOOGLE_APPLICATION_CREDENTIALS as environment variable.')
    os.sys.exit(1)

SHARED_ACCESS_KEY_NAME = os.getenv('SHARED_ACCESS_KEY_NAME', None)
SHARED_ACCESS_KEY = os.getenv('SHARED_ACCESS_KEY', None)

if SHARED_ACCESS_KEY_NAME is None:
    print('Specify SHARED_ACCESS_KEY_NAME as environment variable.')
    os.sys.exit(1)
if SHARED_ACCESS_KEY is None:
    print('Specify SHARED_ACCESS_KEY as environment variable.')
    os.sys.exit(1)

AITALK_USERNAME = os.getenv("AITALK_USERNAME", None)
AITALK_PASSWORD = os.getenv("AITALK_PASSWORD", None)

if AITALK_USERNAME is None:
    print('Specify AITALK_USERNAME as environment variable.')
    os.sys.exit(1)
if AITALK_PASSWORD is None:
    print('Specify AITALK_PASSWORD as environment variable.')
    os.sys.exit(1)