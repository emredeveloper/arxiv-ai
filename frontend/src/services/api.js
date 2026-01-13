/**
 * API service for backend communication
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Articles API
export const articlesAPI = {
    getArticles: (params) => api.get('/articles/', { params }),
    getByCategory: (category, maxResults = 10) =>
        api.get(`/articles/category/${category}`, { params: { max_results: maxResults } }),
    searchByKeyword: (keyword, maxResults = 10) =>
        api.get('/articles/search', { params: { keyword, max_results: maxResults } }),
};

// Favorites API
export const favoritesAPI = {
    getFavorites: (category = null) =>
        api.get('/favorites/', { params: category ? { category } : {} }),
    addFavorite: (data) => api.post('/favorites/', data),
    removeFavorite: (arxivId) => api.delete(`/favorites/${arxivId}`),
    checkFavorite: (arxivId) => api.get(`/favorites/check/${arxivId}`),
};

// Likes API
export const likesAPI = {
    addLike: (arxivId) => api.post(`/likes/${arxivId}`),
    getLikeCount: (arxivId) => api.get(`/likes/${arxivId}`),
};

// Translation API
export const translationAPI = {
    translate: (text, targetLang = 'tr', sourceLang = 'en') =>
        api.post('/translate/', { text, target_lang: targetLang, source_lang: sourceLang }),
};

// Statistics API
export const statisticsAPI = {
    getStatistics: () => api.get('/statistics/'),
};

export default api;
