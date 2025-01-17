# arXiv Makale Gösterim Uygulaması

Bu Streamlit uygulaması, arXiv'deki güncel makine öğrenmesi makalelerini çeker ve kullanıcıya gösterir. Kullanıcılar, makalelerin başlıklarını ve özetlerini Türkçeye çevirebilir, makaleleri beğenebilir ve GitHub bağlantılarını görüntüleyebilir.

## Özellikler

- **Güncel Makaleler**: arXiv'den "Computer Science > Machine Learning" kategorisindeki güncel makaleleri çeker.
- **Türkçe Çeviri**: Makale başlıklarını ve özetlerini Türkçeye çevirme imkanı.
- **Beğenme Sistemi**: Kullanıcılar makaleleri beğenebilir ve beğenilerini kaydedebilir.
- **GitHub Bağlantıları**: Makalelerde GitHub bağlantıları varsa, bu bağlantıları gösterir.
- **Menü Sistemi**: Ana Sayfa, Makine Öğrenmesi ve Transformers gibi farklı sayfalar arasında geçiş yapma imkanı.

## Kurulum

1. **Python Kurulumu**:
   - Projeyi çalıştırmak için Python 3.8 veya üzeri bir sürüm gereklidir.
   - Python'u [resmi sitesinden](https://www.python.org/downloads/) indirip kurabilirsiniz.

2. **Proje Dosyalarını İndirme**:
   - Projeyi bilgisayarınıza indirin veya klonlayın:
     ```bash
     git clone https://github.com/kullanici_adi/proje_repo.git
     cd proje_repo
     ```

3. **Bağımlılıkları Yükleme**:
   - Proje dizininde `requirements.txt` dosyası bulunmaktadır. Bu dosyadaki bağımlılıkları yüklemek için aşağıdaki komutu çalıştırın:
     ```bash
     pip install -r requirements.txt
     ```

## Çalıştırma

1. **Streamlit Uygulamasını Başlatma**:
   - Proje dizininde aşağıdaki komutu çalıştırarak uygulamayı başlatın:
     ```bash
     streamlit run app.py
     ```

2. **Tarayıcıda Görüntüleme**:
   - Uygulama başlatıldıktan sonra, tarayıcınızda otomatik olarak açılacaktır. Eğer açılmazsa, terminalde gösterilen URL'yi tarayıcınıza yapıştırın (örneğin: `http://localhost:8501`).

## Katkıda Bulunma

Eğer bu projeye katkıda bulunmak isterseniz, lütfen aşağıdaki adımları takip edin:

1. Projeyi fork edin.
2. Yeni bir branch oluşturun (`git checkout -b yeni-ozellik`).
3. Değişikliklerinizi yapın ve commit edin (`git commit -am 'Yeni özellik eklendi'`).
4. Branch'inizi push edin (`git push origin yeni-ozellik`).
5. GitHub üzerinden bir Pull Request oluşturun.
