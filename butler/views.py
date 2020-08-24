from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def event(request):
    print("An event!")
    print(request.POST)
    return HttpResponse()
