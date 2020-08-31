from django.urls import path
from . import views

urlpatterns = [
    # 设置商品参数 类似{good_id}/进入商品详情页
    path('phone/', views.phone)
]