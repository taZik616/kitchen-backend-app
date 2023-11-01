from .add_address import addAddressView, changeAddressView
from .address_geo_suggest import addressByCoordsView, addressGeoSuggestView
from .app_links_association import (
    AndroidAppSiteAssociationView,
    AppleAppSiteAssociationView,
)
from .basket import BasketView, basketSetCount, clearBasket
from .category import CategoriesView
from .change_password import changePasswordView
from .check_token import checkTokenView
from .cities import CityListView
from .helpful_info import HelpfulInfoDetailView, HelpfulInfoListView
from .login import loginConfirmView, loginView
from .my_bonuses import myBonusesView
from .personal_info import CustomerPersonalInfoView, cancelDeletionView
from .product import ProductListView
from .registry import registryConfirmView, registryResendCodeView, registrySendCodeView
from .setting import SettingView
from .support_request import makeSupportRequestView
