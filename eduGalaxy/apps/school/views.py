from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic.base import TemplateView

from apps.school.models import Post, Review


##############
# index page #
##############
def index(request):
    return render(request, 'school/index.html', {})


def post_detail(request, pk):
    admin_post = get_object_or_404(Post, pk=pk)
    user_posts = Review.objects.filter(admin_post=pk)

    return render(request, 'school/base_detail.html', {'admin_post': admin_post, 'user_posts': user_posts})

#####################
# admin detail page #
#####################
# def admin_detail(request, pk):
#     admin_post = get_object_or_404(AdminPost, pk=pk)  # pk에 해당하는 admin_post 가 없을 경우 404 return
#
#     return render(request, 'school/admin_detail.html', {'admin_post': admin_post})


####################
# user detail page #
####################
#def user_detail(request, pk):
#    user_post = get_object_or_404(UserPost, pk=pk)  # pk에 해당하는 user_post 가 없을 경우 404 return

#    return render(request, 'school/admin_detail.html', {'user_post': user_post})
class AdminPostList(TemplateView):
    template_name = 'school/post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
        return context
