from django.urls import path

from . import views


app_name = 'catalog'

urlpatterns = [

    path("filter/", views.FilterBrendsView.as_view(), name='filter'),
    path("search/", views.Search.as_view(), name='search'),
    path("<slug:category_slug>/json-filter/", views.JsonFilterBrendsView.as_view(), name='json-filter'),
    path("quickview/<int:id>/", views.QuickView.as_view() ),
    path("parent/<int:id>/", views.ParentProducts.as_view()),
    path("<int:id>/<slug:slug>/", views.product_detail, name='product_detail'),
    path("grid/", views.ProductListView.as_view()),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    #path("review/<int:pk>/", views.add_review, name="add_review"),
    path('', views.product_main),
    path("<slug:category_slug>/", views.product_grid),
    path("<slug:category_slug>/f/",views.product_filter, name='product_filter'),



]
