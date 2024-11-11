class ReportManager {
    constructor() {
        this.modal = null;
    }

    initialize() {
        this.modal = new bootstrap.Modal(document.getElementById('reportModal'));
        this.bindEvents();
    }

    bindEvents() {
        $('#reportIssueBtn').click(() => this.showReportModal());
        $('#submitReport').click(() => this.handleSubmission());
    }

    showReportModal() {
        const streetName = $('#street-name span').text();
        $('#reportStreet').val(streetName);
        this.modal.show();
    }

    async handleSubmission() {
        const submitBtn = $('#submitReport');
        const reportData = {
            street: $('#reportStreet').val(),
            type: $('#reportType').val(),
            description: $('#reportDescription').val(),
            email: $('#reportEmail').val(),
            timestamp: new Date().toISOString(),
            status: 'pending'
        };

        if (!this.validateReport(reportData)) {
            return;
        }

        this.setSubmitLoading(submitBtn, true);

        try {
            const response = await fetch('/api/report', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(reportData)
            });

            const data = await response.json();
            
            if (response.ok) {
                this.handleSuccess();
            } else {
                throw new Error(data.error || 'Failed to submit report');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showAlert('danger', 'Error submitting report. Please try again.');
        } finally {
            this.setSubmitLoading(submitBtn, false);
        }
    }

    validateReport(data) {
        if (!data.type || !data.description) {
            this.showAlert('danger', 'Please fill in all required fields');
            return false;
        }
        return true;
    }

    setSubmitLoading(button, isLoading) {
        button.prop('disabled', isLoading);
        button.html(isLoading ? 
            '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Submitting...' : 
            'Submit Report'
        );
    }

    handleSuccess() {
        this.modal.hide();
        this.showAlert('success', 'Thank you for your report! We will review it shortly.');
        $('#reportForm')[0].reset();
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
}

export const reportManager = new ReportManager(); 