import psutil
import requests
from fastapi import status


def gradio_healthcheck():
    # Send request to gradio interface and returns response status
    try:
        response = requests.get("http://0.0.0.0:8000/")
        return response.status_code
    except:
        return 500


def app_healthcheck():
    # Gradio interface check
    gradio_status = gradio_healthcheck()
    if gradio_status != 200:
        return {'healthcheck': 'Gradio interface error'}, gradio_status

    # Check available disk space
    disk_usage = psutil.disk_usage('/')
    available_disk_space = disk_usage.free
    if available_disk_space < 1073741824:
        return {'healthcheck': 'Low disk space'}, status.HTTP_500_INTERNAL_SERVER_ERROR

    # Check memory usage
    memory_usage = psutil.virtual_memory().percent
    if memory_usage >= 80:
        return {'healthcheck': 'High memory usage'}, status.HTTP_500_INTERNAL_SERVER_ERROR

    # If all checks pass, return status OK
    return {'healthcheck': 'OK'}
