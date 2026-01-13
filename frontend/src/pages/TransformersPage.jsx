import React, { useState } from 'react';
import { Search, Loader } from 'lucide-react';
import ArticleCard from '../components/ArticleCard';
import { articlesAPI } from '../services/api';
import toast from 'react-hot-toast';

const TransformersPage = () => {
    const [articles, setArticles] = useState([]);
    const [loading, setLoading] = useState(false);
    const [searchType, setSearchType] = useState('keyword');
    const [keyword, setKeyword] = useState('transformer');
    const [model, setModel] = useState('BERT');
    const [maxResults, setMaxResults] = useState(10);

    const models = ['BERT', 'GPT', 'T5', 'LLAMA', 'Vision Transformer', 'CLIP'];

    const fetchArticles = async () => {
        setLoading(true);
        try {
            const searchKeyword = searchType === 'keyword' ? keyword : model;
            const response = await articlesAPI.searchByKeyword(searchKeyword, maxResults);
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
                <h1>⚡ Transformers</h1>
                <p className="text-muted">
                    Transformer modelleri ve uygulamaları hakkında en güncel araştırmaları keşfedin
                </p>
            </div>

            <div className="card mb-lg">
                <h3>🔍 Arama Türü</h3>

                <div className="flex gap-md mb-md">
                    <button
                        onClick={() => setSearchType('keyword')}
                        className={searchType === 'keyword' ? 'btn btn-primary' : 'btn btn-secondary'}
                    >
                        Anahtar Kelime
                    </button>
                    <button
                        onClick={() => setSearchType('model')}
                        className={searchType === 'model' ? 'btn btn-primary' : 'btn btn-secondary'}
                    >
                        Popüler Modeller
                    </button>
                </div>

                {searchType === 'keyword' ? (
                    <div className="mb-md">
                        <label className="text-sm text-muted" style={{ display: 'block', marginBottom: '0.5rem' }}>
                            Anahtar Kelime
                        </label>
                        <input
                            type="text"
                            className="input"
                            value={keyword}
                            onChange={(e) => setKeyword(e.target.value)}
                            placeholder="transformer"
                        />
                    </div>
                ) : (
                    <div className="mb-md">
                        <label className="text-sm text-muted" style={{ display: 'block', marginBottom: '0.5rem' }}>
                            Model Seçin
                        </label>
                        <select
                            className="input"
                            value={model}
                            onChange={(e) => setModel(e.target.value)}
                        >
                            {models.map(m => (
                                <option key={m} value={m}>{m}</option>
                            ))}
                        </select>
                    </div>
                )}

                <div className="mb-md">
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
                            Ara
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
                                Makale görmek için yukarıdaki filtreleri ayarlayın ve "Ara" butonuna tıklayın.
                            </p>
                        </div>
                    )}
                </>
            )}
        </div>
    );
};

export default TransformersPage;
