from rest_framework.routers import DefaultRouter

from tasks import views

router = DefaultRouter()
router.register('', views.MovieViewSet, basename='MovieViewSet')
urlpatterns = []
urlpatterns += router.urls
