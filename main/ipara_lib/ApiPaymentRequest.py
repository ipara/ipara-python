from main.ipara_lib.Helper import Helper, HttpClient
from xml.etree.ElementTree import Element, SubElement, tostring


class ApiPaymentRequest(object):
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
    VendorId = ""
    UserId = ""
    CardId = ""
    ThreeDSecureCode = ""
    Products = ""
    Purchaser = ""

    def convert_to_xml(self, req, settings):
        main_root = Element('auth', encoding='UTF-8')

        cardOwnerName = SubElement(main_root, 'cardOwnerName')
        cardOwnerName.text = req.CardOwnerName
        cardNumber = SubElement(main_root, 'cardNumber')
        cardNumber.text = req.CardNumber
        cardExpireMonth = SubElement(main_root, 'cardExpireMonth')
        cardExpireMonth.text = req.CardExpireMonth
        cardExpireYear = SubElement(main_root, 'cardExpireYear')
        cardExpireYear.text = req.CardExpireYear
        cardCvc = SubElement(main_root, 'cardCvc')
        cardCvc.text = req.Cvc
        userId = SubElement(main_root, 'userId')
        userId.text = req.UserId
        cardId = SubElement(main_root, 'cardId')
        cardId.text = req.CardId
        installment = SubElement(main_root, 'installment')
        installment.text =  req.Installment
        threeD = SubElement(main_root, 'threeD')
        threeD.text = req.ThreeD
        orderId = SubElement(main_root, 'orderId')
        orderId.text = req.OrderId
        echo = SubElement(main_root, 'echo')
        echo.text = req.Echo
        amount = SubElement(main_root, 'amount')
        amount.text = req.Amount
        mode = SubElement(main_root, 'mode')
        mode.text = req.Mode

        products = SubElement(main_root, 'products')
        for product in req.Products:
            product_root = SubElement(products, 'product')
            productCode = SubElement(product_root, 'productCode')
            productCode.text = product.code
            productName = SubElement(product_root, 'productName')
            productName.text = product.title
            quantity = SubElement(product_root, 'quantity')
            quantity.text = product.quantity
            price = SubElement(product_root, 'price')
            price.text = product.price

        purchaser_root = SubElement(main_root, 'purchaser')
        name = SubElement(purchaser_root, 'name')
        name.text = req.Purchaser.name
        surname = SubElement(purchaser_root, 'surname')
        surname.text = req.Purchaser.surname
        email = SubElement(purchaser_root, 'email')
        email.text = req.Purchaser.email
        clientIp = SubElement(purchaser_root, 'clientIp')
        clientIp.text = req.Purchaser.clientIp
        birthDate = SubElement(purchaser_root, 'birthDate')
        birthDate.text = req.Purchaser.birthDate
        gsmNumber = SubElement(purchaser_root, 'gsmNumber')
        gsmNumber.text = req.Purchaser.gsmPhone
        tcCertificate = SubElement(purchaser_root, 'tcCertificate')
        tcCertificate.text = req.Purchaser.tcCertificate

        invoiceAddress = SubElement(purchaser_root, 'invoiceAddress')
        iname = SubElement(invoiceAddress, 'name')
        iname.text = req.Purchaser.invoiceAddress.name
        isurname = SubElement(invoiceAddress, 'surname')
        isurname.text = req.Purchaser.invoiceAddress.surname
        iaddress = SubElement(invoiceAddress, 'address')
        iaddress.text = req.Purchaser.invoiceAddress.address
        izipcode = SubElement(invoiceAddress, 'zipcode')
        izipcode.text = req.Purchaser.invoiceAddress.zipCode
        icity = SubElement(invoiceAddress, 'city')
        icity.text = req.Purchaser.invoiceAddress.cityCode
        itcCertificate = SubElement(invoiceAddress, 'tcCertificate')
        itcCertificate.text = req.Purchaser.invoiceAddress.tcCertificate
        icountry = SubElement(invoiceAddress, 'country')
        icountry.text = req.Purchaser.invoiceAddress.country
        itaxNumber = SubElement(invoiceAddress, 'taxNumber')
        itaxNumber.text = req.Purchaser.invoiceAddress.taxNumber
        itaxOffice = SubElement(invoiceAddress, 'taxOffice')
        itaxOffice.text = req.Purchaser.invoiceAddress.taxOffice
        icompanyName = SubElement(invoiceAddress, 'companyName')
        icompanyName.text = req.Purchaser.invoiceAddress.companyName
        iphoneNumber = SubElement(invoiceAddress, 'phoneNumber')
        iphoneNumber.text = req.Purchaser.invoiceAddress.phoneNumber

        shippingAddress = SubElement(purchaser_root, 'shippingAddress')
        sname = SubElement(shippingAddress, 'name')
        sname.text = req.Purchaser.shippingAddress.name
        ssurname = SubElement(shippingAddress, 'surname')
        ssurname.text = req.Purchaser.shippingAddress.surname
        saddress = SubElement(shippingAddress, 'address')
        saddress.text = req.Purchaser.shippingAddress.address
        szipcode = SubElement(shippingAddress, 'zipcode')
        szipcode.text = req.Purchaser.shippingAddress.zipCode
        scity = SubElement(shippingAddress, 'city')
        scity.text = req.Purchaser.shippingAddress.cityCode
        scountry = SubElement(shippingAddress, 'country')
        scountry.text = req.Purchaser.shippingAddress.country
        sphoneNumber = SubElement(shippingAddress, 'phoneNumber')
        sphoneNumber.text = req.Purchaser.shippingAddress.phoneNumber

        xml_string = "<?xml version='1.0' encoding='UTF-8'?>"

        myresult = tostring(main_root).decode('utf-8')
        print(xml_string+myresult)

        return (xml_string+myresult)

    # 3D Secure Olmadan Odeme Servis cagsirini temsil eder.
    def execute(self, req, configs):
        helper = Helper()
        configs.TransactionDate = helper.GetTransactionDateString()

        configs.HashString = configs.PrivateKey + req.OrderId + req.Amount + req.Mode+\
            req.CardOwnerName + req.CardNumber + req.CardExpireMonth + req.CardExpireYear +\
            req.Cvc + req.UserId + req.CardId + req.Purchaser.name + req.Purchaser.surname +\
            req.Purchaser.email + configs.TransactionDate
            
        result = HttpClient.post(configs.BaseUrl+"rest/payment/auth",\
                                 helper.GetHttpHeaders(configs, helper.Application_xml),\
                                 self.convert_to_xml(req, configs))
        
        return result

    # Bu sınıf cüzdana kart ekleme servisi isteği sonucunda ve cüzdandaki kartları getir
    # isteği sonucunda bize döndürülen alanları temsil eder.
    class BankCard:
        cardId = ""
        maskNumber = ""
        alias = ""
        bankId = ""
        bankName = ""
        cardFamilyName = ""
        supportsInstallment = ""
        supportedInstallments = ""
        Type = ""
        serviceProvider = ""
        threeDSecureMandatory = ""
        cvcMandatory = ""

        def __init__(self):
            pass

    # Bu sınıf 3D secure olmadan ödeme kısmında ürün bilgisinin kullanılacağı yerde
    # ve 3D secure ile ödemenin 2. adamında ürün bilgisinin istendiği yerde kullanılır.
    class PurchaserAddress:
        name = ""
        surname = ""
        address = ""
        zipCode = ""
        cityCode = ""
        tcCertificate = ""
        country = ""
        taxNumber = ""
        taxOffice = ""
        companyName = ""
        phoneNumber = ""

        def __init__(self):
            pass

    # Bu sınıf 3D secure olmadan ödeme kısmında ürün bilgisinin kullanılacağı yerde
    # ve 3D secure ile ödemenin 2. adamında ürün bilgisinin istendiği yerde kullanılır.
    class Product:
        code = ""
        title = ""
        quantity = ""
        price = ""


    # Bu sınıf 3D secure olmadan ödeme kısmında ürün bilgisinin kullanılacağı yerde
    # ve 3D secure ile ödemenin 2. adamında ürün bilgisinin istendiği yerde kullanılır.
    class PurchaserClass:
        name = ""
        surname = ""
        birthDate = ""
        email = ""
        gsmPhone = ""
        tcCertificate = ""
        clientIp = ""
        invoiceAddress = ""
        shippingAddress = ""


    # Bu sınıf 3D Secure ile Ödeme işlemlerinin 1. ve 2. adımında kullanılan parametreleri temsil eder.
    class IparaAuth:
        threeD = ""
        orderId = ""
        amount = ""
        echo = ""
        cardOwnerName = ""
        cardNumber = ""
        cardExpireYear = ""
        installment = ""
        cvc = ""
        mode = ""
        vendorId = ""
        threeDSecureCode = ""
        products = ""
        purchaser = ""
