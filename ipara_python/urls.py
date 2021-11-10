"""ipara_python URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from main.views import *

urlpatterns = [
    url(r'^$', threedPaymentRequest, name='threedPaymentRequest'),
    url(r'^nonThreeDPayment/', nonThreeDPaymentRequest, name='nonThreeDPayment'),
    url(r'^paymentInquiry/', paymentInquiryRequest, name='paymentInquiry'),
    url(r'^paymentInquiryWithTime/', paymentInquiryWithTimeRequest,
        name='paymentInquiryWithTime'),
    url(r'^paymentLinkDelete/', paymentLinkDeleteRequest, name='paymentLinkDelete'),
    url(r'^paymentLinkCreate/', paymentLinkCreateRequest, name='paymentLinkCreate'),
    url(r'^paymentLinkInquiry/', paymentLinkInquiryRequest,
        name='paymentLinkInquiry'),
    url(r'^paymentRefundInquiry/', paymentRefundInquiryRequest,
        name='paymentRefundInquiry'),
    url(r'^paymentRefund/', paymentRefundRequest, name='paymentRefund'),
    url(r'^getCardFromWallet/', getCardFromWallet, name='getCardFromWallet'),
    url(r'^addCartToWallet/', addCartToWallet, name='addCartToWallet'),
    url(r'^deleteCardFromWallet/', deleteCardFromWallet,
        name='deleteCardFromWallet'),
    url(r'^binRequest/', binRequest, name='binRequest'),
    url(r'^nonThreeDPaymentWithWallet/', nonThreeDPaymentWithWallet,
        name='nonThreeDPaymentWithWallet'),
    url(r'^admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
