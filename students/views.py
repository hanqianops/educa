from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')  # 成功后返回此url

    def form_valid(self, form):
        """合法的表单数据被提交时 form_valid() 方法就会执行。它必须返回一个 HTTP 响应"""
        result = super(StudentRegistrationView,
                       self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                            password=cd['password1'])
        login(self.request, user)
        return result
