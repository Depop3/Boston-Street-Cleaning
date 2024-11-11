import { mapManager } from './map.js';
import { visualizationManager } from './visualization.js';

class SearchManager {
    constructor() {
        this.currentStreet = null;
    }

    initialize() {
        this.initializeSelect2();
        this.bindEvents();
    }

    initializeSelect2() {
        $('#street-select').select2({
            placeholder: "Type to search for a street...",
            allowClear: true,
            width: '100%'
        });
    }

    bindEvents() {
        $('#street-select').on('change', (e) => this.handleStreetSelection(e));
    }

    async handleStreetSelection(event) {
        const street = $(event.target).val();
        this.currentStreet = street;

        if (street) {
            this.showLoadingSpinner();
            this.hideScheduleDetails();
            mapManager.clearMarker();

            try {
                const response = await fetch(`/api/street-details/${encodeURIComponent(street)}`);
                const data = await response.json();

                if (data.error) {
                    throw new Error(data.error);
                }

                console.log('Received street details:', data);
                this.displayScheduleDetails(data);
                this.updateMapMarker(data[0]);
            } catch (error) {
                console.error('Error:', error);
                this.showAlert('danger', 'Error fetching street details. Please try again.');
            } finally {
                this.hideLoadingSpinner();
            }
        } else {
            this.hideScheduleDetails();
            mapManager.clearMarker();
        }
    }

    showLoadingSpinner() {
        $('#loading-spinner').removeClass('d-none');
    }

    hideLoadingSpinner() {
        $('#loading-spinner').addClass('d-none');
    }

    hideScheduleDetails() {
        $('#schedule-details').addClass('d-none');
    }

    showAlert(type, message) {
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        $('#alerts-container').html(alertHtml);
    }

    displayScheduleDetails(schedules) {
        $('#schedule-details').removeClass('d-none');
        $('#street-name').html(`
            <div class="d-flex justify-content-between align-items-center">
                <span>${schedules[0].street}</span>
                <button id="toggleVisualization" class="btn btn-outline-info btn-sm">
                    <i class="fas fa-route me-1"></i>
                    <span class="button-text">Show Route</span>
                </button>
            </div>
        `);

        const container = $('#schedules-container');
        container.empty();

        // Create side toggle buttons
        container.append(`
            <div class="side-toggle mb-3">
                <button class="btn btn-outline-primary active" data-side="even">Even Side</button>
                <button class="btn btn-outline-success" data-side="odd">Odd Side</button>
            </div>
        `);

        // Create district toggle buttons
        const uniqueDistricts = [...new Set(schedules.map(s => s.district))];
        container.append(`
            <div class="district-toggle mb-3">
                ${uniqueDistricts.map((district, index) => `
                    <button class="btn btn-outline-secondary mb-1 ${index === 0 ? 'active' : ''}" 
                            data-district="${district}">
                        ${district}
                    </button>
                `).join('')}
            </div>
        `);

        this.createScheduleCards(schedules, container);
        this.initializeToggles(schedules);
    }

    createScheduleCards(schedules, container) {
        console.log('Creating schedule cards with data:', schedules);
        
        schedules.forEach((schedule, index) => {
            // Default to even side if not specified
            const side = schedule.side || (index % 2 === 0 ? 'Even' : 'Odd');
            const isEven = side.toLowerCase().includes('even');
            const sideColor = isEven ? 'primary' : 'success';
            
            console.log(`Schedule ${index}:`, {
                district: schedule.district,
                side: side,
                isEven: isEven
            });
            
            container.append(`
                <div class="schedule-card ${isEven ? 'even-side' : 'odd-side'} district-${schedule.district.replace(/\s+/g, '-')}"
                     ${!isEven ? 'style="display: none;"' : ''}>
                    <div class="card border-${sideColor} mb-3">
                        <div class="card-header bg-${sideColor} text-white">
                            ${side} Side - ${schedule.district}
                        </div>
                        <div class="card-body">
                            ${this.createScheduleCardContent(schedule)}
                        </div>
                    </div>
                </div>
            `);
        });
    }

    createScheduleCardContent(schedule) {
        console.log('Creating card content for schedule:', schedule);
        
        // Safely format weeks and days
        const weeksFormatted = Array.isArray(schedule.weeks) 
            ? schedule.weeks.map(w => `${w}${this.getWeekSuffix(w)} week`).join(', ')
            : 'N/A';
            
        const daysFormatted = Array.isArray(schedule.days)
            ? schedule.days.map(d => d.charAt(0).toUpperCase() + d.slice(1)).join(', ')
            : 'N/A';
    
        // Optional fields with fallbacks
        const fromStreet = schedule.from_street || 'Start';
        const toStreet = schedule.to_street || 'End';
        const miles = typeof schedule.miles === 'number' 
        ? `<p><strong>Length:</strong> ${schedule.miles.toFixed(2)} miles</p>` 
            : '';
        const section = typeof schedule.section === 'string' 
            ? `<p><strong>Section:</strong> ${schedule.section}</p>` 
            : '';
    
        return `
            <div class="next-cleaning-countdown alert alert-info">
                <h6>Next Cleaning:</h6>
                <p class="mb-1">${this.formatNextCleaning(schedule)}</p>
            </div>
            <p><strong>Time:</strong> ${schedule.time || 'N/A'}</p>
            ${fromStreet !== 'Start' || toStreet !== 'End' 
                ? `<p><strong>Location:</strong> From ${fromStreet} to ${toStreet}</p>`
                : ''}
            <p><strong>Cleaning Schedule:</strong></p>
            <ul>
                <li>Weeks: ${weeksFormatted}</li>
                <li>Days: ${daysFormatted}</li>
            </ul>
            ${section}
            ${miles}
        `;
    }
    formatNextCleaning(schedule) {
        // Add your existing next cleaning calculation logic here
        return 'Next cleaning date calculation';
    }

    getWeekSuffix(num) {
        const j = num % 10;
        const k = num % 100;
        if (j == 1 && k != 11) return "st";
        if (j == 2 && k != 12) return "nd";
        if (j == 3 && k != 13) return "rd";
        return "th";
    }

    initializeToggles(schedules) {
        // Side toggle
        $('.side-toggle button').click(function() {
            const side = $(this).data('side');
            $('.side-toggle button').removeClass('active');
            $(this).addClass('active');
            $('.schedule-card').hide();
            $(`.${side}-side:not(.district-hidden)`).show();
        });

        // District toggle
        $('.district-toggle button').click(function() {
            const district = $(this).data('district');
            $('.district-toggle button').removeClass('active');
            $(this).addClass('active');
            
            const activeSide = $('.side-toggle button.active').data('side');
            $('.schedule-card').hide();
            $(`.${activeSide}-side.district-${district.replace(/\s+/g, '-')}`).show();
        });
    }

    updateMapMarker(data) {
        mapManager.updateMarker(data);
    }
}

export const searchManager = new SearchManager(); 