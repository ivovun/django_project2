from django.shortcuts import render
from .models import Post


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


# posts = [
#     {
#         'author': 'CoreyMS',
#         'title': 'Blog Post1',
#         'content': 'First post content',
#         'date_posted' : 'August 27, 2018',
#     },
#     {
#         'author': 'Jon Doe',
#         'title': 'Blog Post2',
#         'content': 'Second post content',
#         'date_posted': 'August 28, 2018',
#     },
# ]
