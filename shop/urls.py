from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('category/<str:category_id>/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
      path('admin/', views.index, name='index'),
     path('get_data/', views.get_data, name='get_data'),
    path('add_row/', views.add_row, name='add_row'),
    path('delete_row/', views.delete_row, name='delete_row'),
    path('reorder_rows/', views.reorder_rows, name='reorder_rows'),
    path('insert_row_at_index/', views.add_row_at_index, name='insert_row_at_index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
]
