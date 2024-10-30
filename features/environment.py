import logging
from utils.auth import get_bearer_token
from dotenv import load_dotenv
from behave import use_fixture
import os
import json


# Configure logging
logger = logging.getLogger(__name__)

def before_all(context):
    load_dotenv()
    BASE_URL=os.getenv('BASE_URL')
    context.base_url=BASE_URL
    print(f"{context.base_url}")    
    # Initialize token and headers
    context.api_endpoint = f"{context.base_url}"
    print(f"{context.api_endpoint}")
    context.token = get_bearer_token()
    context.headers = {
        "Authorization": f"Bearer {context.token}",
        "Content-Type": "application/json"
    }
    if context.token != '':
        logging.info("token is generated")
    else:
        logging.info("token cannot be generated")

def before_tag(context, tag):
    if tag == "cartId_needed":
        use_fixture(context, timeout=10)