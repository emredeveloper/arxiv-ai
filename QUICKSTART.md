# 🚀 Hızlı Başlangıç Kılavuzu

## ⚡ 5 Dakikada Başlat!

### 1️⃣ Backend'i Başlat

```bash
# Backend dizinine git
cd backend

# Bağımlılıkları yükle
pip install -r requirements.txt

# Sunucuyu başlat
uvicorn app.main:app --reload
```

✅ Backend hazır: http://localhost:8000
📚 API Docs: http://localhost:8000/api/docs

### 2️⃣ Frontend'i Başlat

**Yeni terminal açın:**

```bash
# Frontend dizinine git
cd frontend

# Bağımlılıkları yükle
npm install

# Development server'ı başlat
npm run dev
```

✅ Frontend hazır: http://localhost:3000

### 3️⃣ Kullanmaya Başla!

1. Tarayıcınızda http://localhost:3000 adresini açın
2. "Makaleleri Getir" butonuna tıklayın
3. Makaleleri beğenin, favorilere ekleyin, çevirin!

---

## 🎯 Özellikler

### Ana Sayfa
- Gelişmiş arama ve filtreleme
- Tarih aralığı seçimi
- Sıralama seçenekleri

### Makale Kartları
- **Çeviri**: Başlık ve özet çevirisi (önbellekli)
- **Beğeni**: Makaleleri beğenin
- **Favoriler**: Kaydetme ve kategori yönetimi
- **GitHub**: Otomatik link tespiti
- **PDF**: Direkt indirme linki

### Sayfalar
- 🏠 **Ana Sayfa**: Genel arama
- 🤖 **Makine Öğrenmesi**: 5 alt kategori
- ⚡ **Transformers**: Model ve keyword araması
- ⭐ **Favoriler**: Kayıtlı makaleler
- 📊 **İstatistikler**: Kullanım metrikleri

---

## 🛠️ Teknolojiler

### Backend
- **FastAPI**: Modern, hızlı web framework
- **SQLAlchemy**: ORM ve veritabanı
- **Pydantic**: Veri validasyonu
- **arXiv API**: Makale verisi
- **Google Translator**: Çeviri servisi

### Frontend
- **React 18**: UI library
- **React Router**: Sayfa yönlendirme
- **Axios**: HTTP client
- **Lucide React**: İkonlar
- **React Hot Toast**: Bildirimler
- **Vite**: Build tool

---

## 📖 API Örnekleri

### Makaleleri Getir
```bash
curl http://localhost:8000/api/v1/articles/?max_results=5
```

### Favorilere Ekle
```bash
curl -X POST http://localhost:8000/api/v1/favorites/ \
  -H "Content-Type: application/json" \
  -d '{
    "arxiv_id": "2301.12345",
    "title": "Example Article",
    "authors": ["John Doe"],
    "summary": "Summary text",
    "published_date": "2023-01-15",
    "entry_url": "http://arxiv.org/abs/2301.12345",
    "github_links": [],
    "category": "machine_learning"
  }'
```

### Çeviri Yap
```bash
curl -X POST http://localhost:8000/api/v1/translate/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Machine Learning",
    "target_lang": "tr"
  }'
```

---

## 🐛 Sorun Giderme

### Backend başlamıyor?
```bash
# Port kullanımda olabilir
uvicorn app.main:app --reload --port 8001
```

### Frontend başlamıyor?
```bash
# Port kullanımda olabilir
npm run dev -- --port 3001
```

### Veritabanı hatası?
```bash
# Veritabanını sıfırla
cd backend
rm arxiv_ai.db
# Uygulamayı yeniden başlat
```

### CORS hatası?
`backend/app/config.py` dosyasında frontend URL'ini ekleyin:
```python
BACKEND_CORS_ORIGINS = ["http://localhost:3000"]
```

---

## 💡 İpuçları

1. **Önbellek**: İlk çeviriler yavaş olabilir, sonrakiler hızlıdır
2. **API Limiti**: Çok fazla makale çekmek API limitine takılabilir
3. **Veritabanı**: Tüm veriler `backend/arxiv_ai.db` dosyasında
4. **Hot Reload**: Kod değişikliklerinde otomatik yenilenir

---

## 📚 Daha Fazla Bilgi

- **API Dokümantasyonu**: http://localhost:8000/api/docs
- **Proje README**: Ana dizindeki README.md
- **GitHub**: https://github.com/emredeveloper

---

**Keyifli kullanımlar! 🎉**
