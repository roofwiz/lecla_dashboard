/**
 * JobNimbus Integration Utilities
 * Provides controlled window popup for JobNimbus records
 */

const JN_BASE_URL = 'https://app.jobnimbus.com';

/**
 * Open JobNimbus record in a controlled popup window
 * @param {string} type - Record type ('job', 'contact', 'estimate', 'invoice')
 * @param {string} id - JobNimbus record ID
 * @param {string} title - Window title (optional)
 */
export function openJobNimbusWindow(type, id, title = '') {
    if (!id) {
        console.error('JobNimbus ID is required to open window');
        return;
    }

    const url = `${JN_BASE_URL}/${type}/${id}`;
    const windowName = `jobnimbus_${type}_${id}`;

    // Window features for controlled popup
    const features = [
        'width=1200',
        'height=800',
        'left=100',
        'top=100',
        'resizable=yes',
        'scrollbars=yes',
        'status=yes',
        'toolbar=yes',
        'menubar=no',
        'location=yes'
    ].join(',');

    // Open window and focus it
    const popup = window.open(url, windowName, features);

    if (popup) {
        popup.focus();
    } else {
        // Popup blocked - fallback to new tab
        console.warn('Popup blocked, opening in new tab');
        window.open(url, '_blank');
    }
}

/**
 * Get JobNimbus deep link URL
 */
export function getJobNimbusUrl(type, id) {
    return `${JN_BASE_URL}/${type}/${id}`;
}

export default {
    openJobNimbusWindow,
    getJobNimbusUrl,
    JN_BASE_URL
};
