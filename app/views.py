from django.http import HttpResponse


def app_home(request):
    return HttpResponse("""
        <p>Welcome to the 'Know Your Planet' Backend.</p>
        <p>The api is available at /api</p>
    """)
