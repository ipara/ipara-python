import json

from main.ipara_lib.Helper import Helper, HttpClient
from main.ipara_lib.configs import Configs


class BinNumberRequest:
    # Bin Sorgulama servisleri içerisinde kullanılacak olan bin numarasını temsil eder.
    binNumber = ""

    def __init__(self):
        pass

    def execute(self, req, configs):
        helper = Helper()
        configs.TransactionDate = helper.GetTransactionDateString()

        configs.HashString = configs.PrivateKey+req.binNumber+configs.TransactionDate;

        json_data = json.dumps(req.__dict__) # Json Serilestirme

        result = HttpClient.post(configs.BaseUrl+"/rest/payment/bin/lookup",
                                 helper.GetHttpHeaders(configs, helper.Application_json),json_data)
        return result
