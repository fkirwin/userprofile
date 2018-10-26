from django.shortcuts import render

def home(request):
    """Basic route for home."""
    return render(request, 'home.html')
