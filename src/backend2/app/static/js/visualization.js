import { mapManager } from './map.js';
import { districtManager } from './districts.js';

class VisualizationManager {
    constructor() {
        this.currentSegments = [];
        this.currentDecorators = [];
        this.isActive = false;
    }

    initialize() {
        this.bindEvents();
    }

    bindEvents() {
        $(document).on('click', '#toggleVisualization', () => this.toggleVisualization());
    }

    async visualizeStreetSegments(street, district) {
        this.clearSegments();
        
        try {
            const response = await fetch(`/api/street-segments/${encodeURIComponent(street)}`);
            const segments = await response.json();
            
            const relevantSegments = district ? 
                segments.filter(s => s.district === district) : 
                segments;

            const promises = relevantSegments.map(segment => {
                return Promise.all([
                    this.geocodeIntersection(street, segment.from_street),
                    this.geocodeIntersection(street, segment.to_street)
                ]).then(([fromCoords, toCoords]) => {
                    return this.createSegmentVisualization(street, segment, fromCoords, toCoords);
                });
            });

            await Promise.all(promises);
        } catch (error) {
            console.error('Error visualizing segments:', error);
            alert('Error loading street visualization');
        }
    }

    async geocodeIntersection(street1, street2) {
        const address = `${street1} and ${street2}, Boston, MA`;
        const response = await fetch(`/api/geocode?address=${encodeURIComponent(address)}`);
        return response.json();
    }

    createSegmentVisualization(street, segment, fromCoords, toCoords) {
        const path = L.polyline([
            [fromCoords.lat, fromCoords.lng],
            [toCoords.lat, toCoords.lng]
        ], {
            color: districtManager.getDistrictColor(segment.district),
            weight: 4,
            opacity: 0.8
        }).addTo(mapManager.getMap());

        const decorator = L.polylineDecorator(path, {
            patterns: [{
                offset: '0%',
                repeat: 50,
                symbol: L.Symbol.arrowHead({
                    pixelSize: 15,
                    polygon: false,
                    pathOptions: {
                        color: districtManager.getDistrictColor(segment.district),
                        fillOpacity: 1,
                        weight: 2
                    }
                })
            }]
        }).addTo(mapManager.getMap());

        path.bindPopup(this.createPopupContent(street, segment));

        this.currentSegments.push(path);
        this.currentDecorators.push(decorator);
        this.animateDecorator(decorator);

        mapManager.fitBounds(path.getBounds());
    }

    createPopupContent(street, segment) {
        return `
            <strong>${street}</strong><br>
            <i class="fas fa-arrow-right me-1"></i> From: ${segment.from_street}<br>
            <i class="fas fa-arrow-left me-1"></i> To: ${segment.to_street}<br>
            <i class="fas fa-map-marker-alt me-1"></i> District: ${segment.district}<br>
            <i class="fas fa-road me-1"></i> Side: ${segment.side}<br>
            <i class="fas fa-ruler me-1"></i> Length: ${segment.length.toFixed(2)} miles
        `;
    }

    animateDecorator(decorator) {
        let offset = 0;
        
        const animate = () => {
            offset = (offset + 1) % 50;
            decorator.setPatterns([{
                offset: offset + '%',
                repeat: 50,
                symbol: L.Symbol.arrowHead({
                    pixelSize: 15,
                    polygon: false,
                    pathOptions: {
                        color: decorator.options.patterns[0].symbol.options.pathOptions.color,
                        fillOpacity: 1,
                        weight: 2
                    }
                })
            }]);
            requestAnimationFrame(animate);
        };
        
        animate();
    }

    clearSegments() {
        this.currentSegments.forEach(segment => segment.remove());
        this.currentDecorators.forEach(decorator => decorator.remove());
        this.currentSegments = [];
        this.currentDecorators = [];
    }

    toggleVisualization() {
        const button = $('#toggleVisualization');
        const street = $('#street-name span').text();
        const district = districtManager.getActiveDistrict();
        
        if (!this.isActive) {
            button.removeClass('btn-outline-info').addClass('btn-info');
            button.find('.button-text').text('Hide Route');
            this.visualizeStreetSegments(street, district);
            this.isActive = true;
        } else {
            button.removeClass('btn-info').addClass('btn-outline-info');
            button.find('.button-text').text('Show Route');
            this.clearSegments();
            this.isActive = false;
        }
    }
}

export const visualizationManager = new VisualizationManager();