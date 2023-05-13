from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.template.defaultfilters import slugify



STATUS = ((0, "Draft"), (1, "Published"))


class Tag(models.Model):
    """
    Defines the category of the tag of the object
    """
    tagname = models.CharField(max_length=80)

    def __str__(self):
        return self.tagname


# Source: https://github.com/Code-Institute-Solutions/Django3blog/blob/master/11_messages/blog/models.py
class Post(models.Model):
    """
    Defines Post object blog_posts post_entries line 29
    """
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    # create_on = models.DateField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='blogpost_like', blank=True)
    tag = models.ForeignKey(
        Tag, on_delete=models.PROTECT, default=1, related_name="tag")

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        """
        helper method to return total num of likes on post
        """
        return self.likes.count()

    def approved_comments(self):
        """
        helper method to return number of approved comments only
        """
        return self.comments.filter(approved=True)

    def save(self, *args, **kwargs):
        """
        helper method to generate slug for Posts submitted
        by non-admin users
        """
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    """
    Defines Comment object
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    name = models.CharField(max_length=80)
    # email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    # create_on = models.DateField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        # return f"Comment {self.body} by {self.name}"
        return f"{self.name} made this into a comment: {self.body}"
