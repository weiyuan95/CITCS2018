from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

import main.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', main.views.index, name='index'),
    url(r"^square$", main.views.squares, name="squares"),
    path('admin/', admin.site.urls),
]
