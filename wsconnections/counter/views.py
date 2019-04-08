from django.views.generic import TemplateView
from nanoid import generate

class CountersWrapperView(TemplateView):
    template_name = "counter/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nanoid'] = generate(size=6)
        return context

class CountView(TemplateView):
    template_name = "counter/count.html"