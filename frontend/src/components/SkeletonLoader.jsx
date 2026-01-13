import React from 'react';
import './SkeletonLoader.css';

const SkeletonLoader = ({ count = 3 }) => {
    return (
        <>
            {[...Array(count)].map((_, index) => (
                <div key={index} className="skeleton-card">
                    <div className="skeleton-header">
                        <div className="skeleton-title"></div>
                        <div className="skeleton-title-short"></div>
                    </div>

                    <div className="skeleton-badges">
                        <div className="skeleton-badge"></div>
                        <div className="skeleton-badge"></div>
                        <div className="skeleton-badge"></div>
                    </div>

                    <div className="skeleton-date"></div>

                    <div className="skeleton-text"></div>
                    <div className="skeleton-text"></div>
                    <div className="skeleton-text-short"></div>

                    <div className="skeleton-actions">
                        <div className="skeleton-button"></div>
                        <div className="skeleton-button"></div>
                        <div className="skeleton-button"></div>
                    </div>
                </div>
            ))}
        </>
    );
};

export default SkeletonLoader;
