from django.shortcuts import render, get_object_or_404
from .models import UserPost, AdminPost
# from .forms import AdminPostForm


##############
# index page #
##############
def index(request):
    return render(request, 'school/index.html', {})


def post_detail(request, pk):
    admin_post = get_object_or_404(AdminPost, pk=pk)
    user_posts = UserPost.objects.filter(admin_post=pk)

    return render(request, 'school/base_detail.html', {'admin_post': admin_post, 'user_posts': user_posts})

#####################
# admin detail page #
#####################
#def admin_detail(request, pk):
    #admin_post = get_object_or_404(AdminPost, pk=pk)  # pk에 해당하는 admin_post 가 없을 경우 404 return

    #return render(request, 'school/admin_detail.html', {'admin_post': admin_post})


####################
# user detail page #
####################
#def user_detail(request, pk):
#    user_post = get_object_or_404(UserPost, pk=pk)  # pk에 해당하는 user_post 가 없을 경우 404 return

#    return render(request, 'school/admin_detail.html', {'user_post': user_post})
