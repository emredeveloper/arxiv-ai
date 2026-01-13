import React, { useState } from 'react';
import { Heart, Star, ExternalLink, Github } from 'lucide-react';
import { favoritesAPI, likesAPI } from '../services/api';
import toast from 'react-hot-toast';
import ArticleModal from './ArticleModal';

const ArticleCard = ({ article, onUpdate }) => {
    const [likeCount, setLikeCount] = useState(article.like_count || 0);
    const [isFavorite, setIsFavorite] = useState(article.is_favorite || false);
    const [isModalOpen, setIsModalOpen] = useState(false);

    const handleLike = async () => {
        try {
            const response = await likesAPI.addLike(article.arxiv_id);
            setLikeCount(response.data.like_count);
            toast.success('Beğenildi!');
        } catch (error) {
            toast.error('Beğeni eklenemedi');
        }
    };

    const handleToggleFavorite = async () => {
        try {
            if (isFavorite) {
                await favoritesAPI.removeFavorite(article.arxiv_id);
                setIsFavorite(false);
                toast.success('Favorilerden çıkarıldı');
            } else {
                await favoritesAPI.addFavorite({
                    arxiv_id: article.arxiv_id,
                    title: article.title,
                    authors: article.authors,
                    summary: article.summary,
                    published_date: article.published_date,
                    entry_url: article.entry_url,
                    github_links: article.github_links || [],
                    category: 'general'
                });
                setIsFavorite(true);
                toast.success('Favorilere eklendi!');
            }
            if (onUpdate) onUpdate();
        } catch (error) {
            toast.error(error.response?.data?.detail || 'İşlem başarısız');
        }
    };

    return (
        <>
            <div className="card fade-in" onClick={() => setIsModalOpen(true)} style={{ cursor: 'pointer' }}>
                <h3>{article.title}</h3>

                <div className="flex gap-sm mb-md" style={{ flexWrap: 'wrap' }}>
                    {article.authors.slice(0, 5).map((author, idx) => (
                        <span key={idx} className="badge badge-primary">{author}</span>
                    ))}
                    {article.authors.length > 5 && (
                        <span className="badge badge-primary">+{article.authors.length - 5} daha</span>
                    )}
                </div>

                <p className="text-muted mb-md" style={{ fontSize: '0.9rem' }}>
                    📅 {article.published_date}
                </p>

                <p style={{
                    fontSize: '0.95rem',
                    lineHeight: '1.6',
                    display: '-webkit-box',
                    WebkitLineClamp: 3,
                    WebkitBoxOrient: 'vertical',
                    overflow: 'hidden',
                    color: 'var(--text-secondary)'
                }}>
                    {article.summary}
                </p>

                {article.github_links && article.github_links.length > 0 && (
                    <div className="mt-md mb-md">
                        <span className="badge badge-success">
                            <Github size={14} />
                            GitHub Mevcut
                        </span>
                    </div>
                )}

                <div className="flex gap-md mt-md" style={{ flexWrap: 'wrap' }} onClick={(e) => e.stopPropagation()}>
                    <a
                        href={article.entry_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn btn-primary"
                    >
                        <ExternalLink size={16} />
                        arXiv
                    </a>

                    {article.pdf_url && (
                        <a
                            href={article.pdf_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="btn btn-secondary"
                        >
                            📄 PDF
                        </a>
                    )}

                    <button onClick={handleLike} className="btn btn-secondary">
                        <Heart size={16} fill={likeCount > 0 ? 'currentColor' : 'none'} />
                        {likeCount}
                    </button>

                    <button
                        onClick={handleToggleFavorite}
                        className={isFavorite ? 'btn btn-success' : 'btn btn-secondary'}
                    >
                        <Star size={16} fill={isFavorite ? 'currentColor' : 'none'} />
                        {isFavorite ? 'Favorilerde' : 'Favorilere Ekle'}
                    </button>
                </div>
            </div>

            <ArticleModal
                article={article}
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                onLike={handleLike}
                onToggleFavorite={handleToggleFavorite}
                likeCount={likeCount}
                isFavorite={isFavorite}
            />
        </>
    );
};

export default ArticleCard;
