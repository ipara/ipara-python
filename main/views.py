from django.shortcuts import render_to_response

from main.ipara_lib.configs import Configs
from main.ipara_lib.Helper import Helper
from main.ipara_lib.BankCardDeleteRequest import BankCardDeleteRequest
from main.ipara_lib.BankCardInquiryRequest import BankCardInquiryRequest
from main.ipara_lib.BinNumberRequest import BinNumberRequest
from main.ipara_lib.BankCardCreateRequest import BankCardCreateRequest
from main.ipara_lib.PaymentInquiryRequest import PaymentInquiryRequest
from main.ipara_lib.ThreedInitResponse import ThreedInitResponse
from main.ipara_lib.ThreedPaymentCompleteRequest import ThreedPaymentCompleteRequest
from main.ipara_lib.ThreedPaymentRequest import ThreedPaymentRequest
from main.ipara_lib.ApiPaymentRequest import ApiPaymentRequest

from random import *
import json

config = Configs(
    #"Public Magaza Anahtarı
    # size mağaza başvurunuz sonucunda gönderilen public key (açık anahtar) bilgisini kullanınız.",
    '',
    #"Private Magaza Anahtarı
    # size mağaza başvurunuz sonucunda gönderilen privaye key (gizli anahtar) bilgisini kullanınız.",
    '',
    #iPara web servisleri API url'lerinin başlangıç bilgisidir.
    # Restful web servis isteklerini takip eden kodlar halinde bulacaksınız.
    'https://api.ipara.com/', #BaseUrl
    'https://www.ipara.com/3dgate', #ThreeDInquiryUrl
    #Test -> T, entegrasyon testlerinin sırasında "T" modunu,
    # canlı sisteme entegre olarak ödeme almaya başlamak için ise Prod -> "P" modunu kullanınız.
    'T', #Mode
    '', #Echo
    #  Kullandığınız iPara API versiyonudur.
    '1.0',  #Version
    # Kullanacağınız hash bilgisini, bağlanmak istediğiniz web servis bilgisine göre doldurulmalıdır.
    # Bu bilgileri Entegrasyon rehberinin ilgili web servise ait bölümde bulabilirsiniz.
    '', #HashString
    '', #TransactionDate
)

# Ana Sayfamızda Ön Tanımlı Olarak 3D Ödeme Kısmı Gelmekte
def threeDPaymentRequest(request):
    message = ""
    xmlOutput = ""
    if request.POST:
        req = ThreedPaymentRequest()
        req.OrderId = str(randint(1, 10000))
        req.Echo = "Echo"
        req.Mode = config.Mode
        req.Version = config.Version
        req.Amount = "10000"
        req.CardOwnerName = request.POST.get('nameSurname')
        req.CardNumber = request.POST.get('cardNumber')
        req.CardExpireMonth = request.POST.get('month')
        req.CardExpireYear = request.POST.get('year')
        req.Installment = request.POST.get('installment')
        req.Cvc = request.POST.get('cvc')
        req.ThreeD = "true"
        req.UserId = ""
        req.CardId = ""
        req.PurchaserName = "Murat"
        req.PurchaserSurname = "Kaya"
        req.PurchaserEmail = "murat@kaya.com"
        req.SuccessUrl = "http://localhost:8000/threeDResultSuccess/"
        req.FailUrl = "http://localhost:8000/threeDResultFail/"

        # 3D formunun 1. Adımının başlatılması için istek çağrısının yapıldığı kısımdır.
        message = req.execute(req, config)
                
    return render_to_response('index.html', {'message': message})

