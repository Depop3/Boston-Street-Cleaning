import { mapManager } from './map.js';
import { searchManager } from './search.js';
import { reportManager } from './reports.js';
import { visualizationManager } from './visualization.js';
import { districtManager } from './districts.js';

class App {
    initialize() {
        // Initialize all managers
        mapManager.initialize();
        searchManager.initialize();
        reportManager.initialize();
        visualizationManager.initialize();
        districtManager.initialize();

        console.log('Application initialized');
    }
}

// Initialize the application when the document is ready
$(document).ready(() => {
    const app = new App();
    app.initialize();
}); 