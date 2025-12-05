from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Rotas HTML
    path("", include("core.urls.urls_html")),

    # Rotas da API
    path("api/", include("core.urls.urls_api")),
]
