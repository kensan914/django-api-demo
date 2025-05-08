from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path("mails/", include("mail.urls")),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]
