# coding=utf-8
import json

from main.ipara_lib.Helper import Helper, HttpClient
from main.ipara_lib.configs import Configs


class BankCardInquiryRequest:
    # Cüzdanda bulunan kartları getirmek için gerekli olan servis girdi
    # parametrelerini temsil eder.
    userId = ""
    cardId = ""
    clientIp = ""

    # Mağazanın, cüzdanda bulunan kartları getirmek için kullandığı servisi temsil eder.
    def execute(self, req, configs):
        helper = Helper()
        configs.TransactionDate = helper.GetTransactionDateString()

        configs.HashString = configs.PrivateKey+req.userId+req.cardId+req.clientIp+\
            configs.TransactionDate

        json_data = json.dumps(req.__dict__) # Json Serilestirme

        return HttpClient.post(configs.BaseUrl+"/bankcard/inquiry",
                               helper.GetHttpHeaders(configs, helper.Application_json),json_data)
