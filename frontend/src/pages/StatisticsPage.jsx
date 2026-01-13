import React, { useState, useEffect } from 'react';
import { statisticsAPI } from '../services/api';
import toast from 'react-hot-toast';

const StatisticsPage = () => {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const response = await statisticsAPI.getStatistics();
                setStats(response.data);
            } catch (error) {
                toast.error('İstatistikler yüklenemedi');
                console.error(error);
            } finally {
                setLoading(false);
            }
        };

        fetchStats();
    }, []);

    if (loading) {
        return (
            <div className="container" style={{ paddingTop: '2rem' }}>
                <div className="text-center p-lg">
                    <div className="spinner" style={{ margin: '0 auto' }}></div>
                    <p className="text-muted mt-lg">İstatistikler yükleniyor...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="container-wide" style={{ paddingTop: '2rem', paddingBottom: '2rem' }}>
            <div className="text-center mb-lg">
                <h1>📊 İstatistikler</h1>
                <p className="text-muted">Kullanım istatistiklerinizi görüntüleyin</p>
            </div>

            <div className="grid grid-3 mb-lg">
                <div className="card text-center" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
                    <h2 style={{ color: 'white', margin: 0 }}>{stats?.total_favorites || 0}</h2>
                    <p style={{ color: 'rgba(255,255,255,0.9)', margin: '0.5rem 0 0 0' }}>Toplam Favori</p>
                </div>

                <div className="card text-center" style={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' }}>
                    <h2 style={{ color: 'white', margin: 0 }}>{stats?.total_likes || 0}</h2>
                    <p style={{ color: 'rgba(255,255,255,0.9)', margin: '0.5rem 0 0 0' }}>Toplam Beğeni</p>
                </div>

                <div className="card text-center" style={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' }}>
                    <h2 style={{ color: 'white', margin: 0 }}>{stats?.total_categories || 0}</h2>
                    <p style={{ color: 'rgba(255,255,255,0.9)', margin: '0.5rem 0 0 0' }}>Farklı Kategori</p>
                </div>
            </div>

            {stats?.category_distribution && Object.keys(stats.category_distribution).length > 0 && (
                <div className="card mb-lg">
                    <h3>📈 Kategori Dağılımı</h3>
                    <div className="grid grid-2">
                        {Object.entries(stats.category_distribution).map(([category, count]) => (
                            <div key={category} className="flex justify-between items-center p-md" style={{ background: 'rgba(255,255,255,0.05)', borderRadius: 'var(--radius-md)' }}>
                                <span>{category}</span>
                                <span className="badge badge-primary">{count} makale</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {stats?.most_liked_articles && stats.most_liked_articles.length > 0 && (
                <div className="card">
                    <h3>🔥 En Çok Beğenilen Makaleler</h3>
                    <div className="flex flex-col gap-md">
                        {stats.most_liked_articles.map((article, idx) => (
                            <div key={article.arxiv_id} className="flex justify-between items-center p-md" style={{ background: 'rgba(255,255,255,0.05)', borderRadius: 'var(--radius-md)' }}>
                                <div className="flex items-center gap-md">
                                    <span className="badge badge-success">{idx + 1}</span>
                                    <span>{article.title}</span>
                                </div>
                                <span className="badge badge-primary">❤️ {article.like_count}</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {(!stats || (stats.total_favorites === 0 && stats.total_likes === 0)) && (
                <div className="card text-center">
                    <h3>Henüz istatistik yok</h3>
                    <p className="text-muted">
                        Makaleleri beğenmeye ve favorilere eklemeye başlayın!
                    </p>
                </div>
            )}
        </div>
    );
};

export default StatisticsPage;
