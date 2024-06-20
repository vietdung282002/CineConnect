from django.http import HttpResponse
import os

def index(request):

    html_output = "hello"
    html_output +=f"<h1>{"World"}</h1>"

    # Trả về phản hồi HTML
    return HttpResponse(html_output)