import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, Star, BarChart3, Github, Linkedin } from 'lucide-react';
import './Navbar.css';

const Navbar = () => {
    const location = useLocation();

    const navItems = [
        { path: '/', icon: Home, label: 'Ana Sayfa' },
        { path: '/favorites', icon: Star, label: 'Favoriler' },
        { path: '/statistics', icon: BarChart3, label: 'İstatistikler' },
    ];

    return (
        <nav className="navbar">
            <div className="container">
                <div className="navbar-content">
                    <div className="navbar-brand">
                        <h2>📚 arXiv AI</h2>
                    </div>

                    <div className="navbar-links">
                        {navItems.map((item) => (
                            <Link
                                key={item.path}
                                to={item.path}
                                className={`nav-link ${location.pathname === item.path ? 'active' : ''}`}
                            >
                                <item.icon size={18} />
                                <span>{item.label}</span>
                            </Link>
                        ))}
                    </div>

                    <div className="navbar-social">
                        <a
                            href="https://github.com/emredeveloper"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="social-link"
                        >
                            <Github size={20} />
                        </a>
                        <a
                            href="https://www.linkedin.com/in/cihatemrekaratas/"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="social-link"
                        >
                            <Linkedin size={20} />
                        </a>
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
