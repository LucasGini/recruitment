"""recruitment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

import settings.base
from jobs.models import Job
from rest_framework import routers, serializers, viewsets
from django.conf.urls.static import static


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


# 注册到API
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'jobs', JobViewSet)

urlpatterns = [
    path('api/', include(router.urls)), # 定义API访问根路径
    url(r"^", include('jobs.urls')),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    url('^accounts/', include('registration.backends.simple.urls')),
    url(r'^api-auth/', include('rest_framework.urls'))
]
urlpatterns += static(settings.base.MEDIA_URL,
                      document_root=settings.base.MEDIA_ROOT)


admin.site.site_header = _('匠果科技招聘管理系统')
