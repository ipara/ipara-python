# coding=utf-8
import json

from main.ipara_lib.Helper import Helper, HttpClient
from main.ipara_lib.configs import Configs


class PaymentLinkCreateRequest:
    # Ödeme linki oluşturma servisi için gerekli olan servis girdi parametrelerini temsil eder.
    clientIp = ""
    name = ""
    surname = ""
    tcCertificate = ""
    taxNumber = ""
    email = ""
    gsm = ""
    amount = ""
    threeD = ""
    expireDate = ""
    sendEmail = ""
    mode = ""
    commissionType = ""

    def execute(self, req, configs):
        helper = Helper()
        configs.TransactionDate = helper.GetTransactionDateString()

        configs.HashString = configs.PrivateKey + req.name + req.surname + \
            req.email + req.amount + req.clientIp + configs.TransactionDate

        json_data = json.dumps(req.__dict__)  # Json Serilestirme

        result = HttpClient.post(configs.BaseUrl+"corporate/merchant/linkpayment/create",
                                 helper.GetHttpHeaders(configs, helper.Application_json), json_data)

        return result
