from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module


# Django自带一个抽象层,用于在同一个页面中使用多个表单,这些表单的组合成为formsets。
# formsets能管理多个Form或者ModelForm表单实例。所有的表单都可以一次性提交
# 还可以做一些其他的事，如表单的初始化数据展示，限制表单能够提交的最大数字，以及所有表单的验证。
ModuleFormSet = inlineformset_factory(
                                Course,
                                Module,
                                fields=['title', 'description'],  # 这个字段将会被formset中的每个表单包含。
                                extra=2,  # 允许我们设置在formset中显示的空的额外的表单数。
                                can_delete=True  # 包含一个布尔字段给所有的表单，该布尔字段将会渲染成一个复选框。允许你确定这个对象你真的要进行删除。
                                )

