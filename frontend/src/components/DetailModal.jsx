import React from 'react';
import './DetailModal.css';

const DetailModal = ({ isOpen, onClose, title, data }) => {
    if (!isOpen) return null;

    // Parse JSON data if it's a string
    let details = {};
    try {
        details = typeof data === 'string' ? JSON.parse(data) : (data.data ? JSON.parse(data.data) : data);
    } catch (e) {
        details = data;
    }

    // Filter out internal/boring fields
    const skipFields = [
        'id', 'jnid', 'lecla_id', 'jn_contact_id', 'data', 'related',
        'date_created', 'date_updated', 'created_by', 'modified_by',
        'is_archived', 'primary_contact'
    ];

    const formatKey = (key) => {
        return key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={e => e.stopPropagation()}>
                <div className="modal-header">
                    <h2>{title} Details</h2>
                    <button className="close-btn" onClick={onClose}>&times;</button>
                </div>
                <div className="modal-body">
                    <div className="details-grid">
                        {Object.entries(details).map(([key, value]) => {
                            if (skipFields.includes(key.toLowerCase()) || !value) return null;

                            // Handle nested objects or arrays (like tags)
                            let displayValue = value;
                            if (Array.isArray(value)) {
                                displayValue = value.join(', ');
                            } else if (typeof value === 'object') {
                                return null; // Skip complex nested objects for now
                            }

                            return (
                                <div key={key} className="detail-item">
                                    <label>{formatKey(key)}</label>
                                    <span>{displayValue}</span>
                                </div>
                            );
                        })}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DetailModal;
