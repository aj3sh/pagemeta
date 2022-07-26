from django.views.generic import TemplateView, ListView, DetailView

from pagemeta.models import Meta

from .models import Blog

class HomePageView(TemplateView):
    template_name = 'pagemeta_example/home.html'

class BlogListView(ListView):
    model = Blog
    template_name = 'pagemeta_example/blogs.html'

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'pagemeta_example/blogs-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()
        self.request.meta = Meta(
            title=blog.title,
            description=blog.description[:125],
            image=blog.photo,
        )
        return context
