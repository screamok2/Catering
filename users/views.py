from django.shortcuts import render, redirect
from django.views import View
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserCreateSerializer
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from .models import User
from django.core.cache import cache
from users.tasks import send_activation_email

class UserRegisterView(View):


    def get(self, request):
        return render(request, 'registration.html')

    def post(self, request):

        data = {
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
        }
        serializer = UserCreateSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save(is_active=False)
            user.send_activation_code()
            #activation_link = f"{settings.SITE_URL}/activate/{user.activation_code}/"
            #send_activation_email.delay(user.email, user.first_name, activation_link)
            return redirect('login')
        else:
            return render(request, 'registration.html', {'errors': serializer.errors})


def activate_user(request, code):
    email = cache.get(code)
    if not email:
        return HttpResponseBadRequest("Link is expired")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return HttpResponse(" User not found")

    if not user.is_active:
        user.is_active = True
        user.save()
        cache.delete(code)
        return HttpResponse("Your account has been activated!")
    return HttpResponse("Account is already active")