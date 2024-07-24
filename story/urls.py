# story/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginAPIView, LogoutAPIView,RegisterAPIView, UserViewSet , PlanListCreateAPIView, PlanRetrieveUpdateDestroyAPIView, UserPlanViewSet, WidgetViewSet, StoryViewSet, DiscountCodeViewSet, PaymentViewSet, ViewerViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
#router.register(r'plans', PlanViewSet)
router.register(r'userplans', UserPlanViewSet)
router.register(r'Widgets', WidgetViewSet)
router.register(r'Storys', StoryViewSet)
router.register(r'discountcodes', DiscountCodeViewSet)
router.register(r'Payments', PaymentViewSet)
router.register(r'viewers', ViewerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('api/logout/', LogoutAPIView.as_view(), name='logout'),
    path('plans/', PlanListCreateAPIView.as_view(), name='plan-list-create'),
    path('plans/<int:pk>/', PlanRetrieveUpdateDestroyAPIView.as_view(), name='plan-detail'),
]

