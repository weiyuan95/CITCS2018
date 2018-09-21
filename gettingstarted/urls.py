from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^test$', hello.views.test, name='test'),
    url(r"^test2$", hello.views.test2, name="test2"),
    url(r"^testing_get", hello.views.testing_get, name="testing"),
    url(r"^testing_post", hello.views.testing_post, name="testing"),
    url(r"^square$", hello.views.squares, name="squares"),
    path('admin/', admin.site.urls),
]
