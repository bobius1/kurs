from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from .admin import Category

"""методом функций"""

# def home(request):
#     if request.method == "POST":
#         return HttpResponse("Hi")
#     elif request.method == "GET":
#         return HttpResponse("Good")

"""метод класса"""

# class HomeView(View):
#     def get(self, request):
#         return HttpResponse("Good")
#
#     def post(self):
#         pass

class HomeView(View):
    """Home page"""
    def get(self, request):
        category_list = Category.objects.all()
        print(category_list)
        return render(request, "blog/home.html", {"categories":category_list})

class CategoryView(View):
    """Вывод статей категории"""
    def get(self, request, category_name):
        category = Category.objects.get(slug=category_name)
        return render(request, "blog/post_list.html", {"category": category })





