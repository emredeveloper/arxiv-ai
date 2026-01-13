import React, { useState, useEffect } from 'react';
import ArticleCard from '../components/ArticleCard';
import { favoritesAPI } from '../services/api';
import toast from 'react-hot-toast';

const FavoritesPage = () => {
    const [favorites, setFavorites] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedCategory, setSelectedCategory] = useState(null);

    const fetchFavorites = async () => {
        setLoading(true);
        try {
            const response = await favoritesAPI.getFavorites(selectedCategory);
            setFavorites(response.data);
        } catch (error) {
            toast.error('Favoriler yüklenemedi');
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchFavorites();
    }, [selectedCategory]);

    const categories = [...new Set(favorites.map(fav => fav.category))];

    return (
        <div className="container-wide" style={{ paddingTop: '2rem', paddingBottom: '2rem' }}>
            <div className="text-center mb-lg">
                <h1>⭐ Favoriler</h1>
                <p className="text-muted">Kaydettiğiniz makaleleri buradan görüntüleyebilirsiniz</p>
            </div>

            {categories.length > 0 && (
                <div className="card mb-lg">
                    <label className="text-sm text-muted" style={{ display: 'block', marginBottom: '0.5rem' }}>
                        Kategori Filtrele
                    </label>
                    <select
                        className="input"
                        value={selectedCategory || ''}
                        onChange={(e) => setSelectedCategory(e.target.value || null)}
                    >
                        <option value="">Tümü</option>
                        {categories.map(cat => (
                            <option key={cat} value={cat}>{cat}</option>
                        ))}
                    </select>
                </div>
            )}

            {loading ? (
                <div className="text-center p-lg">
                    <div className="spinner" style={{ margin: '0 auto' }}></div>
                    <p className="text-muted mt-lg">Favoriler yükleniyor...</p>
                </div>
            ) : (
                <>
                    {favorites.length > 0 ? (
                        <>
                            <p className="text-muted mb-md">
                                <strong>{favorites.length}</strong> favori makaleniz var
                            </p>
                            {favorites.map((fav) => (
                                <ArticleCard
                                    key={fav.arxiv_id}
                                    article={{
                                        ...fav,
                                        is_favorite: true,
                                        like_count: 0
                                    }}
                                    onUpdate={fetchFavorites}
                                />
                            ))}
                        </>
                    ) : (
                        <div className="card text-center">
                            <h3>Henüz favori makaleniz yok</h3>
                            <p className="text-muted">
                                Ana sayfadan makaleleri favorilere ekleyebilirsiniz
                            </p>
                        </div>
                    )}
                </>
            )}
        </div>
    );
};

export default FavoritesPage;
