from django.shortcuts import render
from django.utils import timezone
from django.views.generic.base import TemplateView

from apps.school.models import AdminPost


def index(request):
    return render(request, 'school/index.html', {})


class AdminPostList(TemplateView):
    template_name = 'school/post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = AdminPost.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
        return context
