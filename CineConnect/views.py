from django.http import HttpResponse
import os

def index(request):
    settings_module = 'CineConnect.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'CineConnect.settings'
    
    env_vars = [f"{key}: {value}" for key, value in os.environ.items()]
    html_output = settings_module
    # Tạo HTML cho danh sách
    html_output += "<h1>Environment Variables:</h1>"
    html_output += "<ul>"
    for var in env_vars:
        html_output += f"<li>{var}</li>"
    html_output += "</ul>"

    # Trả về phản hồi HTML
    return HttpResponse(html_output)