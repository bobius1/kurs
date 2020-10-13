# from django.http import HttpResponse
from datetime import datetime

from django.shortcuts import render
from django.views.generic.base import View
# from .admin import Category, Post
from .models import Category, Post, Comment

# Create your views here.

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
        post_list = Post.objects.filter(published_date__lte=datetime.now(), published=True)
        print(category_list)
        return render(request, "blog/post_list.html", {"categories": category_list, "post_list": post_list})


class CategoryView(View):
    """Вывод статей категории"""
    def get(self, request, category_slug):
        category = Category.objects.get(slug=category_slug)
        posts = Post.objects.filter(
            category__slug=category_slug, category__published=True, published=True
        )
        return render(request, posts.first().get_category_template(), {"post_list": posts})


class PostDetailView(View):
    """Вывод полной статьи"""
    def get(self, request, category, slug):
        category_list = Category.objects.all()
        post = Post.objects.get(slug=slug)
        # comments = Comment.objects.filter(post=post) #при выгрузке комментариев через views.py
        # tags = post.get_tags()
        # print(tags)
        return render(request, post.template, {"categories": category_list, "post": post })


class CategoryPostView(View):
    """Вывод перечня постов"""
    def get(self, request):
        post_list = Post.objects.all()
        return render(request, "blog/post_list.html", {"posts": post_list})
