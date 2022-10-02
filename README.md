# PAGE META
Page meta is a Django package allowing to add meta tags, og tags, images, and descriptions dynamically. Meta tags are stored in models and can be managed through Django admin (or any CMS).

## Installation

```bash
pip install django-pagemeta
```

In settings file
```python
INSTALLED_APPS = [
    ...
    'pagemeta',
    ...
]

MIDDLEWARE = [
    ...
    'pagemeta.middleware.MetaRequestMiddleware', # for binding meta into the request
    ...
]
```

## Creating a Meta tags
- Run the server. 
- Go to the **Django Admin** > **Pagemeta** > **Meta for Pages**.
- Create Meta for pages, use full absolute url in `page_url`. Also supports relative url but might varies in different domains.
- To create default tags for the whole system, use `page_url` as `default` or `DEFAULT` (case insensitive)


## Usage

### Load the meta tags in template

In your template
```DjangoHTML
<head>
    ...
    {{ request.meta }}
    ...
</head>
```

Page titles are not rendered through `request.meta`. To render page title see the below example.
```DjangoHTML
...
<title>{{ request.meta.title }}</title>
...
```

For conditional titles `request.meta_exact` will be good. `request.meta_exact` contains the exact meta tags for the url or `None`. Whereas `request.meta` contains default value if no match found.
```DjangoHTML
...
<title>{{ request.meta_exact.title|default:'Default title' }}</title>
...
```
OR
```DjangoHTML
...
<title>{% if request.meta_exact %}{{ request.meta_exact.title }}{% else %}Title for {{ article }}{% endif %}</title>
...
```


### Set a Custom Meta tags
If you want to set a custom meta tags for specific pages or conditions, you can reassign request.meta with an instance of `Meta`.  
_Note: context variable can be overridden if MetaForPage for that url exists_

Example code:
```python

class MyView(TemplateView):
    ...

    def get_context_data(self, **kwargs):
        ...
        # adding custom meta
        self.request.meta = Meta(
            title='custom test',
            description='custom description',
            image_url='http://image_url_dot_com',
        )
        ...

```

## Contribution

### Install requirements
Create your virtualenv first.
```bash
pip install -r requirements.txt
```

### Running test cases
```
python manage.py test
```