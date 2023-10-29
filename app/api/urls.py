import api.v1 as v1
from django.urls import path

urlpatterns = [
    path('categories',
         v1.CategoriesView.as_view()),
    path('change-password', v1.changePasswordView),
    path('login', v1.loginView),
    path('login-confirm', v1.loginConfirmView),
    path('personal-info', v1.CustomerPersonalInfoView.as_view()),
    path('basket', v1.BasketView.as_view()),
    path('basket-reset', v1.clearBasket),
    path('basket-update-count', v1.basketSetCount),
    path('info', v1.HelpfulInfoListView.as_view()),
    path('info/<str:key>', v1.HelpfulInfoDetailView.as_view()),
    path('setting', v1.SettingView.as_view()),
    path('registry', v1.registrySendCodeView),
    path('registry-confirm', v1.registryConfirmView),
    path('registry-resend-code', v1.registryResendCodeView),
    path('check-token', v1.checkTokenView),
    path('cities', v1.CityListView.as_view()),
    path('products', v1.ProductListView.as_view()),
    path('make-support-request', v1.makeSupportRequestView),
    path('my-bonuses', v1.myBonusesView),
    path('cancel-deletion', v1.cancelDeletionView),
]

well_known = [
    path('assetlinks.json', v1.AndroidAppSiteAssociationView),
    path('apple-app-site-association', v1.AppleAppSiteAssociationView),
]
