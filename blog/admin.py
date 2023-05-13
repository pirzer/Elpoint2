from django.contrib import admin
from .models import Post, Comment, Tag
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)
# class PostAdmin(SummernoteModelAdmin):
class PostAdmin(admin.ModelAdmin):


# removing 'slug', 'status', 'created_on' from list_display
    list_display = ('title', 'author', 'tag')
# removing , 'content' from search_fields
    search_fields = ['title']
# removing , 'status',  from list_filter
    list_filter = ('created_on', 'tag')
    prepopulated_fields = {'slug': ('title',)}
    # summernote_fields = ('content',)

    class Meta:
        model = Post
        fields = ('content',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
# removing  'body','created_on',  from list_display
    list_display = ('name', 'post', 'approved')
# added  , 'post'  to  list_filter
    list_filter = ('approved', 'created_on', 'post')
# removing  , 'email', 'body'  from search_fields
    search_fields = ['name']
    # actions = ['approve_comments']

    class Meta:
        model = Comment
        fields = ('body',)


    # def approve_comments(self, request, queryset):
    #     queryset.update(approved=True)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
