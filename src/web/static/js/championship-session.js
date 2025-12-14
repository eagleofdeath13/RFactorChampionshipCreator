/**
 * Championship Creation Session Manager
 *
 * Handles saving and restoring championship creation progress
 * using browser localStorage.
 */

const CHAMPIONSHIP_SESSION_KEY = 'rfactor_championship_draft';

class ChampionshipSessionManager {
    constructor() {
        this.currentStep = 1;
        this.data = {
            step: 1,
            name: '',
            fullName: '',
            selectedVehicles: [],
            vehicleDriverAssignments: {},
            selectedTracks: [],
            trackOrder: [],
            timestamp: null
        };
    }

    /**
     * Save current session to localStorage
     */
    save() {
        this.data.step = this.currentStep;
        this.data.timestamp = new Date().toISOString();
        localStorage.setItem(CHAMPIONSHIP_SESSION_KEY, JSON.stringify(this.data));
        console.log('[Session] Saved championship draft:', this.data);
    }

    /**
     * Load session from localStorage
     * @returns {boolean} True if session was loaded, false otherwise
     */
    load() {
        try {
            const saved = localStorage.getItem(CHAMPIONSHIP_SESSION_KEY);
            if (!saved) {
                return false;
            }

            this.data = JSON.parse(saved);
            this.currentStep = this.data.step || 1;
            console.log('[Session] Loaded championship draft:', this.data);
            return true;
        } catch (error) {
            console.error('[Session] Failed to load draft:', error);
            return false;
        }
    }

    /**
     * Clear session from localStorage
     */
    clear() {
        localStorage.removeItem(CHAMPIONSHIP_SESSION_KEY);
        console.log('[Session] Cleared championship draft');
        this.data = {
            step: 1,
            name: '',
            fullName: '',
            selectedVehicles: [],
            vehicleDriverAssignments: {},
            selectedTracks: [],
            trackOrder: [],
            timestamp: null
        };
        this.currentStep = 1;
    }

    /**
     * Check if there's a saved draft
     * @returns {boolean}
     */
    hasDraft() {
        return localStorage.getItem(CHAMPIONSHIP_SESSION_KEY) !== null;
    }

    /**
     * Get draft age in minutes
     * @returns {number|null}
     */
    getDraftAge() {
        if (!this.data.timestamp) {
            return null;
        }
        const now = new Date();
        const timestamp = new Date(this.data.timestamp);
        return Math.floor((now - timestamp) / 1000 / 60);
    }

    /**
     * Update championship name
     */
    setName(name) {
        this.data.name = name;
        this.save();
    }

    /**
     * Update championship full name
     */
    setFullName(fullName) {
        this.data.fullName = fullName;
        this.save();
    }

    /**
     * Set selected vehicles
     */
    setSelectedVehicles(vehicles) {
        this.data.selectedVehicles = vehicles;
        this.save();
    }

    /**
     * Set vehicle-driver assignments
     */
    setVehicleDriverAssignments(assignments) {
        this.data.vehicleDriverAssignments = assignments;
        this.save();
    }

    /**
     * Set selected tracks
     */
    setSelectedTracks(tracks) {
        this.data.selectedTracks = tracks;
        this.save();
    }

    /**
     * Set track order
     */
    setTrackOrder(order) {
        this.data.trackOrder = order;
        this.save();
    }

    /**
     * Move to a specific step
     */
    goToStep(step) {
        this.currentStep = step;
        this.save();
    }

    /**
     * Get formatted draft information for display
     */
    getDraftInfo() {
        if (!this.hasDraft()) {
            return null;
        }

        const age = this.getDraftAge();
        let ageText = 'Inconnu';
        if (age !== null) {
            if (age < 1) {
                ageText = "À l'instant";
            } else if (age < 60) {
                ageText = `Il y a ${age} minute${age > 1 ? 's' : ''}`;
            } else if (age < 1440) {
                const hours = Math.floor(age / 60);
                ageText = `Il y a ${hours} heure${hours > 1 ? 's' : ''}`;
            } else {
                const days = Math.floor(age / 1440);
                ageText = `Il y a ${days} jour${days > 1 ? 's' : ''}`;
            }
        }

        return {
            name: this.data.name || 'Sans nom',
            step: this.data.step,
            vehicleCount: this.data.selectedVehicles?.length || 0,
            trackCount: this.data.selectedTracks?.length || 0,
            age: ageText,
            timestamp: this.data.timestamp
        };
    }

    /**
     * Export draft data for review
     */
    export() {
        return JSON.parse(JSON.stringify(this.data));
    }
}

// Create global instance
window.championshipSession = new ChampionshipSessionManager();

/**
 * Show restore draft dialog on page load
 */
function checkForDraft() {
    if (window.championshipSession.hasDraft()) {
        const info = window.championshipSession.getDraftInfo();
        const message = `
Un brouillon de championnat existe déjà :

📋 Nom : ${info.name}
⏱️ Créé : ${info.age}
📍 Étape : ${info.step}/5
🚗 Véhicules : ${info.vehicleCount}
🏁 Circuits : ${info.trackCount}

Voulez-vous reprendre depuis cette sauvegarde ?
        `.trim();

        if (confirm(message)) {
            restoreDraft();
        } else {
            // Ask if they want to start fresh
            if (confirm('Voulez-vous supprimer ce brouillon et recommencer ?')) {
                window.championshipSession.clear();
            }
        }
    }
}

/**
 * Restore draft and populate form
 */
function restoreDraft() {
    if (!window.championshipSession.load()) {
        console.warn('[Session] No draft to restore');
        return;
    }

    const data = window.championshipSession.export();

    // Restore step 1 data
    const nameInput = document.getElementById('championship-name');
    const fullNameInput = document.getElementById('championship-full-name');
    if (nameInput && data.name) {
        nameInput.value = data.name;
    }
    if (fullNameInput && data.fullName) {
        fullNameInput.value = data.fullName;
    }

    // Navigate to saved step
    if (data.step > 1) {
        // Gradually move through steps to restore all data
        for (let i = 1; i < data.step; i++) {
            moveToStep(i + 1, false); // false = don't save
        }
    }

    ToastNotification.success('Brouillon restauré avec succès');
}

/**
 * Clear draft with confirmation
 */
function clearDraftWithConfirmation() {
    if (confirm('⚠️ Êtes-vous sûr de vouloir abandonner ce championnat en cours ?\n\nCette action est irréversible.')) {
        window.championshipSession.clear();
        window.location.href = '/championships';
    }
}

// Auto-save on navigation
window.addEventListener('beforeunload', (e) => {
    // Only save if there's actual data
    const session = window.championshipSession;
    if (session.data.name || session.data.selectedVehicles?.length > 0) {
        session.save();
    }
});
