from main.ipara_lib.Helper import Helper, HttpClient
import json


class BankCardCreateRequest():
    userId = ""
    cardOwnerName = ""
    cardNumber = ""
    cardAlias = ""
    cardExpireMonth = ""
    cardExpireYear = ""
    clientIp = ""

    '''
     Cüzdana kart ekleme istek metodur. Bu metod çeşitli kart bilgilerini ve settings sınıfı
     içerisinde bize özel olarak oluşan alanları kullanarak cüzdana bir kartı kaydetmemizi sağlar.
    '''
    def execute(self, req, configs):
        helper = Helper()
        configs.TransactionDate = helper.GetTransactionDateString()
        configs.HashString = configs.PrivateKey+req.userId+req.cardOwnerName+req.cardNumber+\
                             req.cardExpireMonth+req.cardExpireYear+req.clientIp+\
                             configs.TransactionDate
        json_data = json.dumps(req.__dict__) # Json Serilestirme

        result = HttpClient.post(configs.BaseUrl+"/bankcard/create",
                                 helper.GetHttpHeaders(configs, helper.Application_json),json_data)

        return result
