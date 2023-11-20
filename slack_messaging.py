import slack
import os
from pathlib import Path
from dotenv import load_dotenv

def setup_slack_client():
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    return slack.WebClient(token=os.environ['SLACK_TOKEN'])

def send_slack_message(message, channel='#test', error_message=None):
    client = setup_slack_client()
    
    if error_message:
        message += f'\nError: {error_message}'

    client.chat_postMessage(channel=channel, text=message)

def pipeline_success():
    send_slack_message('Pipeline ran successfully')

def pipeline_failure(error_message=None):
    send_slack_message('Pipeline failed', error_message=error_message)
