from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import Http404
from django.utils.text import slugify
from django.db import transaction
from .models import BlogPost, Comment, LikeDislike, BlogPostImage
from .forms import BlogPostForm, CommentForm, BlogPostImageFormSet


def post_list(request):
    posts = BlogPost.objects.all()
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/post_list.html', {'page_obj': page_obj})


def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = post.comments.filter(parent=None, active=True)
    comment_form = CommentForm()
    
    user_reaction = None
    if request.user.is_authenticated:
        try:
            reaction = LikeDislike.objects.get(user=request.user, post=post)
            user_reaction = 'like' if reaction.is_like else 'dislike'
        except LikeDislike.DoesNotExist:
            user_reaction = None
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'user_reaction': user_reaction,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
@require_POST
def add_comment(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    parent_id = request.POST.get('parent_id')
    
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.active = True
        
        if parent_id:
            try:
                parent_comment = Comment.objects.get(id=parent_id)
                comment.parent = parent_comment
                messages.success(request, 'Your reply has been added successfully!')
            except Comment.DoesNotExist:
                messages.error(request, 'Invalid parent comment.')
                return redirect('post_detail', pk=pk)
        else:
            messages.success(request, 'Your comment has been added successfully!')
        
        comment.save()
    else:
        messages.error(request, 'Please enter a valid comment.')
    
    return redirect('post_detail', pk=pk)


@login_required
@require_POST
def like_dislike_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    action = request.POST.get('action')
    
    if action not in ['like', 'dislike']:
        return JsonResponse({'error': 'Invalid action'}, status=400)
    
    try:
        existing_reaction = LikeDislike.objects.get(user=request.user, post=post)
        
        if (action == 'like' and existing_reaction.is_like) or \
           (action == 'dislike' and not existing_reaction.is_like):
            existing_reaction.delete()
            user_reaction = None
        else:
            existing_reaction.is_like = (action == 'like')
            existing_reaction.save()
            user_reaction = action
    
    except LikeDislike.DoesNotExist:
        LikeDislike.objects.create(
            user=request.user,
            post=post,
            is_like=(action == 'like')
        )
        user_reaction = action
    
    response_data = {
        'likes_count': post.total_likes(),
        'dislikes_count': post.total_dislikes(),
        'user_reaction': user_reaction
    }
    
    return JsonResponse(response_data)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        image_formset = BlogPostImageFormSet(request.POST, request.FILES, queryset=BlogPostImage.objects.none())
        
        if form.is_valid() and image_formset.is_valid():
            try:
                with transaction.atomic():
                    # Save the main post
                    post = form.save(commit=False)
                    post.author = request.user
                    post.save()
                    
                    # Save additional images
                    images = image_formset.save(commit=False)
                    for image in images:
                        image.post = post
                        image.save()
                    
                    # Delete any marked for deletion
                    image_formset.save_m2m() if hasattr(image_formset, 'save_m2m') else None
                    
                    messages.success(request, 'Your blog post has been created successfully!')
                    return redirect('post_detail', pk=post.pk)
            except Exception as e:
                messages.error(request, f'There was an error saving your post: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BlogPostForm()
        image_formset = BlogPostImageFormSet(queryset=BlogPostImage.objects.none())
    
    return render(request, 'posts/create_post.html', {
        'form': form,
        'image_formset': image_formset
    })


@login_required
def edit_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    # Only the author can edit their own post
    if post.author != request.user:
        messages.error(request, 'You can only edit your own posts.')
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        image_formset = BlogPostImageFormSet(request.POST, request.FILES, queryset=post.additional_images.all())
        
        if form.is_valid() and image_formset.is_valid():
            try:
                with transaction.atomic():
                    # Save the main post
                    form.save()
                    
                    # Save additional images
                    images = image_formset.save(commit=False)
                    for image in images:
                        image.post = post
                        image.save()
                    
                    # Handle deletions
                    for deleted_image in image_formset.deleted_objects:
                        deleted_image.delete()
                    
                    messages.success(request, 'Your blog post has been updated successfully!')
                    return redirect('post_detail', pk=post.pk)
            except Exception as e:
                messages.error(request, f'There was an error updating your post: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BlogPostForm(instance=post)
        image_formset = BlogPostImageFormSet(queryset=post.additional_images.all())
    
    return render(request, 'posts/edit_post.html', {
        'form': form,
        'image_formset': image_formset,
        'post': post
    })


@login_required
def delete_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    # Only the author can delete their own post
    if post.author != request.user:
        messages.error(request, 'You can only delete your own posts.')
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        post_title = post.title
        post.delete()
        messages.success(request, f'Your post "{post_title}" has been deleted successfully.')
        return redirect('post_list')
    
    return render(request, 'posts/delete_post.html', {'post': post})


@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    # Only the comment author can edit their own comment
    if comment.author != request.user:
        messages.error(request, 'You can only edit your own comments.')
        return redirect('post_detail', pk=comment.post.pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your comment has been updated successfully!')
            return redirect('post_detail', pk=comment.post.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'posts/edit_comment.html', {
        'form': form, 
        'comment': comment, 
        'post': comment.post
    })


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    
    # Only the comment author can delete their own comment
    if comment.author != request.user:
        messages.error(request, 'You can only delete your own comments.')
        return redirect('post_detail', pk=post.pk)
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Your comment has been deleted successfully.')
        return redirect('post_detail', pk=post.pk)
    
    return render(request, 'posts/delete_comment.html', {
        'comment': comment, 
        'post': post
    })


@login_required
def my_posts(request):
    posts = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'posts/my_posts.html', {'page_obj': page_obj})
