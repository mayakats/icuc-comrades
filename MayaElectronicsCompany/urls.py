from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from MayaElectronics.views import (
    index_view, services_view, aboutus_view, products_view, gallery_view,
    CartItemDetailView, CartItemView, add_like, add_dislike, contactus_view,
    display_data_view, update_user_view, edit_user_view, delete_user_view,
    products_list_view, UserViewSet, login_view, logout_view, order_page,
    ProductListView, ProductFilterView, ProductCreateView, ProductUpdateView, ProductRetrieveView, ProductDestroyView, RegisterApiView, LoginApiView, ActivationView, LikeView, FeedbackListCreateView, FeedbackDetailView
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'User', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls,),
    path('', index_view, name='index_page'),
    path('services/', services_view, name='services_page'),
    path('aboutus/', aboutus_view, name='aboutus_page'),
    path('products/', products_view, name='products_page'),
    path('gallery/', gallery_view, name='gallery_page'),
    path('api/cart-items/', CartItemView.as_view(), name='cart-item-list'),
    path('api/cart-items/<int:pk>/', CartItemDetailView.as_view(), name='cart-item-detail'),
    path('contactus/', contactus_view, name='contactus_page'),
    path('display_data/', display_data_view, name='display_data_page'),
    path('update_user/<int:user_id>/', update_user_view, name='update_user_page'),
    path('edit_user/<int:user_id>/', edit_user_view, name='edit_user_page'),
    path('delete_user/<int:user_id>/', delete_user_view, name='delete_user_page'),
    path('order/', order_page, name='order_page'),
    path('products_list/', products_list_view, name='products_list_page'),
    path('', ProductListView.as_view(), name='product-list'),
    path('search/', ProductFilterView.as_view()),
    path('create/', ProductCreateView.as_view()),
    path('update/<int:pk>/', ProductUpdateView.as_view()),
    path('<int:pk>/', ProductRetrieveView.as_view()),
    path('delete/<int:pk>/', ProductDestroyView.as_view()),
    path('register/', RegisterApiView.as_view(), name='register-api'),
    path('login/', LoginApiView.as_view(), name='login-api'),
    path('activate/<uuid:activation_code>/', ActivationView.as_view(), name='activate_account'),
    path('activate/<uuid:activation_code>/', ActivationView.as_view(), name='activate-account'),
    path('', LikeView.as_view(), name='like-view'),
    path('activate/<uuid:activation_code>/', ActivationView.as_view(), name='activate_account'),
    path('', FeedbackListCreateView.as_view(), name='feedback-list-create'),
     path('<int:pk>/', FeedbackDetailView.as_view(), name='feedback-detail'),
    path('add-like/<int:pk>/', add_like),
    path('add-dislike/<int:pk>/', add_dislike),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', include(router.urls)),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
]

admin.site.site_header = 'Admin Login'                   # default: "Django Administration"
admin.site.index_title = 'Features area'                 # default: "Site administration"
admin.site.site_title = 'Admin_Login' # default: "Django site admin"

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
