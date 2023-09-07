"""
URL configuration for bookmark_db project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import path
from django.utils.translation import gettext as _


# Disable Django admin authentication.
admin_user = User.objects.first()
admin.site.has_permission = lambda request: setattr(request, 'user', admin_user) or True

admin.site.enable_nav_sidebar = False
admin.site.index_title = _('Site administration')
admin.site.site_header = _('Bookmark DB')
admin.site.site_title = _('Bookmark DB')
# admin.site.site_url = None

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path('', admin.site.urls),
]
