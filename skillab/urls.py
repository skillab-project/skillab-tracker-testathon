from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from ninja import NinjaAPI
from django.shortcuts import render
from ninja.openapi.docs import DocsBase

from api.views import router


class CustomSwagger(DocsBase):
    def render_page(self, request, api):
        return render(request, "swagger.html")


media_urls = (
    static("/media", document_root=settings.BASE_DIR / "media")
    if settings.DEBUG
    else []
)

api = NinjaAPI(title="Skillab Tracker API", docs=CustomSwagger())
api.add_router("", router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
] + media_urls
