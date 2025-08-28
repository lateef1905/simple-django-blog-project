from django.contrib import admin
from .models import BlogPost, Comment, LikeDislike, BlogPostImage


class BlogPostImageInline(admin.TabularInline):
    model = BlogPostImage
    extra = 3
    fields = ['image', 'caption', 'order']
    ordering = ['order']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'total_likes', 'total_dislikes', 'image_count']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {'title': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    inlines = [BlogPostImageInline]

    def image_count(self, obj):
        return len(obj.get_all_images())
    image_count.short_description = 'Total Images'


@admin.register(BlogPostImage)
class BlogPostImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'caption', 'order', 'uploaded_at']
    list_filter = ['uploaded_at', 'post']
    list_editable = ['order']
    search_fields = ['post__title', 'caption']
    date_hierarchy = 'uploaded_at'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at', 'active', 'parent']
    list_filter = ['active', 'created_at']
    search_fields = ['content', 'author__username']
    list_editable = ['active']
    date_hierarchy = 'created_at'


@admin.register(LikeDislike)
class LikeDislikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'is_like', 'created_at']
    list_filter = ['is_like', 'created_at']
    search_fields = ['user__username', 'post__title']
