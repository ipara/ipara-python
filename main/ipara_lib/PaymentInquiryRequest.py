from main.ipara_lib.Helper import Helper, HttpClient
from main.ipara_lib.configs import Configs


class PaymentInquiryRequest:
    # Ödeme sorugulama servisi için gerekli olan servis girdi parametrelerini temsil eder.
    orderId = ""

    def execute(self, req, configs):
        helper = Helper()
        configs.TransactionDate = helper.GetTransactionDateString()

        configs.HashString = configs.PrivateKey+req.orderId+configs.Mode+configs.TransactionDate

        return HttpClient.post(configs.BaseUrl+"rest/payment/inquiry",
                               helper.GetHttpHeaders(configs, helper.Application_xml),self.to_xml(req, configs))

    def to_xml(self, req, configs):
        return "<?xml version='1.0' encoding='UTF-8' ?><inquiry><orderId>"+\
               req.orderId+"</orderId><echo>"+configs.Echo+"</echo><mode>"+ \
               configs.Mode+"</mode></inquiry>"
