from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
import main.views

admin.autodiscover()

urlpatterns = [
    url(r'^$', main.views.index, name='index'),
    url(r"^square$", main.views.squares, name="squares"),
    url(r"^prime-sum$", main.views.get_prime_sum, name="prime-sum"),
    path('admin/', admin.site.urls),
]
