import time
import boto3
import logging
import ipywidgets as widgets
import uuid

from agent import create_agent_role, create_lambda_role
from agent import create_dynamodb, create_lambda, invoke_agent_helper

#Clients
s3_client = boto3.client('s3')
sts_client = boto3.client('sts')
session = boto3.session.Session()
region = session.region_name
account_id = sts_client.get_caller_identity()["Account"]
bedrock_agent_client = boto3.client('bedrock-agent')
bedrock_agent_runtime_client = boto3.client('bedrock-agent-runtime')
logging.basicConfig(format='[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
region, account_id

"""
Configuration settings for a plasma donation agent:

- Creates unique identifiers using AWS region and account ID
- Defines the agent name as 'plasma-donation-agent'
- Sets up IAM policy and role names for Bedrock access
- Includes a description of the agent's purpose for plasma donation services
- Contains instructions defining the agent's role as a plasma donation specialist
- Specifies an action group for handling donor registrations and appointments

The agent is configured to assist with plasma donation education and 
facilitate the donor registration process through Amazon Bedrock.
"""
suffix = f"{region}-{account_id}"
agent_name = 'plasma-donation-agent'
agent_bedrock_allow_policy_name = f"{agent_name}-ba"
agent_role_name = f'AmazonBedrockExecutionRoleForAgents_{agent_name}'

agent_description = "Agent specializing in plasma donation information and donor registration"
agent_instruction = """
You are a plasma donation specialist agent, dedicated to educating potential donors about plasma donation,
and facilitating the registration process.
"""

agent_action_group_description = """
Actions for checking registration or registering for an appointment"""

agent_action_group_name = "DonorRegistrationsActionGroup"

agent_foundation_model = 'anthropic.claude-3-sonnet-20240229-v1:0'

"""
1. Creating the DynamoDB Table for Donor Registrations

Our agent will us the DynamoDB table to retrieve, update, and delete donor registrations. We'll have an action group that calls a Lambda function to retrieve/update/delete from this table.
"""

table_name = 'donor_registrations'
create_dynamodb(table_name)
## Make sure you have lambda_function.py in your directory
lambda_iam_role = create_lambda_role(agent_name, table_name)
lambda_function_name = f'{agent_name}-lambda'
lambda_function = create_lambda(lambda_function_name, lambda_iam_role)

"""
2. Creating the Agent
"""
agent_role = create_agent_role(agent_name, agent_foundation_model)
# Using boto3 API to create an agent with Claude FM selected above 
response = bedrock_agent_client.create_agent(
    agentName=agent_name,
    agentResourceRoleArn=agent_role['Role']['Arn'],
    description=agent_description,
    idleSessionTTLInSeconds=1800,
    foundationModel=agent_foundation_model,
    instruction=agent_instruction,
)

#Retrieve the agentid
agent_id = response['agent']['agentId']

'''
3. Creating the Agent Action Group

Each action group has a set of functions that are called based on what LLM decides is the correct function to pursue.

Each function has a set of parameters that the user has to provide before the function gets executed. 

'''

agent_functions = [
    {
        'name': 'get_registration_details',
        'description': 'Retrieve details of a donor registration',
        'parameters': {
            "registration_id": {
                "description": "The ID of the registration to retrieve",
                "required": True,
                "type": "string"
            }
        }
    },
    {
        'name': 'create_registration',
        'description': 'Create a new registration',
        'parameters': {
            "date": {
                "description": "The date of the registration in the format YYYY-MM-DD",
                "required": True,
                "type": "string"
            },
            "name": {
                "description": "Name to idenfity your reservation",
                "required": True,
                "type": "string"
            },
            "age": {
                "description": "The age of the user, which must be 18 or older.",
                "required": True,
                "type": "integer"
            },
            "weight": {
                "description": "The weight of the prospective donor, which must be over 110 lbs.",
                "required": True,
                "type": "integer"
            }
        }
    },
    {
        'name': 'delete_registration',
        'description': 'Delete an existing registration',
        'parameters': {
            "registration_id": {
                "description": "The ID of the registration to delete",
                "required": True,
                "type": "string"
            }
        }
    },
]

# Create allow to invoke permission on lambda
lambda_client = boto3.client('lambda')
try:
    response = lambda_client.add_permission(
        FunctionName=lambda_function_name,
        StatementId=f'allow_bedrock_{agent_id}',
        Action='lambda:InvokeFunction',
        Principal='bedrock.amazonaws.com',
        SourceArn=f"arn:aws:bedrock:{region}:{account_id}:agent/{agent_id}",
    )
    print(response)
except Exception as e:
    print(e)

#Prepare the agent
response = bedrock_agent_client.prepare_agent(
    agentId=agent_id
)
print(response)
# Pause to make sure agent is prepared
time.sleep(30)
alias_id = 'TSTALIASID'

'''
Testing the agent - Uncomment the bottom if you are not using the console to test.

'''
%%time
session_id:str = str(uuid.uuid1())
query = "Hi, I am Anna. I want to create a donor registration."
response = invoke_agent_helper(query, session_id, agent_id, alias_id)
print(response)