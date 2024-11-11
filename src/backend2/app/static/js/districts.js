export const districtColors = {
    'North Dorchester': '#FF6B6B',
    'South Dorchester': '#4ECDC4',
    'East Boston': '#45B7D1',
    'South Boston': '#96CEB4',
    'Roxbury': '#FFEEAD',
    'Jamaica Plain': '#D4A5A5',
    'Charlestown': '#9B59B6',
    'West Roxbury': '#3498DB',
    'Brighton': '#E74C3C',
    'Hyde Park': '#2ECC71'
};

class DistrictManager {
    constructor() {
        this.activeDistrict = null;
    }

    initialize() {
        this.bindEvents();
    }

    bindEvents() {
        $(document).on('click', '.district-toggle button', (e) => {
            const button = $(e.currentTarget);
            const district = button.data('district');
            
            $('.district-toggle button').removeClass('active');
            button.addClass('active');
            
            this.activeDistrict = district;
            this.triggerDistrictChange(district);
        });
    }

    getDistrictColor(district) {
        return districtColors[district] || '#666666';
    }

    triggerDistrictChange(district) {
        $(document).trigger('districtChanged', [district]);
    }

    getActiveDistrict() {
        return this.activeDistrict;
    }
}

export const districtManager = new DistrictManager(); 