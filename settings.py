# coding: UTF-8
import os
from dotenv import load_dotenv


load_dotenv()

SHARED_ACCESS_KEY_NAME = os.getenv('SHARED_ACCESS_KEY_NAME', None)
SHARED_ACCESS_KEY = os.getenv('SHARED_ACCESS_KEY', None)

if SHARED_ACCESS_KEY_NAME is None:
    print('Specify SHARED_ACCESS_KEY_NAME as environment variable.')
    os.sys.exit(1)
if SHARED_ACCESS_KEY is None:
    print('Specify SHARED_ACCESS_KEY as environment variable.')
    os.sys.exit(1)