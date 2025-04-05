"""
URL configuration for mynotes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# 配置URL路由到mynotes/urls.py
from django.contrib import admin
from django.urls import path
from notes import views
from django.urls import path, include  # 确保导入了include
import debug_toolbar


urlpatterns = [
    # path("admin/", admin.site.urls),
    path('notes/', include('notes.urls')),
    path('__debug__/', include(debug_toolbar.urls)),

]
