# coding=utf-8
import json

from main.ipara_lib.Helper import Helper, HttpClient
from main.ipara_lib.configs import Configs


class PaymentRefundInquiryRequest:
    # Ödeme iade sorgulama servisi için gerekli olan servis girdi parametrelerini temsil eder.
    clientIp = ""
    orderId = ""
    amount = ""

    def execute(self, req, configs):
        helper = Helper()
        configs.TransactionDate = helper.GetTransactionDateString()

        configs.HashString = configs.PrivateKey + \
            req.orderId + req.clientIp + configs.TransactionDate

        json_data = json.dumps(req.__dict__)  # Json Serilestirme

        result = HttpClient.post(configs.BaseUrl+"corporate/payment/refund/inquiry",
                                 helper.GetHttpHeaders(configs, helper.Application_json), json_data)

        return result
