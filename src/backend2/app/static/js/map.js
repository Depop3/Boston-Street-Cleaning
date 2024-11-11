class MapManager {
    constructor() {
        this.map = null;
        this.currentMarker = null;
        this.streetMarkers = new Map();
    }

    initialize() {
        this.map = L.map('map').setView([42.3601, -71.0589], 20);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(this.map);
    }

    updateMarker(data) {
        if (this.currentMarker) {
            this.map.removeLayer(this.currentMarker);
        }
        
        const marker = L.marker([data.lat, data.lng]).addTo(this.map);
        this.currentMarker = marker;
        
        this.streetMarkers.set(data.street.toLowerCase(), marker);
        this.map.setView([data.lat, data.lng], 16);
    }

    clearMarker() {
        if (this.currentMarker) {
            this.map.removeLayer(this.currentMarker);
            this.currentMarker = null;
        }
    }

    fitBounds(bounds, padding = 50) {
        this.map.fitBounds(bounds, { padding: [padding, padding] });
    }

    getMap() {
        return this.map;
    }
}

export const mapManager = new MapManager(); 