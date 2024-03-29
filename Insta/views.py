# pylint: disable=no-member
from django.views.generic import TemplateView, ListView, DetailView
# 为了user interaction会遇到的security, error handling, UI alert, redirect等问题， django提供的Form提供了很好的平台
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from Insta.models import Post, Like, InstaUser, UserConnection
from Insta.forms import CustomUserCreationForm

# 一个用于给PostView等使用的multi-inheritance：目的就是使得用户不login就看不到
from django.contrib.auth.mixins import LoginRequiredMixin

# imported for using ajax request. need to do---> pipenv install django-annoying
from annoying.decorators import ajax_request

class HelloWorld(TemplateView):  # now HelloWorld extends from TplV, has all its methods
    # now set the tplV's attribute template_name to someting I need
    template_name = 'test.html'
    # when someone wants to see what I have by using this view class 'HelloWOrd',
    # it invokes the get() method which uses the template_name --> directs to 'test.html' --> renders page


class PostsView(ListView):  # inherit from ListView
    # override the following from ListView
    # 这里的model使用的是import进来的Post的model, 当有人调用我这个model的时候，PostsView(or ListView)会生成一个object_list，
    # 所以这里urls.py(urls -> MVT模型）调用PostsView.as_View()时，就会有生成一个posts的object_list, 传递到index.html，可以在index.html里使用
    model = Post  # 我希望这个class可以使用model, which is Post model
    # 我还希望这个class可以用index.html的template作为显示，所以要去urls.py进行import，还要去templates/ 添加index.html
    template_name = 'index.html'

    # Overwrite ListView自带的get_queryset(): 
    # get the list of items for this View. query的结果的posts给到index.html里， 而不是无脑全部的posts
    def get_queryset(self):
        # 默认： return Post.objects()
        # updated: 只把用户关注的用户的posts放到网页
        current_user = self.request.user
        following = set()
        for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
            following.add(conn.following)
        return Post.objects.filter(author__in=following)

# 同上逻辑；同时为了加一个feature, 根据MVT需要改views, models, templates, 还有url configs
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


# 同上逻辑；同时为了加一个feature, 根据MVT需要改views, models, templates, 还有url configs
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post  # CreateView是create 什么东西呢？用的model还是import进来的Post的model
    template_name = 'post_create.html'  # 创建什么页面呢？
    # 在CreateView里有一个attribute叫做fields, 可以从model里来(Post)。这里就是在说当create一个model的时候，希望用户提供哪些field? 因为想要用户提供全部的attributes, 那就是all
    fields = '__all__'
    # 这样因为写了__all__ 当全部当attributes从model里拿出来后，会被render到post_create.html里
    # 因为继承了LoginRequiredMixin, 所以还么login的话就要跳转到login界面
    login_url = 'login'


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title']


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    # 不存在哪个fields了，全删了
    success_url = reverse_lazy("posts")
    # 因为调用这个View时就在删东西了，如果此时使用reverse的话，就相当于一边删除一遍跳转，这是不允许的。所以要用reverse_lazy来
    # lazily delete这个model object


# 对于user login.logout来讲，因为Django提供的LoginView里提供了很多自带features, 但是user sign up没有，所以需要自定义


class SignUp(CreateView):
    # CreatseView, UpdateView,DeleteView都是基于表格/Form，如上面Post就是那些View的表格，但是在Create User的时候
    # 相当于在使用一个组合了 fields + model 的form, 也就是from django.contrib.auth.forms import UserCreationForm里的UserCreationForm
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy("login")


class UserDetailView(DetailView):
    model = InstaUser
    template_name = 'user_detail.html'


@ajax_request #这个函数是专门响应ajax用的，所以不用render到一个template上，所以不用专门设置一个views class
def addLike(request):
    post_pk = request.POST.get('post_pk') #通过request里对POST请求里，通过key='post_pk'拿value
    post = Post.objects.get(pk=post_pk) # 从Post这个model里全部的objects里拿pk等于上面拿到的pk的那个post. Django里允许用pk = ... 或者 id =... 
    try:
        like = Like(post=post, user=request.user) #Constructor, param: post & request.user
        like.save() # after constructing the Like object, need to save it to database
        # like is already existed, 因为like关系是unique_together(user), throw exception
        result = 1
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user) # like object以及存在，说明用户此时点这个“点赞”是在“取消赞”
        like.delete() # 取消点赞
        result = 0
    # result is what's gonna be returned as a response

    return {
        'result': result,
        'post_pk': post_pk
    }