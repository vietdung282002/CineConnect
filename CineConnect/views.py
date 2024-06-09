from django.http import HttpResponse
import os

def index(request):
    env_vars = [f"{key}: {value}" for key, value in os.environ.items()]

    # Tạo HTML cho danh sách
    html_output = "<h1>Environment Variables:</h1>"
    html_output += "<ul>"
    for var in env_vars:
        html_output += f"<li>{var}</li>"
    html_output += "</ul>"

    # Trả về phản hồi HTML
    return HttpResponse(html_output)