# 3D Ödeme Sonucu Başarılı Olduğunda Çalışacak Kısım
def threeDResultSuccess(request):
    message = ""
    if request.POST:
        paymentResponse = ThreedInitResponse()
        paymentResponse.OrderId = request.POST.get('orderId')
        paymentResponse.Result = request.POST.get('result')
        paymentResponse.Amount = request.POST.get('amount')
        paymentResponse.Mode = request.POST.get('mode')

        if request.POST.get('errorCode') != "":
            paymentResponse.ErrorCode = request.POST.get('errorCode')
        if request.POST.get('transactionDate') != "":
            paymentResponse.TransactionDate = request.POST.get('transactionDate')
        if request.POST.get('hash') != "":
            paymentResponse.Hash = request.POST.get('hash')

        # Eğer İşlem 3D olarak Onaylandıysa
        # Sürecin İkinci Kısmını Çalıştırıyoruz
        helper = Helper()
        if helper.Validate3DReturn(paymentResponse, config):
            req = ThreedPaymentCompleteRequest()
            req.OrderId = request.POST.get('orderId')
            req.Echo = "Echo"
            req.Mode = config.Mode
            req.Amount = "10000"
            req.CardOwnerName = "Fatih Coşkun"
            req.CardNumber = "4282209027132016"
            req.CardExpireMonth = "05"
            req.CardExpireYear = "18"
            req.Installment = "1"
            req.Cvc = "000"
            req.ThreeD = "true"
            req.ThreeDSecureCode = request.POST.get('threeDSecureCode')
            req.UserId = ""
            req.CardId = ""

            # Sipariş veren bilgileri
            req.Purchaser = req.PurchaserClass()
            req.Purchaser.name = "Murat"
            req.Purchaser.surname = "Kaya"
            req.Purchaser.birthDate = "1986-07-11"
            req.Purchaser.email = "murat@kaya.com"
            req.Purchaser.gsmPhone = "5881231212"
            req.Purchaser.tcCertificate = "1234567890"
            req.Purchaser.clientIp = "127.0.0.1"

            # region Fatura bilgileri
            req.Purchaser.invoiceAddress = req.PurchaserAddress()
            req.Purchaser.invoiceAddress.name = "Murat"
            req.Purchaser.invoiceAddress.surname = "Kaya"
            req.Purchaser.invoiceAddress.address = "Mevlüt Pehlivan Mah. Multinet Plaza Şişli"
            req.Purchaser.invoiceAddress.zipCode = "34782"
            req.Purchaser.invoiceAddress.cityCode = "34"
            req.Purchaser.invoiceAddress.tcCertificate = "1234567890"
            req.Purchaser.invoiceAddress.country = "TR"
            req.Purchaser.invoiceAddress.taxNumber = "123456"
            req.Purchaser.invoiceAddress.taxOffice = "Kozyatağı"
            req.Purchaser.invoiceAddress.companyName = "iPara"
            req.Purchaser.invoiceAddress.phoneNumber = "2122222222"

            # region Kargo Adresi bilgileri
            req.Purchaser.shippingAddress = req.PurchaserAddress()
            req.Purchaser.shippingAddress.name = "Murat"
            req.Purchaser.shippingAddress.surname = "Kaya"
            req.Purchaser.shippingAddress.address = "Mevlüt Pehlivan Mah. Multinet Plaza Şişli"
            req.Purchaser.shippingAddress.zipCode = "34782"
            req.Purchaser.shippingAddress.cityCode = "34"
            req.Purchaser.shippingAddress.tcCertificate = "1234567890"
            req.Purchaser.shippingAddress.country = "TR"
            req.Purchaser.shippingAddress.phoneNumber = "2122222222"

            # Ürün Bilgileri
            req.Products = []
            product1 = req.Product()
            product1.title = "Telefon"
            product1.code = "TLF0001"
            product1.price = "5000"
            product1.quantity = "1"
            req.Products.append(product1)

            product2 = req.Product()
            product2.title = "Bilgisayar"
            product2.code = "BLG0001"
            product2.price = "5000"
            product2.quantity = "1"
            req.Products.append(product2)

            config.BaseUrl = "https://api.ipara.com/"
            # 3D formunun 2. Adımında ödeme işleminin tamamlanması için başlatılan istek
            # çağrısının yapıldığı kısımdır.
            message = Helper.formatXML(req.execute(req, config))
            
    return render_to_response('threeDResultSuccess.html', {'message': message})


