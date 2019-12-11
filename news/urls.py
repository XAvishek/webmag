from django.urls import path
from news import views
urlpatterns = [
    path('create/', views.CreateNewsView.as_view(), name='create_news'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('<str:category>/', views.NewsCategoryView.as_view(), name='category_news'),
    path('<str:category>/<int:pk>/<str:slug>/',views.NewsDetailView.as_view(), name='detail_news'),
    path('<str:category>/<int:pk>/<str:slug>/delete/',views.NewsDeleteView.as_view(), name='delete_news'),
    path('<str:category>/<int:pk>/<str:slug>/update/',views.NewsUpdateView.as_view(), name='update_news'),
    path('<str:category>/<int:pk>/<str:slug>/comment/',views.create_comment, name='create_comment'),

]
