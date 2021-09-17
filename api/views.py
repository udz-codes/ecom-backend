from django.http import JsonResponse


def home(request):
    return JsonResponse({
        'info': 'Django Rest Framework',
        'name': 'Ujjwal'
    })