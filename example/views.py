from django.views.generic import TemplateView, ListView, DetailView

from page_meta.models import Meta

from .models import Blog

class HomePageView(TemplateView):
    template_name = 'example/home.html'

class BlogListView(ListView):
    model = Blog
    template_name = 'example/blogs.html'

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'example/blogs-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()
        context['meta'] = Meta(
            title=blog.title,
            description=blog.description[:125],
            image=blog.photo,
        )
        return context
