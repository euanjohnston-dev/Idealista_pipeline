from idealista import idealista_run
import base64

def pipeline_idealista(data, context):
  
  message = base64.b64decode(data['data']).decode('utf-8')
  print(f'Hello, {message}!')
  idealista_run()
  return "Pipeline run successfully!"