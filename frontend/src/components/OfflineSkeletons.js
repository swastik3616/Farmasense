import React from 'react';

const OfflineAlertBox = () => {
    return (
        <div style={{
            position: 'sticky', top: 0, zIndex: 50,
            background: '#b91c1c', color: 'white',
            padding: '10px 20px', textAlign: 'center',
            fontWeight: '600', fontSize: '0.9rem',
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
        }}>
            ⚠️ You are currently offline. Showing cached field data. Some features like AI chat may be disabled until connection is restored.
        </div>
    );
};

const SkeletonLoader = ({ height, width, borderRadius="8px", count=1, style={} }) => {
    const skeletons = [];
    for (let i = 0; i < count; i++) {
        skeletons.push(
            <div key={i} style={{
                height: height || '200px',
                width: width || '100%',
                borderRadius: borderRadius,
                background: 'linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%)',
                backgroundSize: '200% 100%',
                animation: 'skeleton-loading 1.5s infinite',
                margin: '10px 0',
                ...style
            }} />
        )
    }

    return (
        <>
            <style>{`
                @keyframes skeleton-loading {
                    0% { background-position: 200% 0; }
                    100% { background-position: -200% 0; }
                }
            `}</style>
            <div className="skeleton-container" style={{display: 'flex', flexDirection: 'column', gap: '15px'}}>
                {skeletons}
            </div>
        </>
    );
};

export { OfflineAlertBox, SkeletonLoader };
