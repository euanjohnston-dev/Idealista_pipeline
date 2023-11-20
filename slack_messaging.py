import slack
import os

def setup_slack_client():
    # No need to load .env, as Cloud Functions manages environment variables directly
    return slack.WebClient(token=os.environ['SLACK_TOKEN'])

def send_slack_message(message, channel='#test', error_message=None):
    client = setup_slack_client()

    if error_message:
        message += f'\nError: {error_message}'

    client.chat_postMessage(channel=channel, text=message)

def pipeline_success(request):
    # Adjust the function signature to handle HTTP request, if needed
    send_slack_message('Pipeline ran successfully')
    return "Pipeline run successfully!"

def pipeline_failure(request, error_message=None):
    # Adjust the function signature to handle HTTP request, if needed
    send_slack_message('Pipeline failed', error_message=error_message)
    return f"Pipeline failed with error: {error_message}" if error_message else "Pipeline failed"