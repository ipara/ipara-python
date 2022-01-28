# coding=utf-8
import json

from main.ipara_lib.Helper import Helper, HttpClient
from main.ipara_lib.configs import Configs


class PaymentLinkInquiryRequest:
    # Ödeme linki sorgulama servisi için gerekli olan servis girdi parametrelerini temsil eder.
    clientIp = ""
    email = ""
    gsm = ""
    linkId = ""
    linkState = ""
    startDate = ""
    endDate = ""
    pageSize = ""
    pageIndex = ""

    def execute(self, req, configs):
        helper = Helper()
        configs.TransactionDate = helper.GetTransactionDateString()

        configs.HashString = configs.PrivateKey + \
            req.clientIp + configs.TransactionDate

        json_data = json.dumps(req.__dict__)  # Json Serilestirme

        result = HttpClient.post(configs.BaseUrl+"corporate/merchant/linkpayment/list",
                                 helper.GetHttpHeaders(configs, helper.Application_json), json_data)

        return result
