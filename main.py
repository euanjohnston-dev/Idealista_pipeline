from idealista import idealista_run

def pipeline_idealista(request):
  idealista_run()
  return "Pipeline run successfully!"