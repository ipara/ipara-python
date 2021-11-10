# coding=utf-8
import json

from main.ipara_lib.Helper import Helper, HttpClient
from main.ipara_lib.configs import Configs


class PaymentInquiryWithTimeRequest:
    # Tarihe göre ödeme sorgulama servisi için gerekli olan servis girdi parametrelerini temsil eder.
    mode = ""
    startDate = ""
    endDate = ""
    echo = ""

    def execute(self, req, configs):
        helper = Helper()
        configs.TransactionDate = helper.GetTransactionDateString()

        configs.HashString = configs.PrivateKey + configs.Mode + configs.TransactionDate

        json_data = json.dumps(req.__dict__)  # Json Serilestirme

        print(json_data)
        return HttpClient.post(configs.BaseUrl+"rest/payment/search",
                               helper.GetHttpHeaders(configs, helper.Application_json), json_data)