from django import forms
from django.forms import modelformset_factory
from .models import BlogPost, Comment, BlogPostImage
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class BlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget(config_name='special'))
    
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter an engaging title for your post...',
                'maxlength': '200'
            }),
            # content field is handled above with CKEditorUploadingWidget
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'title': 'Post Title',
            'content': 'Post Content',
            'image': 'Featured Image (Optional)'
        }
        help_texts = {
            'title': 'Choose a catchy title that summarizes your post (max 200 characters)',
            'content': 'Write your complete blog post using the rich text editor with all formatting options.',
            'image': 'Upload a featured image for your post (JPG, PNG, GIF supported)'
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or len(title.strip()) < 5:
            raise forms.ValidationError('Title must be at least 5 characters long.')
        return title.strip()

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or len(content.strip()) < 50:
            raise forms.ValidationError('Content must be at least 50 characters long.')
        return content.strip()


class BlogPostImageForm(forms.ModelForm):
    class Meta:
        model = BlogPostImage
        fields = ['image', 'caption', 'order']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'caption': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional caption for this image...',
                'maxlength': '200'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'placeholder': '0'
            })
        }
        labels = {
            'image': 'Additional Image',
            'caption': 'Image Caption (Optional)',
            'order': 'Display Order'
        }


# Create a formset for handling multiple images
BlogPostImageFormSet = modelformset_factory(
    BlogPostImage,
    form=BlogPostImageForm,
    extra=3,  # Show 3 empty forms by default
    can_delete=True,
    max_num=10,  # Maximum 10 additional images
    validate_max=True
)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your thoughts about this post...',
                'style': 'resize: vertical;'
            })
        }
        labels = {
            'content': 'Your Comment'
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or len(content.strip()) < 5:
            raise forms.ValidationError('Comment must be at least 5 characters long.')
        return content.strip()
