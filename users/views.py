from django.http import HttpResponse


def index(request):
    return HttpResponse("Тут должны быть юзеры, но это не точно")
