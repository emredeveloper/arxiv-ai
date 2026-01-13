import React, { useState, useEffect } from 'react';
import { Search, Loader, Calendar } from 'lucide-react';
import ArticleCard from '../components/ArticleCard';
import SkeletonLoader from '../components/SkeletonLoader';
import { articlesAPI } from '../services/api';
import toast from 'react-hot-toast';

const HomePage = () => {
    const [articles, setArticles] = useState([]);
    const [loading, setLoading] = useState(false);
    const [query, setQuery] = useState('cat:cs.LG');
    const [maxResults, setMaxResults] = useState(10);
    const [sortBy, setSortBy] = useState('Yeniden Eskiye');
    const [dateRange, setDateRange] = useState('all');
    const [customStartDate, setCustomStartDate] = useState('');
    const [customEndDate, setCustomEndDate] = useState('');

    const queryOptions = [
        { value: 'cat:cs.LG', label: 'Machine Learning (cs.LG)' },
        { value: 'cat:cs.AI', label: 'Artificial Intelligence (cs.AI)' },
        { value: 'cat:cs.CV', label: 'Computer Vision (cs.CV)' },
        { value: 'cat:cs.CL', label: 'Natural Language Processing (cs.CL)' },
        { value: 'cat:cs.NE', label: 'Neural Networks (cs.NE)' },
        { value: 'deep learning', label: 'Deep Learning' },
        { value: 'transformer', label: 'Transformers' },
        { value: 'reinforcement learning', label: 'Reinforcement Learning' },
        { value: 'generative AI', label: 'Generative AI' },
        { value: 'large language model', label: 'Large Language Models (LLM)' },
        { value: 'diffusion model', label: 'Diffusion Models' },
        { value: 'graph neural network', label: 'Graph Neural Networks' },
    ];

    const dateRangeOptions = [
        { value: 'all', label: 'Tüm Zamanlar' },
        { value: '7days', label: 'Son 7 Gün' },
        { value: '30days', label: 'Son 30 Gün' },
        { value: '3months', label: 'Son 3 Ay' },
        { value: '6months', label: 'Son 6 Ay' },
        { value: 'custom', label: 'Özel Tarih Aralığı' },
    ];

    const getDateRange = () => {
        const now = new Date();
        switch (dateRange) {
            case '7days':
                return { start: new Date(now.setDate(now.getDate() - 7)), end: new Date() };
            case '30days':
                return { start: new Date(now.setDate(now.getDate() - 30)), end: new Date() };
            case '3months':
                return { start: new Date(now.setMonth(now.getMonth() - 3)), end: new Date() };
            case '6months':
                return { start: new Date(now.setMonth(now.getMonth() - 6)), end: new Date() };
            case 'custom':
                return {
                    start: customStartDate ? new Date(customStartDate) : null,
                    end: customEndDate ? new Date(customEndDate) : null
                };
            default:
                return { start: null, end: null };
        }
    };

    const fetchArticles = async () => {
        setLoading(true);
        try {
            const response = await articlesAPI.getArticles({
                query,
                max_results: maxResults,
                sort_by: sortBy
            });

            let filteredArticles = response.data;

            // Apply date filter
            if (dateRange !== 'all') {
                const { start, end } = getDateRange();
                if (start && end) {
                    filteredArticles = filteredArticles.filter(article => {
                        const articleDate = new Date(article.published_date);
                        return articleDate >= start && articleDate <= end;
                    });
                }
            }

            setArticles(filteredArticles);
            toast.success(`${filteredArticles.length} makale yüklendi!`);
        } catch (error) {
            toast.error('Makaleler yüklenemedi');
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchArticles();
    }, []);

    return (
        <div className="container-wide" style={{ paddingTop: '2rem', paddingBottom: '2rem' }}>
            <div className="text-center mb-lg">
                <h1>📚 arXiv'de Güncel Makaleler</h1>
                <p className="text-muted" style={{ fontSize: '1.1rem' }}>
                    Makine öğrenmesi ve yapay zeka alanındaki en güncel araştırmaları keşfedin
                </p>
            </div>

            <div className="card mb-lg">
                <h3>🔍 Arama Filtreleri</h3>

                <div className="grid grid-2 mb-md">
                    <div>
                        <label className="text-sm text-muted" style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.95rem' }}>
                            Kategori / Konu
                        </label>
                        <select
                            className="input"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            style={{ fontSize: '0.95rem', padding: '0.75rem 1rem' }}
                        >
                            {queryOptions.map(option => (
                                <option key={option.value} value={option.value}>
                                    {option.label}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div>
                        <label className="text-sm text-muted" style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.95rem' }}>
                            Makale Sayısı
                        </label>
                        <input
                            type="number"
                            className="input"
                            value={maxResults}
                            onChange={(e) => setMaxResults(parseInt(e.target.value))}
                            min="1"
                            max="100"
                            style={{ fontSize: '0.95rem', padding: '0.75rem 1rem' }}
                        />
                    </div>
                </div>

                <div className="grid grid-2 mb-md">
                    <div>
                        <label className="text-sm text-muted" style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.95rem' }}>
                            <Calendar size={16} style={{ display: 'inline', marginRight: '0.25rem' }} />
                            Tarih Aralığı
                        </label>
                        <select
                            className="input"
                            value={dateRange}
                            onChange={(e) => setDateRange(e.target.value)}
                            style={{ fontSize: '0.95rem', padding: '0.75rem 1rem' }}
                        >
                            {dateRangeOptions.map(option => (
                                <option key={option.value} value={option.value}>
                                    {option.label}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div>
                        <label className="text-sm text-muted" style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.95rem' }}>
                            Sıralama
                        </label>
                        <select
                            className="input"
                            value={sortBy}
                            onChange={(e) => setSortBy(e.target.value)}
                            style={{ fontSize: '0.95rem', padding: '0.75rem 1rem' }}
                        >
                            <option value="Yeniden Eskiye">Yeniden Eskiye</option>
                            <option value="Eskiden Yeniye">Eskiden Yeniye</option>
                        </select>
                    </div>
                </div>

                {dateRange === 'custom' && (
                    <div className="grid grid-2 mb-md">
                        <div>
                            <label className="text-sm text-muted" style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.95rem' }}>
                                Başlangıç Tarihi
                            </label>
                            <input
                                type="date"
                                className="input"
                                value={customStartDate}
                                onChange={(e) => setCustomStartDate(e.target.value)}
                                style={{ fontSize: '0.95rem', padding: '0.75rem 1rem' }}
                            />
                        </div>
                        <div>
                            <label className="text-sm text-muted" style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.95rem' }}>
                                Bitiş Tarihi
                            </label>
                            <input
                                type="date"
                                className="input"
                                value={customEndDate}
                                onChange={(e) => setCustomEndDate(e.target.value)}
                                style={{ fontSize: '0.95rem', padding: '0.75rem 1rem' }}
                            />
                        </div>
                    </div>
                )}

                <button
                    onClick={fetchArticles}
                    disabled={loading}
                    className="btn btn-primary"
                    style={{ fontSize: '1rem', padding: '0.75rem 1.5rem' }}
                >
                    {loading ? (
                        <>
                            <Loader className="spinner" size={18} />
                            Yükleniyor...
                        </>
                    ) : (
                        <>
                            <Search size={18} />
                            Makaleleri Getir
                        </>
                    )}
                </button>
            </div>

            {loading ? (
                <SkeletonLoader count={maxResults > 5 ? 5 : maxResults} />
            ) : (
                <>
                    {articles.length > 0 && (
                        <p className="text-muted mb-md" style={{ fontSize: '1rem' }}>
                            <strong>{articles.length}</strong> makale gösteriliyor
                        </p>
                    )}

                    {articles.map((article) => (
                        <ArticleCard
                            key={article.arxiv_id}
                            article={article}
                            onUpdate={fetchArticles}
                        />
                    ))}

                    {articles.length === 0 && !loading && (
                        <div className="card text-center">
                            <p className="text-muted" style={{ fontSize: '1rem' }}>
                                Makale bulunamadı. Filtreleri değiştirip tekrar deneyin.
                            </p>
                        </div>
                    )}
                </>
            )}
        </div>
    );
};

export default HomePage;
