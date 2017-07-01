from  django.conf.urls import include, url
from django.contrib import admin
from  django.contrib.auth import views as auth_views
from courese import views

urlpatterns = [
    url(r"^accounts/login/$", auth_views.login, name="login"),
    url(r"^accounts/logout/$", auth_views.logout, name="logout"),
    url(r'^students/', include('students.urls')),
    url(r"^admin/", include(admin.site.urls)),
    url(r'^course/', include("courese.urls")),
# 展示课程
    url(r'^$', views.CourseListView.as_view(), name='course_list'),
]