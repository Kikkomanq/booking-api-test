import logging
from utils.auth import get_bearer_token
import os
import json
from dotenv import load_dotenv


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    handlers=[
        logging.FileHandler("api_info.log"),
        logging.StreamHandler()
    ]
)

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

    # read json load for booking passangers
    script_dir = os.path.dirname(__file__)
    rel_path = '../data/booking_payload.json'
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, 'r', encoding='utf-8') as json_file:
        context.bookingPayload = json.load(json_file)
