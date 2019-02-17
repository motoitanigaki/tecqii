from django.conf import settings

from django.conf.urls.static import static
from django.urls import include, path
from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib import admin
from tecqii.views import UserListView, UserDetailView


urlpatterns = [
    path("", UserListView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
    url(r'^user/(?P<pk>[^/]+)', UserDetailView.as_view(), name="user-detail"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
