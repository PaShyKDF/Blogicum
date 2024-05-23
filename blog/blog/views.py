from django.http import Http404
from django.shortcuts import (render, get_object_or_404, redirect)
from django.urls import reverse_lazy
from .models import Comments, Post, Category
from .forms import PostForm, CommentForm
from django.views.generic import (ListView, CreateView, UpdateView,
                                  DeleteView, DetailView)
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from user.forms import CustomUserUpdateForm
from django.utils import timezone


COUNT_POSTS = 10
USER = get_user_model()


def get_posts(**kwargs):
    return Post.objects.select_related(
        'category', 'author', 'location'
    ).prefetch_related('comment').order_by('-pub_date')


class SUrlProfileMixin:
    """Успешная переадресация на профиль"""

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user})


class SUrlDetailMixin:
    """Успешная переадресация на публикацию"""

    model = Comments
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'pk': self.object.post.pk})


class IndexListView(ListView):
    """Главная страница со списком публикаций"""

    model = Post
    template_name = 'blog/index.html'
    queryset = Post.objects.select_related(
        'category', 'author', 'location'
    ).filter(is_published=True,
             category__is_published=True,
             location__is_published=True,
             pub_date__lte=timezone.now()
             ).prefetch_related('comment').order_by('-pub_date')
    paginate_by = COUNT_POSTS


class PostCreateView(SUrlProfileMixin, LoginRequiredMixin, CreateView):
    """Создание публикации"""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    """Просмотр отдельной публикации"""

    model = Post
    template_name = 'blog/detail.html'
    ordering = ('-pub_date',)
    paginate_by = COUNT_POSTS

    def get_context_data(self, **kwargs):
        post = get_object_or_404(get_posts(location__is_published=True,
                                           ), pk=self.object.id)
        if post.author != self.request.user:
            if not (post.is_published
                    and post.category.is_published
                    and post.pub_date <= timezone.now()):
                raise Http404
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comment.select_related('author')
        )
        return context


class PostUpdateView(SUrlProfileMixin, LoginRequiredMixin, UpdateView):
    """Изменение публикации"""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(
            Post,
            pk=kwargs['pk']
        )
        if request.user == post.author:
            return super().dispatch(request, *args, **kwargs)
        return redirect('blog:post_detail', pk=kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={"pk": self.object.pk})


class PostDeleteView(SUrlProfileMixin, LoginRequiredMixin, DeleteView):
    """Удаление публикации"""

    model = Post

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(
            Post.objects.select_related('author'),
            pk=kwargs['pk']
        )
        if request.user == post.author:
            return super().dispatch(request, *args, **kwargs)
        return redirect('blog:post_detail', pk=kwargs['pk'])


class CategoryListView(ListView):
    """Отображение всех публикации отдельной категории"""

    model = Post
    template_name = 'blog/category.html'
    paginate_by = COUNT_POSTS

    def get_queryset(self):
        self.category = get_object_or_404(
            Category.objects.filter(is_published=True),
            slug=self.kwargs['category_slug'])

        queryset = get_posts(
            category__slug=self.kwargs['category_slug'],
            category__is_published=True,
            is_published=True,
            pub_date__lt=timezone.now()
        ).order_by('-pub_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.category
        context['category'] = category.title
        return context


def profile(request, username):
    """Страница профиля"""
    profile = get_object_or_404(USER, username=username)
    if profile != request.user:
        page_obj = get_posts(
            author=profile,
            is_published=True,
            category__is_published=True,
            location__is_published=True,
            pub_date__lte=timezone.now()).order_by('-pub_date')
    else:
        page_obj = get_posts(
            author=profile).order_by('-pub_date')
    paginator = Paginator(page_obj, COUNT_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'profile': profile, 'page_obj': page_obj}
    return render(request, 'blog/profile.html', context)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование своего профиля"""

    model = USER
    template_name = 'blog/user.html'
    form_class = CustomUserUpdateForm
    success_url = reverse_lazy('blog:index')


@login_required
def add_comment(request, pk):
    """Добавление коментариев к публикациям"""
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', pk=pk)


class CommentUpdateView(SUrlDetailMixin, LoginRequiredMixin, UpdateView):
    """Редактирование коментариев"""

    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.comment = get_object_or_404(
            Comments.objects.select_related('author'), pk=kwargs['pk']
        )
        if request.user == self.comment.author:
            return super().dispatch(request, *args, **kwargs)
        return redirect('blog:post_detail', pk=self.comment.post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.comment
        return context


class CommentDeleteView(SUrlDetailMixin, LoginRequiredMixin, DeleteView):
    """Удаление коментариев"""

    def dispatch(self, request, *args, **kwargs):
        self.comment = get_object_or_404(
            Comments.objects.select_related('author'), pk=kwargs['pk']
        )
        if request.user == self.comment.author:
            return super().dispatch(request, *args, **kwargs)
        return redirect('blog:post_detail', pk=self.comment.post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.comment
        return context
