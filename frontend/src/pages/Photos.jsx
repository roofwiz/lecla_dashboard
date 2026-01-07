import React, { useEffect, useState } from 'react';
import api, { fetchProjects } from '../services/api';

function Photos() {
    const [projects, setProjects] = useState([]);
    const [photos, setPhotos] = useState({}); // project_id -> photos
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadPhotos = async () => {
            setLoading(true);
            try {
                // 1. Get recent projects
                const projectData = await fetchProjects();
                setProjects(Array.isArray(projectData) ? projectData : []);

                // 2. Fetch photos for each project (first 4)
                const photoMap = {};

                if (Array.isArray(projectData)) {
                    // Concurrent fetches for photos using the central api instance
                    await Promise.all(projectData.slice(0, 8).map(async (p) => {
                        try {
                            const resp = await api.get(`/photos?project_id=${p.id}&limit=4`);
                            photoMap[p.id] = resp.data;
                        } catch (e) {
                            console.error(`Failed to fetch photos for project ${p.id}`, e);
                        }
                    }));
                }

                setPhotos(photoMap);
            } catch (err) {
                console.error("Failed to load photos", err);
            } finally {
                setLoading(false);
            }
        };
        loadPhotos();
    }, []);

    return (
        <div className="photos-page">
            <header style={{ marginBottom: '2rem' }}>
                <h1>Project Gallery</h1>
                <p style={{ color: 'var(--color-text-muted)' }}>Latest updates from CompanyCam</p>
            </header>

            {loading ? (
                <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
                    <p>Loading projects and photos...</p>
                </div>
            ) : (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '25px' }}>
                    {projects.map(project => (
                        <div key={project.id} className="card photo-project-card" style={{
                            padding: '0',
                            overflow: 'hidden',
                            transition: 'transform 0.3s ease, box-shadow 0.3s ease',
                            cursor: 'default'
                        }}>
                            <div style={{ padding: '20px', background: 'rgba(255,255,255,0.02)', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                                <h3 style={{ margin: '0', fontSize: '1.2rem', color: 'var(--color-primary)' }}>{project.name}</h3>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginTop: '8px' }}>
                                    <span style={{ fontSize: '1.2rem' }}>📍</span>
                                    <p style={{ margin: '0', fontSize: '0.85rem', color: 'var(--color-text-muted)' }}>
                                        {project.address?.street_address}, {project.address?.city}, {project.address?.state}
                                    </p>
                                </div>
                            </div>

                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '4px', padding: '10px', background: 'rgba(0,0,0,0.1)' }}>
                                {(photos[project.id] || []).map(photo => (
                                    <div key={photo.id} style={{
                                        aspectRatio: '1/1',
                                        overflow: 'hidden',
                                        borderRadius: '4px',
                                        position: 'relative'
                                    }}>
                                        <img
                                            src={photo.thumbnails?.medium || photo.uri}
                                            alt="Project"
                                            style={{
                                                width: '100%',
                                                height: '100%',
                                                objectFit: 'cover',
                                                transition: 'transform 0.5s ease'
                                            }}
                                            onMouseOver={e => e.currentTarget.style.transform = 'scale(1.1)'}
                                            onMouseOut={e => e.currentTarget.style.transform = 'scale(1.0)'}
                                        />
                                    </div>
                                ))}
                                {(!photos[project.id] || photos[project.id].length === 0) && (
                                    <div style={{
                                        padding: '60px 20px',
                                        gridColumn: 'span 2',
                                        textAlign: 'center',
                                        color: 'var(--color-text-muted)',
                                        fontSize: '0.9rem',
                                        fontStyle: 'italic'
                                    }}>
                                        No recent photos captured
                                    </div>
                                )}
                            </div>
                            <div style={{ padding: '12px', textAlign: 'right' }}>
                                <button style={{
                                    background: 'transparent',
                                    border: '1px solid rgba(255,255,255,0.1)',
                                    color: 'white',
                                    padding: '5px 12px',
                                    borderRadius: '4px',
                                    fontSize: '0.8rem',
                                    cursor: 'pointer'
                                }}>
                                    View full project →
                                </button>
                            </div>
                        </div>
                    ))}
                    {projects.length === 0 && (
                        <div className="card" style={{ gridColumn: 'span 3', textAlign: 'center', padding: '60px' }}>
                            <div style={{ fontSize: '3rem', marginBottom: '20px' }}>📸</div>
                            <h3>No CompanyCam Projects</h3>
                            <p style={{ color: 'var(--color-text-muted)' }}>We couldn't find any projects linked to your account.</p>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default Photos;
