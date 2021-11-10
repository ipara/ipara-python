# coding=utf-8
import json
from main.ipara_lib.Helper import Helper


class ThreedPaymentRequest:
    Echo = ""
    Mode = ""
    ThreeD = ""
    OrderId = ""
    Amount = ""
    CardOwnerName = ""
    CardNumber = ""
    CardExpireMonth = ""
    CardExpireYear = ""
    Installment = ""
    Cvc = ""
    PurchaserName = ""
    PurchaserSurname = ""
    PurchaserEmail = ""
    SuccessUrl = ""
    FailUrl = ""
    Version = ""
    TransactionDate = ""
    Token = ""
    VendorId = ""
    UserId = ""
    CardId = ""
    FormInput = ""

    def execute(self, req, configs):
        helper = Helper()
        configs.TransactionDate = helper.GetTransactionDateString()
        configs.HashString = configs.PrivateKey+req.OrderId+req.Amount+req.Mode+req.CardOwnerName +\
            req.CardNumber+req.CardExpireMonth+req.CardExpireYear+req.Cvc+req.UserId +\
            req.CardId+req.PurchaserName+req.PurchaserSurname +\
            req.PurchaserEmail+configs.TransactionDate

        req.Token = helper.CreateToken(configs.PublicKey, configs.HashString)

        formInput = json.dumps({
            'orderId': req.OrderId,
            'cardOwnerName': req.CardOwnerName,
            'cardNumber': req.CardNumber,
            'cardExpireMonth': req.CardExpireMonth,
            'cardExpireYear': req.CardExpireYear,
            'cardCvc': req.Cvc,
            'userId': req.UserId,
            'cardId': req.CardId,
            'installment': '1',
            'amount': req.Amount,
            'echo': '',
            'language': 'tr-TR',
            'purchaser': {
                'name': req.PurchaserName,
                'surname': req.PurchaserSurname,
                'email': req.PurchaserEmail,
                'clientIp': '127.0.0.1',
            },
            'products': [
                {
                    'productCode': 'Bilgisayar',
                    'productName': 'BLG0001',
                    'quantity': '1',
                    'price': '5000',
                },
                {
                    'productCode': 'TLF0001',
                    'productName': 'Telefon',
                    'quantity': '1',
                    'price': '5000',
                },
            ],
            'successUrl': req.SuccessUrl,
            'failureUrl': req.FailUrl,
            'mode': req.Mode,
            'version': req.Version,
            'transactionDate': configs.TransactionDate,
            'token': req.Token,
        })

        return str(self.toHtmlString(formInput))

    def toHtmlString(self, formInput):
        return(
            '<!DOCTYPE html>' + "<html lang='en'>" + '<head>' +
            "<meta charset='UTF-8' />" +
            "<meta name='viewport' content='width=device-width, initial-scale=1.0' />" +
            '</head>' + '<body>' +
            "<form action='https://api.ipara.com/rest/payment/threed' method='POST' id='iParaMerchantRequestForm'>" +
            "<input id='token' type='hidden' name='parameters' value='" +
            formInput + "' />" + '</form>' + '<script>' +
            "document.getElementById('iParaMerchantRequestForm').submit();" +
            '</script>' + '</body>' + '</html>'
        )
