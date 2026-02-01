from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls')),
    path('orders/', include('orders.urls')),
    path('reports/', include('reports.urls')),
]
