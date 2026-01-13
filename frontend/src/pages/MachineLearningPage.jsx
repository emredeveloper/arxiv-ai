import React, { useState } from 'react';
import { Search, Loader } from 'lucide-react';
import ArticleCard from '../components/ArticleCard';
import { articlesAPI } from '../services/api';
import toast from 'react-hot-toast';

const MachineLearningPage = () => {
    const [articles, setArticles] = useState([]);
    const [loading, setLoading] = useState(false);
    const [category, setCategory] = useState('cs.LG');
    const [maxResults, setMaxResults] = useState(10);

    const categories = [
        { value: 'cs.LG', label: 'Genel (cs.LG)' },
        { value: 'cs.AI', label: 'Yapay Zeka (cs.AI)' },
        { value: 'cs.CV', label: 'Bilgisayarlı Görü (cs.CV)' },
        { value: 'cs.CL', label: 'Doğal Dil İşleme (cs.CL)' },
        { value: 'cs.NE', label: 'Sinir Ağları (cs.NE)' },
    ];

    const fetchArticles = async () => {
        setLoading(true);
        try {
            const response = await articlesAPI.getByCategory(category, maxResults);
            setArticles(response.data);
            toast.success(`${response.data.length} makale yüklendi!`);
        } catch (error) {
            toast.error('Makaleler yüklenemedi');
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container-wide" style={{ paddingTop: '2rem', paddingBottom: '2rem' }}>
            <div className="text-center mb-lg">
                <h1>🤖 Makine Öğrenmesi</h1>
                <p className="text-muted">
                    Makine öğrenmesi kategorisindeki en güncel araştırmaları keşfedin
                </p>
            </div>

            <div className="card mb-lg">
                <h3>⚙️ Kategori Seçimi</h3>

                <div className="grid grid-2 mb-md">
                    <div>
                        <label className="text-sm text-muted" style={{ display: 'block', marginBottom: '0.5rem' }}>
                            Alt Kategori
                        </label>
                        <select
                            className="input"
                            value={category}
                            onChange={(e) => setCategory(e.target.value)}
                        >
                            {categories.map(cat => (
                                <option key={cat.value} value={cat.value}>{cat.label}</option>
                            ))}
                        </select>
                    </div>

                    <div>
                        <label className="text-sm text-muted" style={{ display: 'block', marginBottom: '0.5rem' }}>
                            Makale Sayısı
                        </label>
                        <input
                            type="number"
                            className="input"
                            value={maxResults}
                            onChange={(e) => setMaxResults(parseInt(e.target.value))}
                            min="1"
                            max="100"
                        />
                    </div>
                </div>

                <button
                    onClick={fetchArticles}
                    disabled={loading}
                    className="btn btn-primary"
                >
                    {loading ? (
                        <>
                            <Loader className="spinner" size={16} />
                            Yükleniyor...
                        </>
                    ) : (
                        <>
                            <Search size={16} />
                            Makaleleri Getir
                        </>
                    )}
                </button>
            </div>

            {loading ? (
                <div className="text-center p-lg">
                    <div className="spinner" style={{ margin: '0 auto' }}></div>
                    <p className="text-muted mt-lg">Makaleler yükleniyor...</p>
                </div>
            ) : (
                <>
                    {articles.length > 0 && (
                        <p className="text-muted mb-md">
                            <strong>{articles.length}</strong> makale gösteriliyor
                        </p>
                    )}

                    {articles.map((article) => (
                        <ArticleCard key={article.arxiv_id} article={article} />
                    ))}

                    {articles.length === 0 && !loading && (
                        <div className="card text-center">
                            <p className="text-muted">
                                Makale görmek için yukarıdaki filtreleri ayarlayın ve "Makaleleri Getir" butonuna tıklayın.
                            </p>
                        </div>
                    )}
                </>
            )}
        </div>
    );
};

export default MachineLearningPage;
