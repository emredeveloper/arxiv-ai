# arXiv AI - Modern Makale Takip Sistemi

**FastAPI + React** ile geliştirilmiş, modern ve profesyonel bir arXiv makale arama ve takip uygulaması.

## ✨ Özellikler

### 🎯 Ana Özellikler
- **Modern UI/UX**: React ile glassmorphism, gradients ve animasyonlar
- **RESTful API**: FastAPI ile yüksek performanslı backend
- **Veri Kalıcılığı**: SQLAlchemy ile SQLite veritabanı
- **Çeviri Önbelleği**: Tekrarlayan çeviriler için hızlı erişim
- **Responsive Design**: Tüm cihazlarda mükemmel görünüm
- **Real-time Feedback**: Toast notifications ile anlık bildirimler

### 📚 Sayfalar
1. **Ana Sayfa**: Gelişmiş filtreleme ile makale arama
2. **Makine Öğrenmesi**: 5 farklı alt kategori desteği
3. **Transformers**: Anahtar kelime ve model bazlı arama
4. **Favoriler**: Kategori filtreleme ile kayıtlı makaleler
5. **İstatistikler**: Görsel istatistikler ve analytics

### 🛡️ Teknik Özellikler
- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Frontend**: React 18, React Router, Axios
- **Styling**: Modern CSS with CSS Variables
- **Icons**: Lucide React
- **Notifications**: React Hot Toast
- **Build Tool**: Vite

## 📁 Proje Yapısı

```
arxiv-ai/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   │   ├── articles.py
│   │   │   ├── favorites.py
│   │   │   ├── likes.py
│   │   │   ├── translation.py
│   │   │   └── statistics.py
│   │   ├── services/         # Business logic
│   │   │   ├── arxiv_service.py
│   │   │   └── translation_service.py
│   │   ├── config.py         # Configuration
│   │   ├── database.py       # Database setup
│   │   ├── models.py         # SQLAlchemy models
│   │   ├── schemas.py        # Pydantic schemas
│   │   └── main.py           # FastAPI app
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── ArticleCard.jsx
│   │   │   ├── Navbar.jsx
│   │   │   └── Navbar.css
│   │   ├── pages/            # Page components
│   │   │   ├── HomePage.jsx
│   │   │   ├── MachineLearningPage.jsx
│   │   │   ├── TransformersPage.jsx
│   │   │   ├── FavoritesPage.jsx
│   │   │   └── StatisticsPage.jsx
│   │   ├── services/         # API client
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
└── README.md
```

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+
- Node.js 16+
- npm veya yarn

### 1. Backend Kurulumu

```bash
# Backend dizinine git
cd backend

# Virtual environment oluştur (önerilen)
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Environment dosyasını oluştur
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Uygulamayı başlat
uvicorn app.main:app --reload
```

Backend şu adreste çalışacak: `http://localhost:8000`
API Dokümantasyonu: `http://localhost:8000/api/docs`

### 2. Frontend Kurulumu

```bash
# Frontend dizinine git
cd frontend

# Bağımlılıkları yükle
npm install

# Development server'ı başlat
npm run dev
```

Frontend şu adreste çalışacak: `http://localhost:3000`

## 🎮 Kullanım

### Backend API Endpoints

#### Articles
- `GET /api/v1/articles/` - Makale listesi
- `GET /api/v1/articles/category/{category}` - Kategoriye göre makaleler
- `GET /api/v1/articles/search?keyword={keyword}` - Anahtar kelime araması

#### Favorites
- `GET /api/v1/favorites/` - Favorileri listele
- `POST /api/v1/favorites/` - Favori ekle
- `DELETE /api/v1/favorites/{arxiv_id}` - Favori sil
- `GET /api/v1/favorites/check/{arxiv_id}` - Favori kontrolü

#### Likes
- `POST /api/v1/likes/{arxiv_id}` - Beğeni ekle
- `GET /api/v1/likes/{arxiv_id}` - Beğeni sayısı

#### Translation
- `POST /api/v1/translate/` - Metin çevir

#### Statistics
- `GET /api/v1/statistics/` - İstatistikleri getir

### Frontend Sayfalar

- `/` - Ana sayfa
- `/machine-learning` - Makine öğrenmesi
- `/transformers` - Transformers
- `/favorites` - Favoriler
- `/statistics` - İstatistikler

## 🗄️ Veritabanı

SQLite veritabanı otomatik olarak oluşturulur. Tablolar:

- **favorites**: Favori makaleler
- **likes**: Beğeniler
- **translations**: Çeviri önbelleği
- **user_interactions**: Kullanıcı etkileşimleri

## 🎨 Özelleştirme

### Backend

`backend/app/config.py` dosyasından ayarları değiştirebilirsiniz:
- CORS origins
- Database URL
- Cache TTL
- Secret key

### Frontend

`frontend/src/index.css` dosyasındaki CSS değişkenlerini düzenleyerek renk şemasını özelleştirebilirsiniz.

## 📊 Production Build

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm run build
npm run preview
```

Build dosyaları `frontend/dist` klasöründe oluşturulur.

## 🐛 Hata Ayıklama

### Backend Logları
FastAPI otomatik olarak detaylı hata mesajları gösterir. `/api/docs` adresinden Swagger UI ile API'yi test edebilirsiniz.

### Frontend Logları
Browser console'da hataları görebilirsiniz. React DevTools kullanarak component state'lerini inceleyebilirsiniz.

### Veritabanı Sıfırlama

```bash
# Backend dizininde
rm arxiv_ai.db
# Uygulamayı yeniden başlatın, otomatik oluşturulur
```

## 🔒 Güvenlik

- Production'da `SECRET_KEY` değiştirin
- HTTPS kullanın
- CORS ayarlarını production için güncelleyin
- Rate limiting ekleyin (önerilir)

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Lisans

MIT License

## 👨‍💻 Geliştirici

**Emre Karataş**
- GitHub: [@emredeveloper](https://github.com/emredeveloper)
- LinkedIn: [cihatemrekaratas](https://www.linkedin.com/in/cihatemrekaratas/)

## 🙏 Teşekkürler

- [arXiv](https://arxiv.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
- [Vite](https://vitejs.dev/)

## 📈 Roadmap

- [ ] User authentication
- [ ] Dark/Light mode toggle
- [ ] Advanced search filters
- [ ] Export favorites (PDF, CSV)
- [ ] Email notifications
- [ ] ML-based article recommendations
- [ ] Multi-language support
- [ ] Mobile app (React Native)

---

**Not**: Bu proje modern web teknolojileri ile geliştirilmiş, production-ready bir uygulamadır. Önerileriniz için issue açabilirsiniz!