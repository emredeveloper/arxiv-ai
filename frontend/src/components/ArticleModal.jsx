import React from 'react';
import { X, ExternalLink, Github, Heart, Star, Calendar, User } from 'lucide-react';
import './ArticleModal.css';

const ArticleModal = ({ article, isOpen, onClose, onLike, onToggleFavorite, likeCount, isFavorite }) => {
    if (!isOpen || !article) return null;

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <button className="modal-close" onClick={onClose}>
                    <X size={24} />
                </button>

                <div className="modal-header">
                    <h2>{article.title}</h2>
                </div>

                <div className="modal-body">
                    {/* Authors */}
                    <div className="modal-section">
                        <div className="section-title">
                            <User size={18} />
                            <span>Yazarlar</span>
                        </div>
                        <div className="authors-grid">
                            {article.authors.map((author, idx) => (
                                <span key={idx} className="author-badge">{author}</span>
                            ))}
                        </div>
                    </div>

                    {/* Published Date */}
                    <div className="modal-section">
                        <div className="section-title">
                            <Calendar size={18} />
                            <span>Yayın Tarihi</span>
                        </div>
                        <p className="publish-date">{article.published_date}</p>
                    </div>

                    {/* Summary */}
                    <div className="modal-section">
                        <div className="section-title">
                            <span>📄</span>
                            <span>Özet</span>
                        </div>
                        <p className="article-summary">{article.summary}</p>
                    </div>

                    {/* GitHub Links */}
                    {article.github_links && article.github_links.length > 0 && (
                        <div className="modal-section">
                            <div className="section-title">
                                <Github size={18} />
                                <span>GitHub Repository</span>
                            </div>
                            <div className="github-links">
                                {article.github_links.map((link, idx) => (
                                    <a
                                        key={idx}
                                        href={link}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="github-link"
                                    >
                                        <Github size={16} />
                                        {link.split('/').slice(-1)[0]}
                                        <ExternalLink size={14} />
                                    </a>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Actions */}
                    <div className="modal-actions">
                        <a
                            href={article.entry_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="btn btn-primary"
                        >
                            <ExternalLink size={18} />
                            arXiv'de Aç
                        </a>

                        {article.pdf_url && (
                            <a
                                href={article.pdf_url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="btn btn-secondary"
                            >
                                📄 PDF İndir
                            </a>
                        )}

                        <button onClick={onLike} className="btn btn-secondary">
                            <Heart size={18} fill={likeCount > 0 ? 'currentColor' : 'none'} />
                            {likeCount}
                        </button>

                        <button
                            onClick={onToggleFavorite}
                            className={isFavorite ? 'btn btn-success' : 'btn btn-secondary'}
                        >
                            <Star size={18} fill={isFavorite ? 'currentColor' : 'none'} />
                            {isFavorite ? 'Favorilerde' : 'Favorilere Ekle'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ArticleModal;
