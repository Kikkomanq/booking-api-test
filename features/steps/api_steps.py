from behave import given, when, then
import requests
import random
import string


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
    assert tour_id=="513b4fd0-40b3-414e-9824-abc4d662187a", "The ID of the selected tour is not valid"
    assert option_id=="234cdbb9-fad2-4a84-9725-d85aafe68923"
    context.tour_id = tour_id
    context.options_ids = option_id
    context.shoppingCartReference=shoppingCartReference

@then('I send tour ID and Option ID')
def step_then(context):
    tour_id = context.tour_id
    options_id = context.options_ids
    context.api_endpoint = f"{context.base_url}/v1/tours/{tour_id}/options/{options_id}"
    context.response = requests.get(context.api_endpoint, headers=context.headers)
    assert context.response.status_code == 200, f"Expected status 200, got {context.response.status_code}"
    # assert shopping cart is not empty

@then('optionalServices and ShoppingCartReference is generated')
def step_impl(context):
    response_json=context.response.json()
    shoppingCartReference=response_json["departures"][0]["optionalServices"][0]["shoppingCartReference"]
    assert shoppingCartReference != "", "shoppingCartReference is empty"

@given('optionalServices and ShoppingCartReference is generated')
def step_impl(context):
    tour_id="7c629e71-bcfd-450e-92bf-fac36fb6792a"
    option_id="9216f916-0d09-456d-9d5b-fdf86a40b512"
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
    payload = {
        "items": [
            {
                "reference": "eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJ5IjowLCJwIjoiSGlyaW5nIiwidCI6IjdjNjI5ZTcxLWJjZmQtNDUwZS05MmJmLWZhYzM2ZmI2NzkyYSIsIm8iOiI5MjE2ZjkxNi0wZDA5LTQ1NmQtOWQ1Yi1mZGY4NmE0MGI1MTIiLCJkYyI6IjI3MjgiLCJkIjo2Mzg5NTk5NjgwMDAwMDAwMDAsImMiOiJVU0QiLCJuIjoxLCJhIjpbXSwiciI6IjE3NTAiLCJkaSI6IjJkMzYxYmZlLWVjNmMtNDI5OS1hOWMwLWVkMThkNWVkMmFkMiIsImRzYyI6bnVsbH0."
            }
        ]
    }
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
    assert response_json['bookingId'].strip() != "", "bookingId is empty"
    assert response_json['bookingCode'].strip() != "", "bookingCode is empty"

@then('Booking cant be made because externalIdentifier is already used')
def step_then(context):
    assert context.response.status_code == 201, f"Expected status 201, got {context.response.status_code}"