#3D secure ödeme sonucu başarısız olup, hata mesajının son kullanıcıya gösterildiği kısımdır.
def threeDResultFail(request):
    if request.content_params != None:
        output = "<?xml version='1.0' encoding='UTF-8' ?>"
        output += "<authResponse>"
        if request.POST.get('echo') != "":
            output += "<echo>"+request.POST.get('echo') +"</echo>"
        if request.POST.get('result') != "":
            output += "<result>"+request.POST.get('result')+"</result>"
        if request.POST.get('amount') != "":
            output += "<amount>"+request.POST.get('amount')+"</amount>"
        if request.POST.get('publicKey') != "":
            output += "<publicKey>"+request.POST.get('publicKey')+"</publicKey>"
        if request.POST.get('orderId') != "":
            output += "<orderId>"+request.POST.get('orderId')+"</orderId>"
        if request.POST.get('mode') != "":
            output += "<mode>"+request.POST.get('mode')+"</mode>"
        if request.POST.get('errorCode') != "":
            output += "<errorCode>"+request.POST.get('errorCode')+"</errorCode>"
        if request.POST.get('errorMessage') != "":
            output += "<errorMessage>"+request.POST.get('errorMessage')+"</errorMessage>"
        output += "</authResponse>"
        output = Helper.formatXML(output)
    return render_to_response('threeDResultFail.html', {'message': output})


# 3D Olmadan Ödeme Örneği
def apiPaymentRequest(request):
    message = ""
    if request.POST:
        non3DPaymentRequest = ApiPaymentRequest()
        non3DPaymentRequest.Echo = "Echo"
        non3DPaymentRequest.Mode = config.Mode
        non3DPaymentRequest.ThreeD = "false"
        non3DPaymentRequest.OrderId = str(randint(1, 10000))
        non3DPaymentRequest.Amount = "10000"
        non3DPaymentRequest.CardOwnerName = request.POST.get('nameSurname')
        non3DPaymentRequest.CardNumber = request.POST.get('cardNumber')
        non3DPaymentRequest.CardExpireMonth = request.POST.get('month')
        non3DPaymentRequest.CardExpireYear = request.POST.get('year')
        non3DPaymentRequest.Installment = request.POST.get('installment')
        non3DPaymentRequest.Cvc = request.POST.get('cvc')
        non3DPaymentRequest.VendorId = ""
        non3DPaymentRequest.UserId = "123456"
        non3DPaymentRequest.CardId = ""
        non3DPaymentRequest.ThreeDSecureCode = ""

        non3DPaymentRequest.Purchaser = non3DPaymentRequest.PurchaserClass()
        non3DPaymentRequest.Purchaser.name = "Murat"
        non3DPaymentRequest.Purchaser.surname = "Kaya"
        non3DPaymentRequest.Purchaser.birthDate = "1986-07-11"
        non3DPaymentRequest.Purchaser.email = "mura@kaya.com"
        non3DPaymentRequest.Purchaser.gsmPhone = "5881231212"
        non3DPaymentRequest.Purchaser.tcCertificate = "58812312547"
        non3DPaymentRequest.Purchaser.clientIp = "127.0.0.1"

        # Fatura Bilgileri
        non3DPaymentRequest.Purchaser.invoiceAddress = non3DPaymentRequest.PurchaserAddress()
        non3DPaymentRequest.Purchaser.invoiceAddress.name = "Murat"
        non3DPaymentRequest.Purchaser.invoiceAddress.surname = "Kaya"
        non3DPaymentRequest.Purchaser.invoiceAddress.address = "Mevlüt Pehlivan Mah. Multinet Plaza Şişli"
        non3DPaymentRequest.Purchaser.invoiceAddress.zipCode = "34782"
        non3DPaymentRequest.Purchaser.invoiceAddress.cityCode = "34"
        non3DPaymentRequest.Purchaser.invoiceAddress.tcCertificate = "1234567890"
        non3DPaymentRequest.Purchaser.invoiceAddress.country = "TR"
        non3DPaymentRequest.Purchaser.invoiceAddress.taxNumber = "123456"
        non3DPaymentRequest.Purchaser.invoiceAddress.taxOffice = "Kozyatagi"
        non3DPaymentRequest.Purchaser.invoiceAddress.companyName = "iPara"
        non3DPaymentRequest.Purchaser.invoiceAddress.phoneNumber = "2122222222"

        # Kargo Bilgileri
        non3DPaymentRequest.Purchaser.shippingAddress = non3DPaymentRequest.PurchaserAddress()
        non3DPaymentRequest.Purchaser.shippingAddress.name = "Murat"
        non3DPaymentRequest.Purchaser.shippingAddress.surname = "Kaya"
        non3DPaymentRequest.Purchaser.shippingAddress.address = "Mevlüt Pehlivan Mah. Multinet Plaza Şişli"
        non3DPaymentRequest.Purchaser.shippingAddress.zipCode = "34782"
        non3DPaymentRequest.Purchaser.shippingAddress.cityCode = "34"
        non3DPaymentRequest.Purchaser.shippingAddress.tcCertificate = "1234567890"
        non3DPaymentRequest.Purchaser.shippingAddress.country = "TR"
        non3DPaymentRequest.Purchaser.shippingAddress.phoneNumber = "2122222222"

        # Ürün Bilgileri
        non3DPaymentRequest.Products = []
        product1 = non3DPaymentRequest.Product()
        product1.title = "Telefon"
        product1.code = "TLF0001"
        product1.price = "5000"
        product1.quantity = "1"
        non3DPaymentRequest.Products.append(product1)

        product2 = non3DPaymentRequest.Product()
        product2.title = "Bilgisayar"
        product2.code = "BLG0001"
        product2.price = "5000"
        product2.quantity = "1"
        non3DPaymentRequest.Products.append(product2)

        # API Cagrisi Yapiyoruz
        message = Helper.formatXML(non3DPaymentRequest.execute(non3DPaymentRequest, config))
                
    return render_to_response('apiPayment.html', {'message': message})


