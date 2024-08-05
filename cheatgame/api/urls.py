from django.urls import path, include

urlpatterns = [
    path('auth/', include('cheatgame.authentication.urls'), name='auth'),
    path('user/', include('cheatgame.users.urls'), name='user'),
    path('product/', include('cheatgame.product.urls'), name="product"),
    path("general/", include("cheatgame.general.urls"), name="general"),
    path("shop/", include("cheatgame.shop.urls"), name="shop"),
    path("issue/", include("cheatgame.issue.urls"), name="issue")

]
