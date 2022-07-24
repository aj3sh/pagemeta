# PAGE META
Page meta is a Django package allowing to add meta tags and descriptions dynamically. Meta tags are stored in models and can be controlled by Django admin (or any CMS).

## Installation

In settings file
```python
INSTALLED_APPS = [
    ...
    'page_meta',
    ...
]

MIDDLEWARE = [
	...
	'page_meta.middleware.MetaRequestMiddleware', # for binding meta into the request
	...
]
```

## Creating a Meta tags
- Run the server. 
- Go to the Admin > Page_meta > Meta for pages.
- Create Meta for pages, use relative url in `page_url`. Also supports relative url but might varies in different domains.
- To create default tags for the whole system, use `page_url` as `default` or `DEFAULT` (case insensitive)


## Usage

### Load the meta tags in template
Include the meta template provided by the library, it automatically detects the current url and loads the meta tags.

In your template
```DjangoHTML
{% include "page_meta/meta.html" %}
```


### Set a Custom Meta tags
If you want to set a custom meta tags for specific pages or conditions, you can send a context variable named `meta` as an instance of `Meta`.

_Note: context variable can be overridden if MetaForPage for that url exists_

Example code:
```python

class MyView(TemplateView):
	...

	def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
		...
		context['meta'] = Meta(
			title='custom test',
			description='custom description',
			image_url='http://image_url_dot_com',
		)
        ...
		return context
    ...

```