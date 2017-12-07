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

    '''
    Bu fonksiyon diğer fonksiyonların aksine 3D sınıfı bir formun post edilmesi ile başlar.
	Bundan dolayı bu fonksiyon "toHtmlString" metodunda ilgili HTML formu oluşturur ve geri döndürür.
	Bu metod sayesinde 3D ile ödeme formu başlatılmış olur.
    '''
    def execute(self, req, configs):
        helper = Helper()
        configs.TransactionDate = helper.GetTransactionDateString()
        configs.HashString = configs.PrivateKey+req.OrderId+req.Amount+req.Mode+req.CardOwnerName+\
                             req.CardNumber+req.CardExpireMonth+req.CardExpireYear+req.Cvc+req.UserId+\
                             req.CardId+req.PurchaserName+req.PurchaserSurname+\
                             req.PurchaserEmail+configs.TransactionDate

        req.Token = helper.CreateToken(configs.PublicKey, configs.HashString)

        return str(self.toHtmlString(req, configs))

    def toHtmlString(self, req, configs):
        builder = ""

        builder += "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0 Transitional//EN\">"
        builder += "<html>"
        builder += "<body>"
        builder += "<form action=\"" + configs.ThreeDInquiryUrl + "\" method=\"post\" id=\"three_d_form\">"
        builder += "<input type=\"hidden\" name=\"orderId\" value=\"" + req.OrderId + "\"/>"
        builder += "<input type=\"hidden\" name=\"amount\" value=\"" + req.Amount + "\"/>"
        builder += "<input type=\"hidden\" name=\"cardOwnerName\" value=\"" + req.CardOwnerName + "\"/>"
        builder += "<input type=\"hidden\" name=\"cardNumber\" value=\"" + req.CardNumber + "\"/>"
        builder += "<input type=\"hidden\" name=\"userId\" value=\"" + req.UserId + "\"/>"
        builder += "<input type=\"hidden\" name=\"cardId\" value=\"" + req.CardId + "\"/>"
        builder += "<input type=\"hidden\" name=\"cardExpireMonth\" value=\"" + req.CardExpireMonth + "\"/>"
        builder += "<input type=\"hidden\" name=\"cardExpireYear\" value=\"" + req.CardExpireYear + "\"/>"
        builder += "<input type=\"hidden\" name=\"installment\" value=\"" + req.Installment + "\"/>"
        builder += "<input type=\"hidden\" name=\"cardCvc\" value=\"" + req.Cvc + "\"/>"
        builder += "<input type=\"hidden\" name=\"mode\" value=\"" + req.Mode + "\"/>"
        builder += "<input type=\"hidden\" name=\"purchaserName\" value=\"" + req.PurchaserName + "\"/>"
        builder += "<input type=\"hidden\" name=\"purchaserSurname\" value=\"" + req.PurchaserSurname + "\"/>"
        builder += "<input type=\"hidden\" name=\"purchaserEmail\" value=\"" + req.PurchaserEmail + "\"/>"
        builder += "<input type=\"hidden\" name=\"successUrl\" value=\"" + req.SuccessUrl + "\"/>"
        builder += "<input type=\"hidden\" name=\"failureUrl\" value=\"" + req.FailUrl + "\"/>"
        builder += "<input type=\"hidden\" name=\"echo\" value=\"" + req.Echo + "\"/>"
        builder += "<input type=\"hidden\" name=\"version\" value=\"" + req.Version + "\"/>"
        builder += "<input type=\"hidden\" name=\"transactionDate\" value=\"" + configs.TransactionDate + "\"/>"
        builder += "<input type=\"hidden\" name=\"token\" value=\"" + req.Token + "\"/>"
        builder += "<input type=\"submit\" value=\"Öde\" style=\"display:none\"/>"
        builder += "<noscript>"
        builder += "<br/>"
        builder += "<br/>"
        builder += "<center>"
        builder += "<h1>3D Secure Yönlendirme İşlemi</h1>"
        builder += "<h2>Javascript internet tarayıcınızda kapatılmış veya desteklenmiyor.<br/></h2>"
        builder += "<h3>Lütfen banka 3D Secure sayfasına yönlenmek için tıklayınız.</h3>"
        builder += "<input type=\"submit\" value=\"3D Secure Sayfasına Yönlen\">"
        builder += "</center>"
        builder += "</noscript>"
        builder += "</form>"
        builder += "</body>"
        builder += "<script>document.getElementById(\"three_d_form\").submit()</script>"
        builder += "</html>"

        return builder
