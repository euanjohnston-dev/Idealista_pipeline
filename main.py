from idealista import idealista_run
import base64
from slack_messaging import pipeline_success, pipeline_failure

def idealista_pipeline(data, context):
    try:
        message = base64.b64decode(data['data']).decode('utf-8')
        print(f'Hello, {message}!')
        
        idealista_run()
        
        pipeline_success()
        return "Pipeline run successfully!"
    
    except Exception as e:
        pipeline_failure(e)
        return f"Pipeline failed with error: {str(e)}"