"""求人案件検索機能"""
from django.urls import path
from . import views


app_name = 'app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('api/', views.PostAiView.as_view(), name='api'),
    path('mock/', views.MockView.as_view(), name='mock'),
    path('list/', views.AiAnalysisLogList.as_view(), name='list'),
]
