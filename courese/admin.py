from django.contrib import admin
from .models import Subject, Course, Module

# admin.register() 与 admin.site.register() 功能相同
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug':('title',)}

class ModuleInline(admin.StackedInline):
    model = Module

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
    actions = ['asset_approval',]
    def asset_approval(self, request, querysets):
        pass
    asset_approval.short_description = "资产审批"