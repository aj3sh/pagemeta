# PAGE META

## Installation

In settings file
```
INSTALLED_APPS = [
    ...
    'page_meta',
    ...
]
```

## Creating a Meta tags
- Run the server. 
- Go to the Admin > Page_meta > Meta for pages.
- Create Meta for pages, use relative url in `page_url`. Also supports relative url but might varies in different domains.
- To create default tags for the whole system, use `page_url` as `default`


## Usage

### Load the meta tags in template
Include the meta template provided by the library, it automatically detects the current url and loads the meta tags.

In your template
```DjangoHTML
{% include "page_meta/meta.html" %}
```


### Set a Custom Meta tags
If you want to set a custom meta tags for specific pages or conditions, you can send a context variable named `meta` as an instance of `Meta`

Example code:
```python

class MyView(TemplateView):
	...

	def get_context_data(self, **kwargs):
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