def paymentInquryRequest(request):
    message = ""
    if request.POST:
        req = PaymentInquiryRequest()
        req.orderId = request.POST.get('orderId')

        # ödeme sorgulama servisi api çağrısının yapıldığı kısımdır.
        message = Helper.formatXML(req.execute(req, config))

    return render_to_response('paymentInqury.html', {'message': message})


# Cüzdandaki Kartla Tek Tıkla Ödeme Yaptığımız Örnek
def apiPaymentWithWallet(request):
    message = ""
    if request.POST:
        req = ApiPaymentRequest()
        req.OrderId = str(randint(1, 10000))
        req.Echo = "Echo"
        req.Mode = config.Mode
        req.Amount = "10000"
        req.CardOwnerName = ""
        req.CardNumber = ""
        req.CardExpireMonth = ""
        req.CardExpireYear = ""
        req.Installment = ""
        req.Cvc = ""
        req.ThreeD = "false"
        req.UserId = request.POST.get('userId')
        req.CardId = request.POST.get('cardId')

        # Sipariş veren bilgileri
        req.Purchaser = req.PurchaserClass()
        req.Purchaser.name = "Murat"
        req.Purchaser.surname = "Kaya"
        req.Purchaser.birthDate = "1986-07-11"
        req.Purchaser.email = "murat@kaya.com"
        req.Purchaser.gsmPhone = "5889541011"
        req.Purchaser.tcCertificate = "1234567890"
        req.Purchaser.clientIp = "127.0.0.1"

        # Fatura bilgileri
        req.Purchaser.invoiceAddress = req.PurchaserAddress()
        req.Purchaser.invoiceAddress.name = "Murat"
        req.Purchaser.invoiceAddress.surname = "Kaya"
        req.Purchaser.invoiceAddress.address = "Mevlüt Pehlivan Mah. Multinet Plaza Şişli"
        req.Purchaser.invoiceAddress.zipCode = "34782"
        req.Purchaser.invoiceAddress.cityCode = "34"
        req.Purchaser.invoiceAddress.tcCertificate = "1234567890"
        req.Purchaser.invoiceAddress.country = "TR"
        req.Purchaser.invoiceAddress.phoneNumber = "2122222222"

        # Kargo adresi bilgileri
        req.Purchaser.shippingAddress = req.PurchaserAddress()
        req.Purchaser.shippingAddress.name = "Murat"
        req.Purchaser.shippingAddress.surname = "Kaya"
        req.Purchaser.shippingAddress.address = "Mevlüt Pehlivan Mah. Multinet Plaza Şişli"
        req.Purchaser.shippingAddress.zipCode = "34782"
        req.Purchaser.shippingAddress.cityCode = "34"
        req.Purchaser.shippingAddress.tcCertificate = "1234567890"
        req.Purchaser.shippingAddress.country = "TR"
        req.Purchaser.shippingAddress.phoneNumber = "2122222222"

        # Ürün Bilgileri
        req.Products = []
        product1 = req.Product()
        product1.title = "Telefon"
        product1.code = "TLF0001"
        product1.price = "5000"
        product1.quantity = "1"
        req.Products.append(product1)

        product2 = req.Product()
        product2.title = "Bilgisayar"
        product2.code = "BLG0001"
        product2.price = "5000"
        product2.quantity = "1"
        req.Products.append(product2)

        # Cüzdandaki kart ile ödeme yapma API çağrısının yapıldığı kısımdır.
        message = Helper.formatXML(req.execute(req, config))

    return render_to_response('apiPaymentWithWallet.html', {'message': message})


