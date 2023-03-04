from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView 

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('book', views.BookViewSet)
router.register('author', views.AuthorViewSet)
router.register('cart', views.CartViewSet)
router.register('cartitem', views.CartItemViewSet)
router.register('user', views.UserViewSet)





urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>/', views.post, name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>',views.AuthorDetailView.as_view(), name='author-detail'),
]

urlpatterns += [
    path('book/create/', views.create_book, name='book-create'),
    path('book/<int:pk>/addcart/', views.SaveCart, name ='add-cart'),
    path('cart/', views.CartView, name ='cart'),
]

urlpatterns +=[
    path('register/', views.register, name = 'register'),
]

urlpatterns +=[
    path('api/', include(router.urls)),
]