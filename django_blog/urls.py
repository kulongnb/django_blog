from django.contrib import admin
# 记得引入include
from django.urls import path, include
from django.views.generic import TemplateView
# 存放映射关系的列表
urlpatterns = [
    path('',TemplateView.as_view(template_name='base.html')),
    path('admin/', admin.site.urls),

    # 新增代码，配置app的url
    path('article/', include('article.urls', namespace='article')),
    # 用户管理
    path('userprofile/', include('userprofile.urls', namespace='userprofile')),
    path('password-reset/', include('password_reset.urls')),
]
