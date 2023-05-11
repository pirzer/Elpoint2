from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


STATUS = ((0, "Draft"), (1, "Published"))


class Label(models.Model):
    """
    Defines label object (category)
    """
    labelname = models.CharField(max_length=80)

    def __str__(self):
        return self.labelname


# Source: https://github.com/Code-Institute-Solutions/Django3blog/blob/master/11_messages/blog/models.py#:~:text=class%20Post(,.count() # noqa
class Post(models.Model):
    """
    Defines Post object
    """
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts")
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    create_on = models.DateField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='blogpost_like', blank=True)
    label = models.ForeignKey(
        Label, on_delete=models.PROTECT, default=1, related_name="label")

    class Meta:
        ordering = ['-create_on']

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
        return self.tankas.filter(approved=True)

    def save(self, *args, **kwargs):
        """
        helper method to generate slug for posts submitted
        by non-admin users
        """
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


# Source: https://github.com/Code-Institute-Solutions/Django3blog/blob/master/11_messages/blog/models.py#:~:text=class%20Comment(,name%7D%22  # noqa
class Comments(models.Model):
    """
    Defines Comment object
    """
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=70)
    body = models.TextField()
    created_on = models.DateField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-create_on']

    def __str__(self):
        return f"{self.name} made this into a comment: {self.body}"
        # return f"Comment {self.body} by {self.name}"
