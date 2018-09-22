from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
import main.views

admin.autodiscover()

urlpatterns = [
    url(r'^$', main.views.index, name='index'),
    url(r"^square$", main.views.squares, name="squares"),
    url(r"^prime-sum$", main.views.get_prime_sum, name="prime-sum"),
    url(r"^airtrafficcontroller", main.views.flight, name="flights"),
    url(r"^tally-expense$", main.views.tally_expenses, name="tallyexpenses"),
    url(r'^customers-and-hotel/minimum-distance', main.views.min_dist, name='lmao'),
    url(r'^customers-and-hotel/minimum-camps', main.views.min_camps),
    url(r'^broadcaster/message-broadcast', main.views.broadcaster),
    url(r'^broadcaster/most-connected-node', main.views.most_connected_node),
    url(r"^sorting-game", main.views.solve_sliding),
    url(r'^imagesGPS', main.views.images_gps),
    url(r"^skill-tree", main.views.skill_tree),
    path('admin/', admin.site.urls),
]
