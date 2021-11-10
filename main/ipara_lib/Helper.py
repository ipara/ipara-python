# coding=utf-8
import hashlib
import datetime
import base64
import requests
import xml.dom.minidom as MND
import pytz


class Helper(object):
    TransactionDate = "transactionDate"
    Version = "version"
    Token = "token"
    Accept = "Accept"
    Application_xml = "application/xml"
    Application_json = "application/json"

    '''
    Doğru formatta tarih döndüren yardımcı sınıftır. Isteklerde tarih istenen noktalarda bu fonksiyon sonucu kullanılır.
	Servis çağrılarında kullanılacak istek zamanı için istenen tarih formatında bu fonksiyon kullanılmalıdır.
    Bu fonksiyon verdiğimiz tarih değerini iParanın bizden beklemiş olduğu tarih formatına değiştirmektedir.
    '''

    def GetTransactionDateString(self):
        d = datetime.datetime.now(pytz.timezone('Asia/Bahrain'))
        return d.strftime("%Y-%m-%d %H:%M:%S")

    # Parametre olarak verilen key bilgisini Sha1 algoritmasıyla hasleyerek geri döndürür.
    def Sha1Creator(self, key):
        return hashlib.sha1(str(key).encode('utf-8')).hexdigest()

    '''
    Çağrılarda kullanılacak Tokenları oluşturan yardımcı metotdur.
	İstek güvenlik bilgisi kullanılacak tüm çağrılarda token oluşturmamız gerekmektedir.
	Token oluştururken hash bilgisi ve public key alanlarının parametre olarak gönderilmesi gerekmektedir.
	hashstring alanı servise ait birden fazla alanın birleşmesi sonucu oluşan verileri ve public key mağaza açık anahtarını
    kullanarak bizlere token üretmemizi sağlar.
    '''

    def CreateToken(self, publicKey, hashString):
        encoded = hashlib.sha1(hashString.encode('utf-8')).digest()
        encoded = base64.b64encode(encoded)
        print(publicKey+':'+encoded.decode('utf-8'))
        return publicKey+':'+encoded.decode('utf-8')
    '''
    Verilen string i SHA1 ile hashleyip Base64 formatına çeviren fonksiyondur.
    CreateToken dan farklı olarak token oluşturmaz sadece hash hesaplar
    '''

    def ComputeHash(self, hashString):
        encoded = hashlib.sha1(hashString.encode('utf-8')).digest()
        encoded = base64.b64encode(encoded)

        return encoded.decode('utf-8')

    # Bir çok çağrıda kullanılan HTTP Header bilgilerini otomatik olarak ekleyen fonksiyondur.
    def GetHttpHeaders(self, configs, acceptType):
        token = self.CreateToken(configs.PublicKey, configs.HashString)
        print('HASH STR: '+configs.HashString)
        print('TOKEN: '+token)
        header = {'accept': acceptType, 'content-type': acceptType+'; charset=utf-8',
                  'Token': token,
                  'Version': configs.Version,
                  'transactionDate': configs.TransactionDate}
        print("TRANSACTION DATE: ", configs.TransactionDate)
        return header

    '''
    3D akışının ilk adımında yapılan işlemin ardından gelen cevabın doğrulanması adına kullanılacak fonksiyondur.
	Ödeme cevabı için response içerisinde hash bilgisine bakılarak işlem yapılır.
	hash bilgisi boş değilse çeşitli parametrelerle hashtext oluşturulur ve hash bilgisi hesaplanır.
    Hesaplanan hash bilgisi ile cevap sonucunda oluşan istek bilgisinin doğruluğu burada kontrol edilir.
    '''

    def Validate3DReturn(self, paymentResponse, configs):
        if paymentResponse.Hash is None:
            raise Exception("Odeme cevabi hash bilgisi bos")

        hashText = paymentResponse.OrderId+paymentResponse.Result+paymentResponse.Amount+paymentResponse.Mode+paymentResponse.ErrorCode +\
            paymentResponse.ErrorMessage+paymentResponse.TransactionDate + \
            configs.PublicKey+configs.PrivateKey
        hashedText = self.ComputeHash(hashText)

        if hashedText != paymentResponse.Hash:
            hashText = paymentResponse.OrderId+paymentResponse.Result+paymentResponse.Amount+paymentResponse.Mode+paymentResponse.ErrorCode +\
                paymentResponse.ErrorMessage+paymentResponse.TransactionDate + \
                configs.PublicKey+configs.PrivateKey
        hashedText = self.ComputeHash(hashText)
        if hashedText != paymentResponse.Hash:
            raise Exception("Ödeme cevabı hash doğrulaması hatalı.")
        return True

    @staticmethod
    def formatXML(input):
        doc = MND.parseString(input)
        output = doc.toprettyxml(
            indent="\t", newl="\n", encoding="utf-8").decode('UTF-8')
        return output


class HttpClient(object):
    @staticmethod
    def get(url, header={}):
        print("----IN HTTP GET----")
        print("URL: "+url)

        client = requests.get(url, None, headers=header)

        print("Return Code: ", client.status_code)
        print("---- HTTP GET OUT----")

    @staticmethod
    def post(url, header, content):
        print("----IN HTTP POST----")
        print("URL: ", url)
        print("HEADER.accept: ", header['accept'])
        print("HEADER.content-type: ", header['content-type'])
        print("HEADER.Token: ", header['Token'])
        print("HEADER.Version: ", header['Version'])
        print("HEADER.transactionDate: ", header['transactionDate'])

        client = requests.post(url, data=content.encode('utf-8'), headers=header,
                               params={'Token': header['Token']})

        print("REQUEST")
        print("Status Code: ", client.status_code)
        print(client.text)

        return client.text
