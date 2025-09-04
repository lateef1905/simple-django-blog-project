from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextUploadingField(blank=True, null=True)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)  # Keep for backward compatibility
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.likes.filter(is_like=True).count()

    def total_dislikes(self):
        return self.likes.filter(is_like=False).count()

    def get_all_images(self):
        """Return all images associated with this post (including the main image and additional images)"""
        images = []
        if self.image:
            images.append(self.image)
        images.extend([img.image for img in self.additional_images.all()])
        return images

    def get_primary_image(self):
        """Return the primary image for display (first available image)"""
        if self.image:
            return self.image
        additional_images = self.additional_images.all()
        if additional_images.exists():
            return additional_images.first().image
        return None


class BlogPostImage(models.Model):
    """Model for additional images in a blog post"""
    post = models.ForeignKey(BlogPost, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/additional/')
    caption = models.CharField(max_length=200, blank=True, help_text="Optional caption for this image")
    order = models.PositiveIntegerField(default=0, help_text="Order in which this image should appear")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'uploaded_at']
        verbose_name = "Additional Blog Image"
        verbose_name_plural = "Additional Blog Images"

    def __str__(self):
        return f"Image for {self.post.title} (Order: {self.order})"


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

    def get_replies(self):
        return Comment.objects.filter(parent=self, active=True)


class LikeDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='likes')
    is_like = models.BooleanField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{'Like' if self.is_like else 'Dislike'} by {self.user.username} on {self.post.title}"
