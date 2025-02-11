import json
import uuid
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('donor_registrations')

def get_named_parameter(event, name):
    """
    Get a parameter from the lambda event
    """
    return next(item for item in event['parameters'] if item['name'] == name)['value']


def get_registration_details(donation_id):
    """
    Retrieve details of a donation registration
    
    Args:
        donor_id (string): The ID of the registration to retrieve
    """
    try:
        response = table.get_item(Key={'registration_id': registration_id})
        if 'Item' in response:
            return response['Item']
        else:
            return {'message': f'No registration found with ID {registration_id}'}
    except Exception as e:
        return {'error': str(e)}


def create_registration(date, name, age, weight):
    """
    Create a new donor registration
    
    Args:
        date (string): The date of the registration
        name (string): Name to idenfity your reservation
        age (integer): Age must be over 18 years old
        weight (integer): Weight must be over 110 lbs
    """
    try:
        registration_id = str(uuid.uuid4())[:8]
        table.put_item(
            Item={
                'registration_id': registration_id,
                'date': date,
                'name': name,
                'age': age,
                'weight': weight
            }
        )
        return {'registration_id': registration_id}
    except Exception as e:
        return {'error': str(e)}


def delete_registration(registration_id):
    """
    Delete an existing donor registration
    
    Args:
        booking_id (str): The ID of the booking to delete
    """
    try:
        response = table.delete_item(Key={'registration_id': registration_id})
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return {'message': f'Register with ID {registration_id} deleted successfully'}
        else:
            return {'message': f'Failed to delete registration with ID {registration_id}'}
    except Exception as e:
        return {'error': str(e)}
    

def lambda_handler(event, context):
    # get the action group used during the invocation of the lambda function
    actionGroup = event.get('actionGroup', '')
    
    # name of the function that should be invoked
    function = event.get('function', '')
    
    # parameters to invoke function with
    parameters = event.get('parameters', [])

    if function == 'get_registration_details':
        registration_id = get_named_parameter(event, "registration_id")
        if registration_id:
            response = str(get_registration_details(registration_id))
            responseBody = {'TEXT': {'body': json.dumps(response)}}
        else:
            responseBody = {'TEXT': {'body': 'Missing registration_id parameter'}}

    elif function == 'create_registration':
        date = get_named_parameter(event, "date")
        name = get_named_parameter(event, "name")
        age = get_named_parameter(event, "age")
        weight = get_named_parameter(event, "weight")

        if date and age and weight:
            response = str(create_registration(date, name, age, weight))
            responseBody = {'TEXT': {'body': json.dumps(response)}}
        else:
            responseBody = {'TEXT': {'body': 'Missing required parameters'}}

    elif function == 'delete_registration':
        registration_id = get_named_parameter(event, "registration_id")
        if registration_id:
            response = str(delete_registration(registration_id))
            responseBody = {'TEXT': {'body': json.dumps(response)}}
        else:
            responseBody = {'TEXT': {'body': 'Missing registration_id parameter'}}

    else:
        responseBody = {'TEXT': {'body': 'Invalid function'}}

    action_response = {
        'actionGroup': actionGroup,
        'function': function,
        'functionResponse': {
            'responseBody': responseBody
        }
    }

    function_response = {'response': action_response, 'messageVersion': event['messageVersion']}
    print("Response: {}".format(function_response))

    return function_response
