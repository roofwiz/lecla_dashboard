import React, { useEffect, useState } from 'react';
import { fetchCRMContacts, triggerSync } from '../services/api';
import DetailModal from '../components/DetailModal';
import JobNimbusButton, { JobNimbusIcon } from '../components/JobNimbusButton';

function Contacts() {
    const [contacts, setContacts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [syncing, setSyncing] = useState(false);
    const [selectedContact, setSelectedContact] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);

    const loadContacts = async () => {
        setLoading(true);
        try {
            const data = await fetchCRMContacts();
            setContacts(data);
        } catch (err) {
            console.error("Failed to load contacts", err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadContacts();
    }, []);

    const handleSync = async () => {
        setSyncing(true);
        try {
            await triggerSync();
            alert("Sync started in background. Please refresh in a few moments.");
        } catch (err) {
            alert("Failed to start sync");
        } finally {
            setSyncing(false);
        }
    };

    const handleRowClick = (contact) => {
        setSelectedContact(contact);
        setIsModalOpen(true);
    };

    return (
        <div className="crm-container">
            <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h2>CRM Contacts</h2>
                <div style={{ display: 'flex', gap: '10px' }}>
                    <button onClick={loadContacts} className="btn-refresh" style={{ padding: '10px 15px', background: 'rgba(255,255,255,0.1)', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' }}>
                        🔄 Refresh
                    </button>
                    <button
                        onClick={handleSync}
                        disabled={syncing}
                        className="btn-sync"
                        style={{
                            padding: '10px 20px',
                            background: 'var(--color-accent)',
                            color: 'white',
                            border: 'none',
                            borderRadius: '6px',
                            cursor: 'pointer'
                        }}
                    >
                        {syncing ? "Syncing..." : "Force JN Sync"}
                    </button>
                </div>
            </div>

            <div className="card">
                {loading ? (
                    <p>Loading contacts...</p>
                ) : (
                    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                        <thead>
                            <tr style={{ textAlign: 'left', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
                                <th style={{ padding: '12px' }}>Name</th>
                                <th style={{ padding: '12px' }}>Email</th>
                                <th style={{ padding: '12px' }}>Phone</th>
                                <th style={{ padding: '12px' }}>Location</th>
                                <th style={{ padding: '12px' }}>Status</th>
                                <th style={{ padding: '12px', width: '50px' }}>JN</th>
                            </tr>
                        </thead>
                        <tbody>
                            {contacts.map(contact => {
                                // Extract status and name from JSON if possible
                                let details = {};
                                try { details = JSON.parse(contact.data); } catch (e) { }

                                const status = details.status_name || contact.status || 'Active';

                                // Robust name display
                                let displayName = `${contact.first_name || ''} ${contact.last_name || ''} `.trim();
                                if (!displayName) {
                                    displayName = details.display_name || details.company || 'Unnamed Contact';
                                }

                                return (
                                    <tr
                                        key={contact.lecla_id}
                                        onClick={() => handleRowClick(contact)}
                                        className="clickable-row"
                                        style={{ borderBottom: '1px solid rgba(255,255,255,0.05)', cursor: 'pointer' }}
                                    >
                                        <td style={{ padding: '12px', fontWeight: '500' }}>{displayName}</td>
                                        <td style={{ padding: '12px' }}>{contact.email || '—'}</td>
                                        <td style={{ padding: '12px' }}>{contact.phone || '—'}</td>
                                        <td style={{ padding: '12px' }}>{contact.city}, {contact.state}</td>
                                        <td style={{ padding: '12px' }}>
                                            <span style={{
                                                fontSize: '0.75em',
                                                background: 'rgba(78, 115, 223, 0.1)',
                                                color: '#4e73df',
                                                padding: '4px 8px',
                                                borderRadius: '12px',
                                                border: '1px solid rgba(78, 115, 223, 0.2)'
                                            }}>
                                                {status}
                                            </span>
                                        </td>
                                        <td style={{ padding: '12px', textAlign: 'center' }}>
                                            <JobNimbusIcon type="contacts" id={contact.jn_contact_id} title={displayName} />
                                        </td>
                                    </tr>
                                );
                            })}
                            {contacts.length === 0 && (
                                <tr>
                                    <td colSpan="5" style={{ padding: '20px', textAlign: 'center' }}>No contacts found. Try syncing.</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                )}
            </div>

            <DetailModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                title={selectedContact ? (selectedContact.first_name ? `${selectedContact.first_name} ${selectedContact.last_name} ` : (JSON.parse(selectedContact.data).display_name || 'Contact')) : 'Contact'}
                data={selectedContact}
            />
        </div>
    );
}

export default Contacts;
