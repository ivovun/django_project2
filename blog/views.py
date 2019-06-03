from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']  # знак минус - обратный порядок
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    # ordering = ['-date_posted']  # знак минус - обратный порядок
    paginate_by = 5

    def get_queryset(self):
        # so now if that user exists then we will
        # capture them in that user variable ( 26:24)
        # if they don't exist then it's just going to return a 404 ( 26:28)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()  # этот метод из UserPassesTestMixin
        # возвращает пост который мы должны обновить
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()  # этот метод из UserPassesTestMixin
        # возвращает пост который мы должны обновить
        return self.request.user == post.author


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
