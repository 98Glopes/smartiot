from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token

from apps.api import views


router = routers.DefaultRouter()
router.register(r'me', views.MyUserDetailView, basename='MyUser')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', obtain_jwt_token),
    path('refresh-token/', refresh_jwt_token),
    path('admin/', admin.site.urls),

    path('user/', views.CreateUserView().as_view()),
    # path('user/<int:pk>/', views.UpdateUserView().as_view()),

    path('device/', views.DeviceListCreateView().as_view()),
    path('device/<str:device>/', views.DeviceRetrieveUpdateView().as_view()),

    path('device/<str:device>/sensor/', views.SensorListCreateView().as_view()),
    path('device/<str:device>/sensor/<str:sensor>/', views.SensorRetrieveUpdateView.as_view())
]
