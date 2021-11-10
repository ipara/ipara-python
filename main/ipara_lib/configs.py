
# coding=utf-8
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
