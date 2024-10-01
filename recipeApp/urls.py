import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("authentication.urls")),
    path("recipes/", include("recipes.urls")),
    path("blogs/", include("blogs.urls")),
    path("nutritionist/", include("nutritionists.urls")),
    path("__debug__/", include(debug_toolbar.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

