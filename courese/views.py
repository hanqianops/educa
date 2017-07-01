from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.db.models import Count
from .models import Subject

"""
LoginRequiredMixin：复制login_required装饰器的功能。
PermissionRequiredMixin：会在用户使用视图的时候检查该用户是否有指定在permission_required属性中的权限。超级用户自动拥有所有权限。
"""

from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuleFormSet
from django.forms.models import modelform_factory
from django.apps import apps
from .models import Module
from .models import Course
from .models import Content


class OwnerMixin(object):
    """
    提供课程过滤功能，只检索前用户创建的课程
    """
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    """
    带有表单的视图或模型表单的视图比如Createview和UpdateView.form_valid()当提交的表单是有效的时候就会被执行
    """
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)

class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ['subject', 'title', 'slug', 'overview']  # 从CreateView和UpdateView视图中构建模型。
    success_url = reverse_lazy('manage_course_list')  # 表单成功提交之后重定向用户
    template_name = 'courses/manage/course/form.html'

class ManageCourseListView(OwnerCourseMixin, ListView):
    """
    用户课程排序
    """
    template_name = 'courses/manage/course/list.html'

class CourseCreateView(PermissionRequiredMixin, OwnerCourseEditMixin, CreateView):
    """
    创建课程
    """
    permission_required = 'courses.add_course'

class CourseUpdateView(PermissionRequiredMixin, OwnerCourseEditMixin, UpdateView):
    """
    更新课程
    """
    template_name = 'courses/manage/course/form.html'
    permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin, OwnerCourseMixin, DeleteView):
    """
    删除课程
    """
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('manage_course_list')
    permission_required = 'courses.delete_course'



########## 管理课程模块
class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    def dispatch(self, request,pk):
        """
        先获取当前用户的课程
        :param **kwargs:
        """
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super(CourseModuleUpdateView, self).dispatch(request, pk)

    def get_formset(self, data=None):
        """
        定义这个方法去避免重复构建formset的代码。
        使用可选数据为给予的Course对象创建一个ModuleFormSet对象。
        """
        return ModuleFormSet(instance=self.course, data=data)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():  # 验证提交的表单
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course, 'formset': formset})

#### 给模块添加内容
class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            # 使用Django的apps模块获取指定的model
            return apps.get_model(app_label='courese', model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        """构建一个动态的表单集"""
        Form = modelform_factory(model, exclude=['owner', 'order', 'created', 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        """
        :param request:
        :param module_id:  内容关联的模块ID
        :param model_name:  要创建或更新的内容的模型名
        :param id: 将要更新的对象的id。在创建新对象的时候它会是None。
        """
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)
        return super(ContentCreateUpdateView,
                     self).dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # new content
                Content.objects.create(module=self.module,)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content,
                            id=id,
                            module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    """管理模块和内容"""
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)

        return self.render_to_response({'module': module})



class CourseListView(TemplateResponseMixin, View):
    """展示课程"""
    model = Course
    template_name = 'courses/course/list.html'
    def get(self, request, subject=None):
        subjects = Subject.objects.annotate(
                      total_courses=Count('courses'))
        courses = Course.objects.annotate(
                      total_modules=Count('modules'))
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)
        return self.render_to_response({'subjects':subjects, 'subject': subject, 'courses': courses})


from django.views.generic.detail import DetailView

class CourseDetailView(DetailView):
    """展示课程详情"""
    model = Course
    template_name = 'courses/course/detail.html'