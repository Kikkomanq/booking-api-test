import requests
import random
import string
import logging
from behave import given, when, then
from utils.json_loader import load_json

logger = logging.getLogger(__name__)

@given('I set GET method for tours endpoint')
def step_impl(context):
    context.api_endpoint = f"{context.base_url}/v1/tours"


@when('I send GET HTTP request')
def step_impl(context):
    context.response = requests.get(context.api_endpoint, headers=context.headers)

@then('The search response status should be {status_code:d}')
def step_then(context, status_code):
    assert context.response.status_code == status_code, f"Expected status {status_code}, got {context.response.status_code}"

@then('There should be available tours for booking')
def step_impl(context):
    response_json = context.response.json()
    paging_data = response_json["paging"]
    assert paging_data["totalElements"] >= 4, "There is no Available Tours for booking, or less then expected"

@given('I get the results of tours endpoint')
def step_given(context):
    context.api_endpoint = f"{context.base_url}/v1/tours"
    context.response = requests.get(context.api_endpoint, headers=context.headers)
    assert context.response.status_code == 200, f"Expected status 200, got {context.response.status_code}"

@when('I get the tour ID and Option ID')
def step_when(context):
    response_json = context.response.json()
    tour_id = response_json["tours"][0]["id"]
    option_id = response_json["tours"][0]["options"][0]["id"]
    shoppingCartReference=response_json["tours"][0]["options"][0]["departures"][0]["shoppingCartReference"]
    context.tour_id = tour_id
    context.options_ids = option_id
    context.shoppingCartReference=shoppingCartReference

@when('I send tour ID and Option ID')
def step_when(context):
    tour_id = context.tour_id
    options_id = context.options_ids
    context.api_endpoint = f"{context.base_url}/v1/tours/{tour_id}/options/{options_id}"
    context.response = requests.get(context.api_endpoint, headers=context.headers)
    assert context.response.status_code == 200, f"Expected status 200, got {context.response.status_code}"
    # assert shopping cart is not empty

@then('ShoppingCartReference is generated')
def step_impl(context):
    response_json=context.response.json()
    shoppingCartReference=response_json["departures"][0]["optionalServices"][0]["shoppingCartReference"]
    assert shoppingCartReference != "", "shoppingCartReference is empty"

@given('optionalServices and ShoppingCartReference is generated')
def step_impl(context):
    context.api_endpoint = f"{context.base_url}/v1/tours"
    context.response = requests.get(context.api_endpoint, headers=context.headers)
    response_json=context.response.json()
    tour_id = response_json["tours"][0]["id"]
    option_id = response_json["tours"][0]["options"][0]["id"]
    context.api_endpoint = f"{context.base_url}/v1/tours/{tour_id}/options/{option_id}"
    context.response = requests.get(context.api_endpoint, headers=context.headers)
    response_json=context.response.json()
    context.shoppingCartReference=response_json["departures"][0]["shoppingCartReference"]
    assert context.shoppingCartReference != "", "shoppingCartReference is empty"


@when('I send booking refereference to cart endpoint')
def step_when(context):
    context.api_endpoint = f"{context.base_url}/v1/carts"
    payload = {
        "items": [
            {
                "reference": context.shoppingCartReference
            }
        ]
    }
    context.response = requests.post(context.api_endpoint, headers=context.headers, json=payload)
    assert context.response.status_code == 201, f"Expected status 201, got {context.response.status_code}"

@then('Id with booking cart will be generated')
def step_then(context):
    response_json = context.response.json()
    assert response_json['id'].strip() != "", "id is empty"

    
@given('I recieved booking reference from selected tour')
def step_given(context):
    context.api_endpoint = f"{context.base_url}/v1/carts"
    context.response = requests.get(context.api_endpoint, headers=context.headers)
    assert context.response.status_code == 200, f"Expected status 200, got {context.response.status_code}"

@given('Cart Id is present')
def step_given(context):   
    context.api_endpoint = f"{context.base_url}/v1/carts"
    payload = load_json('../data/cartReference.json')
    context.response = requests.post(context.api_endpoint, headers=context.headers, json=payload)
    assert context.response.status_code == 201, f"Expected status 201, got {context.response.status_code}"
    response_json = context.response.json()
    context.cart_id=response_json['id'].strip()
    assert response_json['id'].strip() != "", "id is empty"

@when('I send cart Id to check endpoint')
def step_when(context):
    cart_id=context.cart_id
    context.api_endpoint = f"{context.base_url}/v1/carts/{cart_id}/check"
    context.response = requests.post(context.api_endpoint, headers=context.headers)
    assert context.response.status_code == 200, f"Expected status 200, got {context.response.status_code}"