# Cüzdandaki Kartları Listelediğimiz Kısım
def getCardFromWallet(request):
    message = ""
    if request.POST:
        req = BankCardInquiryRequest()
        req.userId = request.POST.get('userId')
        req.cardId = request.POST.get('cardId')
        req.clientIp = "127.0.0.1"

        # Cüzdandan kartların getirildiği API cagrisini temsil etmektedir
        response = req.execute(req, config)
        message = json.dumps(json.loads(response), indent=4, ensure_ascii=False)

    return render_to_response('getCardFromWallet.html', {'message': message})


# Cüzdana Kart Eklediğimiz Kısım
def addCartToWallet(request):
    message = ""
    if request.POST:
        req = BankCardCreateRequest()
        req.userId = request.POST.get('userId')
        req.cardOwnerName = request.POST.get('nameSurname')
        req.cardNumber = request.POST.get('cardNumber')
        req.cardAlias = request.POST.get('cardAlias')
        req.cardExpireMonth = request.POST.get('month')
        req.cardExpireYear = request.POST.get('year')
        req.clientIp = "127.0.0.1"

        # Cüzdana kart eklemek için yapılan API cagrisini temsil etmektedir
        response = req.execute(req, config)
        message = json.dumps(json.loads(response), indent=4, ensure_ascii=False)

    return render_to_response('addCartToWallet.html', {'message': message})


# Cüzdandan Kart Sildiğimiz Kısım
def deleteCardFromWallet(request):
    message = ""
    if request.POST:
        req = BankCardDeleteRequest()
        req.userId = request.POST.get('userId')
        req.cardId = request.POST.get('cardId')
        req.clientIp = "127.0.0.1"

        # Cüzdanda bulunan karti silmek için yapılan API cagrisini temsil etmektedir
        response = req.execute(req, config)
        message = json.dumps(json.loads(response), indent=4, ensure_ascii=False)

    return render_to_response('deleteCardFromWallet.html', {'message': message})


# Bin İsteği Yaptığımız Kısım
def binRequest(request):
    message = ""
    if request.POST:
        req = BinNumberRequest()
        req.binNumber = request.POST.get('binNumber')

        # Bin istegi icin yapılan API cagrisini temsil etmektedir
        response = req.execute(req, config)
        message = json.dumps(json.loads(response), indent=4, ensure_ascii=False)

    return render_to_response('bininqury.html', {'message': message})
