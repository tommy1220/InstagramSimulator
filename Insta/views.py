from django.views.generic import TemplateView


class HelloWorld(TemplateView):  # now HelloWorld extends from TplV, has all its methods
    # now set the tplV's attribute template_name to someting I need
    template_name = 'test.html'
    # when someone wants to see what I have by using this view class 'HelloWOrd',
    # it invokes the get() method which uses the template_name --> directs to 'test.html' --> renders page
