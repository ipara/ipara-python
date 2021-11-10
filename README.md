iPara Python/Django Client Kütüphanesi
===================

iPara Python/Django Kütüphanesidir. iPara API'lerine çok hızlı bir şekilde bağlanmanızı sağlar.
[https://www.ipara.com.tr](https://www.ipara.com.tr) adresimizden mağaza başvurusu yaparak
hesabınızı açabilirsiniz.

## Entegrasyon sürecinde dikkat edilecek noktalar

iPara servislerini kullanabilmek için iPara'ya üye olmalısınız. Üye olduktan sonra Mağaza Listesi > Detay sayfası içerisindeki Public ve Private Key sizinle paylaşılacaktır. Paylaşılan bu anahtarları ipara-python projesinde Configs classda yer alan publicKey ve privateKey alanlarına eklemeniz gerekmektedir.

```python
class Configs:
    '''
    Tüm çağrılarda kullanılacak ayarların tutulduğu sınıftır.
    Bu sınıf üzerinde size özel parametreler fonksiyonlar arasında taşınabilir.
    Bu sınıf üzerinde tüm sistemde kullanacağımız ayarları tutar ve bunlara göre işlem yaparız.
    '''

    def __init__(self, PublicKey, PrivateKey, BaseUrl, Mode, Echo, Version, HashString, TransactionDate):
        # Public Magaza Anahtarı - size mağaza başvurunuz sonucunda gönderilen public key (açık anahtar) bilgisini kullanınız.
        self.PublicKey = PublicKey
        # Private Magaza Anahtarı  - size mağaza başvurunuz sonucunda gönderilen privaye key (gizli anahtar) bilgisini kullanınız.
        self.PrivateKey = PrivateKey
        # iPara web servisleri API url'lerinin başlangıç bilgisidir.
        self.BaseUrl = BaseUrl
        # Test -> T, entegrasyon testlerinin sırasında "T" modunu, canlı sisteme entegre olarak ödeme almaya başlamak için ise Prod -> "P" modunu kullanınız
        self.Mode = Mode
        # 3D secure işlemlerinde kullanacağımız url adresini temsil eder
        self.Echo = Echo
        # Kullandığınız iPara API versiyonudur.
        self.Version = Version
        # Kullanacağınız hash bilgisini, bağlanmak istediğiniz web servis bilgisine göre doldurulmalıdır.
        self.HashString = HashString
        # Api çağrılarında transactionDate olarak kullanacağımız alan bilgisidir.
        self.TransactionDate = TransactionDate
```

Örnek projelerimizdeki servislerimizi daha iyi anlamak için [iPara geliştirici merkezini](http://dev.ipara.com.tr) takip etmeniz büyük önem arz etmektedir.

* Entegrasyon işlemlerinde encoding “UTF-8” kullanılması önerilmektedir.Token parametrelerinden kaynaklı sorun encoding probleminden kaynaklanmaktadır. Özel karakterlerde encoding işlemi yapılmalıdır.
* Servis isteği yaparaken göndermiş olduğunuz alanların başında ve sonunda oluşabilecek boşluk alanlarını kaldırmanızı ( trim() ) önemle rica ederiz. Çünkü bu alanlar oluşacak hash sonuçlarını etkilemektedir.
* Entegrasyon dahilinde gönderilen input alanlarında, kart numarası alanı dışında kart numarası bilgisi gönderilmesi halinde işlem reddedilecektir.

iPara örnek projelerinin amacı, yazılım geliştiricilere iPara servislerine entegre olabilecek bir proje örneği sunmak ve entegrasyon adımlarının daha iyi anlaşılmasını sağlamaktır. Projeleri doğrudan canlı ortamınıza alarak kod değişimi yapmadan kullanmanız için desteğimiz bulunmamaktadır. **Projeyi bir eğitsel kaynak (tutorial) olarak kullanınız.**

## Test Kartları

Başarılı bir ödemeyi test etmek için aşağıdaki kart numaralarını ve diğer bilgileri kullanabilirsiniz.

| Sıra No  | Kart Numarası     | SKT    | CVC  | Banka                 | Kart Ailesi            |
|--------- |------------------ |------- |----- | ---------------       | ---------              |
| 1        | 4282209004348015  | 12/22  | 123  | Garanti Bankası       | BONUS                  |
| 2        | 5571135571135575  | 12/22  | 000  | Akbank                | AXESS                  |
| 3        | 4355084355084358  | 12/22  | 000  | Akbank                | AXESS                  |
| 4        | 4662803300111364  | 10/25  | 000  | Alternatif Bank       | BONUS                  |
| 5       | 4022774022774026  | 12/24  | 000  | Finansbank            | CARD FINANS            |
| 6        | 5456165456165454  | 12/24  | 000  | Finansbank            | CARD FINANS            |
| 7         | 9792023757123604  | 01/26     | 861   | Finansbank            | FINANSBANK DEBIT       |
| 8        | 4531444531442283  | 12/24  | 000  | Aktif Yatırım Bankası | AKTIF KREDI KARTI      |
| 9        | 5818775818772285  | 12/24  | 000  | Aktif Yatırım Bankası | AKTIF KREDI KARTI      |
| 10       | 4508034508034509  | 12/24  | 000  | İş bankası            | MAXIMUM                |
| 11       | 5406675406675403  | 12/24  | 000  | İş bankası            | MAXIMUM                |
| 12       | 4025903160410013  | 07/22  | 123  | Kuveyttürk            | KUVEYTTURK KREDI KARTI |
| 13       | 5345632006230604  | 12/24  | 310  | Aktif Yatırım Bankası | AKTIF KREDI KARTI      |
| 14       | 4282209027132016  | 12/24  | 358  | Garanti Bankası       | BONUS                  |
| 15       | 4029400154245816  | 03/24  | 373  | Vakıf Bank            | WORLD                  |
| 16       | 4029400184884303  | 01/23  | 378  | Vakıf Bank            | WORLD                  |
| 17       | 9792350046201275  | 07/27   | 993  | TÜRK ELEKTRONIK PARA  | PARAM KART             |
| 18       | 6501700194147183 | 03/27   | 136  | Vakıf Bank            | WORLD                  |
| 19      | 6500528865390837 | 01/22   | 686  | Vakıf Bank            | VAKIFBANK DEBIT        |

Test kartlarımızda alınan hata kodları ve çözümleriyle ilgili detaylı bilgiye ulaşabilmek için [iPara Hata Kodları](https://dev.ipara.com.tr/home/ErrorCode) inceleyebilirsiniz.

## Örnek Kullanım Yöntemi
```python
def nonThreeDPaymentRequest(request):
    message = ""
    if request.POST:
        non3DPaymentRequest = NonThreeDPaymentRequest()
        non3DPaymentRequest.Echo = "Echo"
        non3DPaymentRequest.Mode = config.Mode
        non3DPaymentRequest.ThreeD = "false"
        non3DPaymentRequest.OrderId = str(randint(1, 10000))
        non3DPaymentRequest.Amount = "10000"
        non3DPaymentRequest.CardOwnerName = "Murat Kaya"
        non3DPaymentRequest.CardNumber = "5456165456165454"
        non3DPaymentRequest.CardExpireMonth = "12"
        non3DPaymentRequest.CardExpireYear = "24"
        non3DPaymentRequest.Installment = "1"
        non3DPaymentRequest.Cvc = "000"
        non3DPaymentRequest.VendorId = ""
        non3DPaymentRequest.UserId = ""
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
        non3DPaymentRequest.Purchaser.invoiceAddress.address = "Mevlut Pehlivan Mah. Multinet Plaza Sisli"
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
        non3DPaymentRequest.Purchaser.shippingAddress.address = "Mevlut Pehlivan Mah. Multinet Plaza Sisli"
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
        message = Helper.formatXML(
            non3DPaymentRequest.execute(non3DPaymentRequest, config))

    return render_to_response('nonThreeDPayment.html', {'message': message})

```

## Hash Hesaplama
iPara servislerine entegre olurken alınan hataların en sık karşılaşılanı hash değerinin doğru hesaplanmasıdır. Hash değeri her servise göre değişen verilerin yanyana eklenmesi ile oluşan değerin bir dizi işleme tabi tutulması ile oluşur.

Aşağıdaki adreste hash hesaplama ile ilgili detaylar yer almaktadır. Yine burada yer alan interaktif fonksiyon ile hesapladığınız hash fonksiyonlarını test edebilirsiniz.

[iPara Hash Hesaplama](https://dev.ipara.com.tr/#hashCalculate)

Her örnek projenin Helper sınıfı içinde hash hesaplama ile alakalı bir fonksiyon bulunmaktadır. Entegrasyon sırasıdna bu hazır fonksiyonları da kullanabilirsiniz.

## Canlı Ortama Geçiş

* Test ortamında kullandığınız statik verilerin canlı ortamda gerçek müşteri datasıyla değiştirildiğinden emin olun.
* Canlı ortamda yanlış, sabit data gönderilmediğinden emin olun. Gönderdiğiniz işlemlere ait verileri mutlaka size özel panelden görüntüleyin.
* Geliştirmeler tamamlandıktan sonra ödeme adımlarını, iPara test kartları ile tüm olası durumlar için test edin ve sonuçlarını görüntüleyin.
* iPara servislerinden dönen ve olabilecek tüm hataları karşılayacak ve müşteriye uygun cevabı gösterecek şekilde kodunuzu düzenleyin ve test edin.
* iPara hata kodları kullanıcı dostu mesajlar olup müşterinize gösterebilirsiniz.
* Hassas olmayan verileri ve servis yanıtlarını, hata çözümü ve olası sorunların çözümünde yardımcı olması açısından loglamaya dikkat edin.
* Canlı ortama geçiş sonrası ilk işlemleri kendi kredi kartlarınız ile deneyerek sonuçlarını size özel Kurum ekranlarından görüntüleyin. Sonuçların ve işlemlerin doğru tamamlandığından emin olun.

Sorularınız olması durumunda bize [Destek](https://dev.ipara.com.tr/Home/Support) üzerinden yazabilirsiniz.

## Versiyon Yenilikleri

| Versiyon | Versiyon Yenilikleri                                                                             |
|--------- |-------------------------------------------------------------------------------------------   |
| 1.0.1     | - İki adımlı ThreeD ödemesi kaldırılıp **Tek adımlı ThreeD** ödemesi eklendi.<br />- Ödeme sorgulama servisinde ek olarak **tarih filtresi** eklendi.<br />- **Link ile ödeme, ödeme linki sorgulama,ödeme linki silme** servisleri eklendi.<br />- **Ürün iade bilgisi sorgulama,ürün iade talebi** oluşturma servisleri eklendi. <br />- **Bin sorgulama servisine tutar bilgisi** eklenerek komisyon bilgisi kullanıcıya sunuldu. |
