import os
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'default-bucket-name')
ENV = os.getenv("ENVIRONMENT", "local")