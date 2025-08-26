from django.urls import path, include

urlpatterns = [
    path('pages/', include('api.v1.pages.urls'))
]

