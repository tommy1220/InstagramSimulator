from django.views.generic import TemplateView, ListView, DetailView
from Insta.models import Post


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


# 同上逻辑；同时为了加一个feature, 根据MVT需要改views, models, templates, 还有url configs
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