@then('Selected Tour should be available for booking with message "{text}"')
def step_then(context, text):
    response_json = context.response.json()
    code=response_json['items'][0]['status']['code']
    message_json=response_json['items'][0]['status']['message']
    assert code=='BOOKABLE', "Tour is not bookable"
    assert message_json==text, "Message is not correct"

@when('I send cart Id to reserve endpoint')
def step_when(context):
    cart_id=context.cart_id
    context.api_endpoint = f"{context.base_url}/v1/carts/{cart_id}/reserve"
    context.response = requests.post(context.api_endpoint, headers=context.headers)
    assert context.response.status_code == 200, f"Expected status 200, got {context.response.status_code}"

@when('I send valid payload so to make booking')
def step_when(context):
    cart_id=context.cart_id
    context.api_endpoint = f"{context.base_url}/v1/carts/{cart_id}/reserve"
    context.response = requests.post(context.api_endpoint, headers=context.headers)
    context.api_endpoint = f"{context.base_url}/v1/carts/{cart_id}/book"
    # booking payload saved in seperate file
    # TODO
    # Create payload generator with fake and variable data
    # payload=context.bookingPayload

    payload = {
        "customer": {
            "title": "Mr.",
            "firstName": "Tony",
            "lastName": "Stark",
            "middleName": "Edward",
            "email": "tony.stark@starkindustries.com",
            "contactNumber": "+1 (555) 987-6543",
            "address": {
                "countryCode": "US",
                "state": "California",
                "city": "Malibu",
                "streetName": "Malibu Point",
                "streetNumber": "10880",
                "postalCode": "90265"
            }
        },
        "payment": {
            "price": {
                "amount": 153.4,
                "currencyCode": "USD"
            },
            "formOfPayment": "Credit card",
            "externalIdentifier": ''.join(random.choices(string.digits, k=23))
        },
        "note": "Very special booking requirements",
        "status": "Confirmed",
        "additionalInformation": {
            "customInfoParameter1": "custom value 1",
            "customInfoParameter2": "custom value 2",
            "customInfoParameter3": "custom value 3"
        }
    }

    context.response = requests.post(context.api_endpoint, headers=context.headers, json=payload)

@then('Selected Tour should be reserved with message "{text}"')
def step_then(context, text):
    response_json = context.response.json()
    code=response_json['items'][0]['status']['code']
    message_json=response_json['items'][0]['status']['message']
    assert code=='RESERVED', "Tour is not bookable"
    assert message_json==text, "Message is not correct"
   
@then('A unique booking identifier is returned that can be used for further booking amends')
def step_then(context):
    response_json = context.response.json()
    assert context.response.status_code == 201, f"Expected status 201, got {context.response.status_code}"
    logger.info(f"{response_json}")
    bookingId=response_json['bookingId'].strip() 
    context.bookingId=bookingId
    print(f"bookingid={bookingId}")
    assert response_json['bookingId'].strip() != "", "bookingId is empty"
    assert response_json['bookingCode'].strip() != "", "bookingCode is empty"

@when('I send invalid payload so to make booking')
def step_when(context):
    cart_id=context.cart_id
    context.api_endpoint = f"{context.base_url}/v1/carts/{cart_id}/reserve"
    context.response = requests.post(context.api_endpoint, headers=context.headers)
    context.api_endpoint = f"{context.base_url}/v1/carts/{cart_id}/book"
    # booking payload saved in seperate file
    # TODO
    # Create payload generator with fake and variable data
    # payload=context.bookingPayload

    payload =  load_json('../data/booking_payload.json')
    context.response = requests.post(context.api_endpoint, headers=context.headers, json=payload)

@then('Booking cant be made because externalIdentifier is already used')
def step_then(context):
    assert context.response.status_code == 400, f"Expected status 400, got {context.response.status_code}"  
    
@then('A booking endpoint returnes valid status code')
def step_then(context):
    print(context.bookingId)
    context.api_endpoint = f"{context.base_url}/v1/bookings/{context.bookingId}"
    context.response = requests.get(context.api_endpoint, headers=context.headers)

@then('Booking data is returned')
def step_when(context):
    response_json = context.response.json()
    assert context.response.status_code == 200, f"Expected status 200, got {context.response.status_code}"      
    assert response_json['customer']["email"]=="tony.stark@starkindustries.com", f"customer email is not returned"