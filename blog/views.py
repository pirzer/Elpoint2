from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Post, Comment, Tag
from .forms import PostForm, CommentForm


class PostList(generic.ListView):
    """
    Renders all objects of Post model as list
    """
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6

    def get_context_data(self, *args, **kwargs):
        tag_items = Tag.objects.all()
        context = super(PostList, self).get_context_data(*args, **kwargs)
        context["tag_items"] = tag_items
        return context


class PostDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.order_by('create_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "comment_added": False,
                "liked": liked,
                "comment_form": CommentForm(),
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.order_by('create_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment.instance.email = request.user.email
            comment.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "comment_added": True,
                "comment_form": comment_form,
                "liked": liked,
            },
        )


class PostLike(View):
    """
    Allows user to like/unlike Posts
    """
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class CreatePost(CreateView):
    """
    Allows authenticated users to add
    and save Posts
    """
    model = Post
    form_class = PostForm
    template_name = 'create_post.html'
    success_url = reverse_lazy('home')

    # Source: https://stackoverflow.com/questions/67366138/django-display-message-after-creating-a-post # noqa
    def form_valid(self, form):
        form.instance.author = self.request.user
        msg = "Your Post was submitted successfully"
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super(CreateView, self).form_valid(form)


class UpdatePost(UpdateView):
    """
    Allows authenticated users to update
    already submitted posts
    """
    model = Post
    form_class = PostForm
    template_name = 'update_post.html'
    success_url = reverse_lazy('home')

    # Source: https://stackoverflow.com/a/67366233
    def form_valid(self, form):
        form.instance.author = self.request.user
        msg = "Your post has been updated successfully"
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super(UpdateView, self).form_valid(form)


class DeletePost(DeleteView):
    """
    Allows authenticated users to delete
    submitted posts
    """
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')

    # Source: https://stackoverflow.com/a/25325228
    def delete(self, request, *args, **kwargs):
        msg = "Your post has been deleted"
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super(DeleteView, self).delete(request, *args, **kwargs)


class TagList(View):
    """
    View to filter posts by specific tags
    """
    def get(self, request, tag):
        tag_posts = Post.objects.filter(tag__tagname=self.kwargs['tag'])

        return render(
            request,
            "tag_list.html",
            {
                "tag": tag,
                "tag_posts": tag_posts
            })


class UserPosts(generic.ListView):
    """
    Displays all Posts submitted only by
    currently authenticated user
    """
    model = Post
    template_name = 'user_posts.html'

    def get_queryset(self):
        queryset = Post.objects.filter(
            author__id=self.request.user.id).order_by('-created_on')
        return queryset
