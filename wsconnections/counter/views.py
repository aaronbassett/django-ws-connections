from django.views.generic import TemplateView

class CountView(TemplateView):
    template_name = "counter/count.html"