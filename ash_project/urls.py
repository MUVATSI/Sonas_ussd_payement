from django.conf.urls.static import static
from django.conf.urls import include
from django.conf import settings
from django.contrib import admin
from django.urls import path
from assurances import views

urlpatterns = [
    path('home',views.home, name='home'),
    path('admin/', admin.site.urls),
    path('tech/',views.HomeView.as_view(), name='tech'),
    path('ajout/',views.Ajouter.as_view(), name='ajout'),
    path('paie/',views.PayementManuel.as_view(), name='paie'),
    path('quittance/<int:pk>',views.GenererQuittance.as_view(), name='quittance'),
    path('quittance-pdf/<int:pk>', views.get_quittance_pdf, name="quittance-pdf"),
    path('', include('ApiSimilation.urls')),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
