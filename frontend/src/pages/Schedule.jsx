import React, { useEffect, useState } from 'react';
import { fetchCalendar } from '../services/api';

function Schedule() {
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadCalendar = async () => {
            setLoading(true);
            try {
                const data = await fetchCalendar();
                setEvents(Array.isArray(data) ? data : []);
            } catch (err) {
                console.error("Failed to load calendar", err);
            } finally {
                setLoading(false);
            }
        };
        loadCalendar();
    }, []);

    const formatDateTime = (dateTimeStr, dateStr) => {
        const dt = dateTimeStr || dateStr;
        if (!dt) return '—';
        const date = new Date(dt);

        if (dateStr) {
            return date.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' }) + " (All Day)";
        }

        return date.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' }) +
            " at " +
            date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
    };

    return (
        <div className="schedule-page">
            <header style={{ marginBottom: '2rem' }}>
                <h1>Team Schedule</h1>
                <p style={{ color: 'var(--color-text-muted)' }}>Upcoming appointments and project milestones</p>
            </header>

            {loading ? (
                <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
                    <p>Loading schedule...</p>
                </div>
            ) : (
                <div className="calendar-list" style={{ maxWidth: '900px', margin: '0 auto' }}>
                    {events.length > 0 ? (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                            {events.map((event) => (
                                <div key={event.id} className="card event-card" style={{
                                    display: 'flex',
                                    gap: '24px',
                                    alignItems: 'center',
                                    padding: '24px',
                                    border: '1px solid rgba(255,255,255,0.05)',
                                    transition: 'transform 0.2s ease, box-shadow 0.2s ease',
                                    cursor: 'default'
                                }}>
                                    <div className="event-date-box" style={{
                                        minWidth: '100px',
                                        textAlign: 'center',
                                        padding: '15px 10px',
                                        background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(37, 99, 235, 0.05))',
                                        borderRadius: '12px',
                                        border: '1px solid rgba(59, 130, 246, 0.2)',
                                        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                                    }}>
                                        <div style={{ fontSize: '0.85rem', color: '#60a5fa', fontWeight: '800', marginBottom: '4px', letterSpacing: '0.05em' }}>
                                            {new Date(event.start?.dateTime || event.start?.date).toLocaleDateString('en-US', { month: 'short' }).toUpperCase()}
                                        </div>
                                        <div style={{ fontSize: '1.8rem', fontWeight: '900', color: 'white' }}>
                                            {new Date(event.start?.dateTime || event.start?.date).getDate()}
                                        </div>
                                    </div>

                                    <div className="event-info" style={{ flex: 1 }}>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                                            <h3 style={{ margin: 0, fontSize: '1.25rem', fontWeight: '700' }}>{event.summary || "Untitled Event"}</h3>
                                            <span style={{
                                                padding: '2px 8px',
                                                borderRadius: '4px',
                                                fontSize: '0.7rem',
                                                background: 'rgba(59, 130, 246, 0.1)',
                                                color: '#60a5fa',
                                                border: '1px solid rgba(59, 130, 246, 0.2)'
                                            }}>
                                                Google Calendar
                                            </span>
                                        </div>
                                        <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                                            <div style={{ fontSize: '0.9rem', color: 'var(--color-text-muted)', display: 'flex', alignItems: 'center', gap: '8px' }}>
                                                <span>🕒 {formatDateTime(event.start?.dateTime, event.start?.date)}</span>
                                            </div>
                                            {event.location && (
                                                <div style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)', display: 'flex', alignItems: 'center', gap: '8px' }}>
                                                    <span>📍 {event.location}</span>
                                                </div>
                                            )}
                                        </div>
                                        {event.description && (
                                            <p style={{
                                                margin: '15px 0 0',
                                                fontSize: '0.85rem',
                                                color: 'rgba(255,255,255,0.5)',
                                                lineHeight: '1.5',
                                                padding: '12px',
                                                background: 'rgba(0,0,0,0.15)',
                                                borderRadius: '8px'
                                            }}>
                                                {event.description}
                                            </p>
                                        )}
                                    </div>

                                    <div className="event-action">
                                        <button style={{
                                            padding: '8px 16px',
                                            borderRadius: '8px',
                                            fontSize: '0.85rem',
                                            background: 'rgba(16, 185, 129, 0.1)',
                                            color: '#10b981',
                                            border: '1px solid rgba(16, 185, 129, 0.2)',
                                            fontWeight: '600',
                                            cursor: 'pointer'
                                        }}>
                                            Details
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="card" style={{ textAlign: 'center', padding: '80px 40px', background: 'rgba(255,255,255,0.02)' }}>
                            <div style={{ fontSize: '4rem', marginBottom: '24px', opacity: 0.5 }}>📅</div>
                            <h3 style={{ fontSize: '1.5rem', marginBottom: '12px' }}>Clear Schedule</h3>
                            <p style={{ color: 'var(--color-text-muted)', fontSize: '1.05rem' }}>No upcoming events found for the next period.</p>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default Schedule;
