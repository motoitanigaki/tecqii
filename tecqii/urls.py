from django.conf import settings

from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import TemplateView
from django.contrib import admin
from tecqii.views import UserListView


urlpatterns = [
    # path("", TemplateView.as_view(template_name="homepage.html"), name="home"),
    path("", UserListView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
