from django.contrib.auth.models import User
from django.shortcuts import redirect

from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from .models import Post, Responses
from .forms import PostForm, ResponseForm
from .filters import PostFilter
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin


class PostsList(ListView):
    model = Post
    ordering = '-create_time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    form_class = ResponseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_pk = self.kwargs.get('pk', None)
        post_query = Post.objects.filter(id=post_pk)
        post_object = post_query[0]
        context['post'] = post_object
        return context

    def form_valid(self, form):
        response = form.save(commit=False)
        author_object = User.objects.filter(id=self.request.user.id)
        response.author = author_object[0]
        news_pk = self.kwargs.get('pk', None)
        post_object = Post.objects.filter(id=news_pk)
        response.post = post_object[0]
        response.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_list')


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        author_object = User.objects.filter(id=self.request.user.id)
        post.author = author_object[0]
        post.save()

        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    success_url = reverse_lazy('my_posts')


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('my_posts')


class PostResponse(LoginRequiredMixin, CreateView):
    form_class = ResponseForm
    model = Responses
    template_name = 'post_response.html'

    def form_valid(self, form):
        response = form.save(commit=False)
        author_object = User.objects.filter(id=self.request.user.id)
        response.author = author_object[0]
        post_object = Post.objects.filter(id=self.request.post.id)
        response.post = post_object[0]
        response.save()

        return super().form_valid(form)


class MyPosts(ListView):
    model = Post
    ordering = '-create_time'
    template_name = 'my_posts.html'
    context_object_name = 'my_posts'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        my_queryset = queryset.filter(author=self.request.user)
        self.filterset = PostFilter(self.request.GET, my_queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostResponses(ListView):
    model = Responses
    ordering = '-create_time'
    template_name = 'post_responses.html'
    context_object_name = 'responses'
    paginate_by = 3

    def get_queryset(self):
        self.queryset = Responses.objects.filter(post=self.kwargs['post_id'])
        return super().get_queryset()


class ResponseDelete(DeleteView):
    model = Responses
    template_name = 'response_delete.html'
    success_url = reverse_lazy('my_posts')


def accept_response(request, pk):
    response = Responses.objects.get(id=pk)
    email = response.author.email

    html_content = render_to_string(
        'responser_not.html',
        {
            'post': response,
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'Ваш отклик приняли!',
        body=response.text,
        from_email='lion4652@yandex.ru',
        to=[email],
    )
    msg.attach_alternative(html_content, "text/html")

    msg.send()

    response.delete()
    return redirect('my_posts')

