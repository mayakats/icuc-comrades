from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from MayaElectronics.views import (
    index_view, aboutus_view, products_list_view, gallery_view,  
    CartItemDetailView, CartItemView, contactus_view,product_detail_view,
    update_user_view, add_to_cart, remove_from_cart, cart_view, edit_user_view, delete_user_view,
     UserViewSet, login_view, logout_view, order_page, cart_view, 
    ProductListView, ProductFilterView, ProductCreateView, ProductUpdateView, ProductDestroyView, FeedbackListCreateView, FeedbackDetailView
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'User', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls,),
    path('', index_view, name='index_page'),
    path('aboutus/', aboutus_view, name='aboutus_page'),
    path('gallery/', gallery_view, name='gallery_page'),
    path('api/cart-items/', CartItemView.as_view(), name='cart-item-list'),
    path('api/cart-items/<int:pk>/', CartItemDetailView.as_view(), name='cart-item-detail'),
    path('contactus/', contactus_view, name='contactus_page'),
    path('update_user/<int:user_id>/', update_user_view, name='update_user_page'),
    path('edit_user/<int:user_id>/', edit_user_view, name='edit_user_page'),
    path('delete_user/<int:user_id>/', delete_user_view, name='delete_user_page'),
    path('order/', order_page, name='order_page'),
      path('product/<int:product_id>/', product_detail_view, name='product_detail'),
    path('', ProductListView.as_view(), name='product-list'),
    path('search/', ProductFilterView.as_view()),
    path('create/', ProductCreateView.as_view()),
    path('update/<int:pk>/', ProductUpdateView.as_view()),
    path('delete/<int:pk>/', ProductDestroyView.as_view()),
    path('', FeedbackListCreateView.as_view(), name='feedback-list-create'),
    path('<int:pk>/', FeedbackDetailView.as_view(), name='feedback-detail'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', include(router.urls)),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('products/', products_list_view, name='products_list_page'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/', cart_view, name='cart_view'),
    
]

admin.site.site_header = 'Admin Login'                   # default: "Django Administration"
admin.site.index_title = 'Features area'                 # default: "Site administration"
admin.site.site_title = 'Admin_Login' # default: "Django site admin"

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
