import React, { useState, useEffect } from 'react';
import { GoogleMap, useJsApiLoader, Marker } from '@react-google-maps/api';
import api from '../services/api';

const containerStyle = {
    width: '100%',
    height: '400px',
    borderRadius: '12px'
};

const center = {
    lat: 41.65, // Default to a central Connecticut location
    lng: -72.7
};

function MapWidget({ projects }) {
    const [apiKey, setApiKey] = useState('');
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchConfig = async () => {
            try {
                const resp = await api.get('/config');
                if (resp.data.google_maps_api_key) {
                    setApiKey(resp.data.google_maps_api_key);
                } else {
                    setError("Google Maps API Key missing in backend configuration.");
                }
            } catch (err) {
                console.error("Failed to load map config", err);
                setError("Failed to connect to backend configuration.");
            }
        };
        fetchConfig();
    }, []);

    if (error) return <div className="card" style={{ height: '400px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#ef4444' }}>{error}</div>;
    if (!apiKey) return <div className="card" style={{ height: '400px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>Loading Map Configuration...</div>;

    return <MapContent apiKey={apiKey} projects={projects} />;
}

function MapContent({ apiKey, projects }) {
    const { isLoaded, loadError } = useJsApiLoader({
        id: 'google-map-script',
        googleMapsApiKey: apiKey
    });

    const [map, setMap] = useState(null);

    const onLoad = React.useCallback(function callback(map) {
        setMap(map);
    }, []);

    const onUnmount = React.useCallback(function callback(map) {
        setMap(null);
    }, []);

    const markers = projects?.filter(p => p.coordinates?.latitude && p.coordinates?.longitude).map(p => ({
        id: p.id,
        name: p.name,
        position: {
            lat: parseFloat(p.coordinates.latitude),
            lng: parseFloat(p.coordinates.longitude)
        }
    })) || [];

    if (loadError) return <div className="card" style={{ height: '400px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>Error loading maps</div>;
    if (!isLoaded) return <div className="card" style={{ height: '400px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>Initializing Maps...</div>;

    return (
        <div className="card map-card" style={{ padding: '0', overflow: 'hidden' }}>
            <GoogleMap
                mapContainerStyle={containerStyle}
                center={markers.length > 0 ? markers[0].position : center}
                zoom={9}
                onLoad={onLoad}
                onUnmount={onUnmount}
                options={{
                    styles: [
                        { elementType: "geometry", stylers: [{ color: "#242f3e" }] },
                        { elementType: "labels.text.stroke", stylers: [{ color: "#242f3e" }] },
                        { elementType: "labels.text.fill", stylers: [{ color: "#746855" }] },
                        {
                            featureType: "administrative.locality",
                            elementType: "labels.text.fill",
                            stylers: [{ color: "#d59563" }],
                        },
                        {
                            featureType: "poi",
                            elementType: "labels.text.fill",
                            stylers: [{ color: "#d59563" }],
                        },
                        {
                            featureType: "road",
                            elementType: "geometry",
                            stylers: [{ color: "#38414e" }],
                        },
                        {
                            featureType: "road",
                            elementType: "geometry.stroke",
                            stylers: [{ color: "#212a37" }],
                        },
                        {
                            featureType: "water",
                            elementType: "geometry",
                            stylers: [{ color: "#17263c" }],
                        },
                    ]
                }}
            >
                {markers.map(marker => (
                    <Marker
                        key={marker.id}
                        position={marker.position}
                        title={marker.name}
                    />
                ))}
            </GoogleMap>
        </div>
    );
}

export default React.memo(MapWidget);
