



from django.urls import path
from .apis import RegisterApi, UserApi, VerifyPhoneRequestApi, VerifyEmailRequestApi, VerfiyPhoneApi, VerifyEmailApi, \
    ChangePasswordRequestApi, ChangePasswordApi, AddressApi, AddressDetailApi, AddressListApi, FavoriteProductApi, \
    FavoriteProductDetailApi, FavoriteProductListApi, ContactFormApi, ContactFormDetailAdminApi, \
    ContactFormListAdminApi, UserListApi, UserRegisterReport

urlpatterns = [
    path('register/', RegisterApi.as_view(), name="register"),
    path('user/', UserApi.as_view(), name="user"),
    path('request-verify-phone/', VerifyPhoneRequestApi.as_view(), name='request-phone-otp'),
    path('requset-verify-emali/', VerifyEmailRequestApi.as_view(), name='request-verify-email'),
    path('requset-change-password/', ChangePasswordRequestApi.as_view(), name='request-change-password'),
    path('verify-phone/', VerfiyPhoneApi.as_view(), name='verify-phone'),
    path('verify-email/', VerifyEmailApi.as_view(), name='verify-emali'),
    path('change-password/', ChangePasswordApi.as_view(), name='change-password'),
    path("create-address/", AddressApi.as_view(), name='create-address'),
    path("address-detail/<int:id>/", AddressDetailApi.as_view(), name="address-detail"),
    path("address-list-user/", AddressListApi.as_view(), name="address-list"),
    path("add-favorite-product/", FavoriteProductApi.as_view(), name="add-favorite-product"),
    path("remove-favorite-product/<int:id>/", FavoriteProductDetailApi.as_view(), name="remove-favorite-product"),
    path("favorite-product-list/", FavoriteProductListApi.as_view(), name="favorite-product-list"),
    path("create-contanct-form/" , ContactFormApi.as_view() , name = "create-contact-form"),
    path("contact-form-detail/<int:id>/" , ContactFormDetailAdminApi.as_view() , name= "contact-form-detail"),
    path("contact-form-list-admin/" , ContactFormListAdminApi.as_view() , name= "contact-form-list-admin"),
    path("user-list/" , UserListApi.as_view()  , name="user-list-admin"),
    path("user-register-report/" , UserRegisterReport.as_view(),name = "user-register-report"),








]
