# CKEditor Configuration

Add this configuration to your `Blog/settings.py` file:

```python
# CKEditor Configuration
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 400,
        'width': '100%',
        'toolbarCanCollapse': True,
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage',
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
        'removePlugins': ','.join([
            'stylesheetparser',
        ]),
    },
    'awesome_ckeditor': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', 'SpellChecker', 'Undo', 'Redo'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule'],
            ['TextColor', 'BGColor'],
            ['Smiley', 'SpecialChar'], 
            ['Source'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote'],
            ['FontSize', 'RemoveFormat', 'Maximize'],
        ],
        'height': 400,
        'width': '100%',
        'toolbarCanCollapse': True,
        'extraPlugins': ','.join([
            'uploadimage',
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    },
    'special': {
        'toolbar': 'Special',
        'toolbar_Special': [
            ['Bold', 'Italic', 'Underline', 'Strike', '-', 'Subscript', 'Superscript'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak'],
            ['Styles', 'Format', 'Font', 'FontSize', 'TextColor', 'BGColor'],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo'],
            ['Find', 'Replace', '-', 'SelectAll', 'RemoveFormat'],
            ['Maximize', 'ShowBlocks', 'Source']
        ],
        'height': 450,
        'width': '100%',
        'toolbarCanCollapse': True,
        'extraPlugins': ','.join([
            'uploadimage',
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
        'removePlugins': ','.join([
            'stylesheetparser',
        ]),
        'format_tags': 'p;h1;h2;h3;h4;h5;h6;pre;address;div',
        'font_names': 'Arial/Arial, Helvetica, sans-serif;' +
                     'Times New Roman/Times New Roman, Times, serif;' +
                     'Verdana;' +
                     'Courier New;' +
                     'Comic Sans MS;' +
                     'Impact;' +
                     'Lucida Sans Unicode;' +
                     'Tahoma;' +
                     'Trebuchet MS;' +
                     'Georgia;' +
                     'Palatino;',
        'colorButton_enableMore': True,
        'colorButton_colors': '000,800000,8B4513,2F4F4F,008080,000080,4B0082,696969,' +
                             'B22222,A52A2A,DAA520,006400,40E0D0,0000CD,800080,808080,' +
                             'F00,FF8C00,FFD700,008000,0FF,00F,EE82EE,A0A0A0,' +
                             'FFA07A,FFA500,FFFF00,00FF00,AFEEEE,ADD8E6,DDA0DD,D3D3D3,' +
                             'FFF0F5,FAEBD7,FFFFE0,F0FFF0,F0FFFF,F0F8FF,E6E6FA,FFF'
    }
}
```

Also, make sure to add these apps to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... your existing apps
    'ckeditor',
    'ckeditor_uploader',
]
```

And add this to your main `urls.py`:

```python
urlpatterns = [
    # ... your existing URLs
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
```
