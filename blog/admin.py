from django.contrib import admin
from .models import Post, Comment, Tag
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'author', 'tag', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    list_filter = ('status', 'created_on', 'tag')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    class Meta:
        model = Comment
        fields = ('body',)


    def approve_comments(self, request, queryset):
        queryset.update(approved=True)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
