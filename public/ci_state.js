/**
 * ci_state.js — Cimeika Organism State Module
 *
 * Single state→manifest pipeline for the frontend PWA.
 * Persists to localStorage under CI_STATE key.
 * Dispatches window event 'ci:state_changed' on every commitState call.
 */

const STATE_KEY = 'CI_STATE';
const LEGACY_GITAPI_KEY = 'CI_GITAPI_URL';

const DEFAULT_STATE = {
    runtime: {
        mode: 'local',
        ci_gitapi_url: 'http://localhost:8000'
    },
    ui: {
        fab_enabled: true
    }
};

// Load initial state from localStorage, migrate legacy key if present
function _loadInitialState() {
    let state;
    try {
        const raw = localStorage.getItem(STATE_KEY);
        state = raw ? JSON.parse(raw) : null;
    } catch (e) {
        state = null;
    }

    if (!state) {
        state = structuredClone(DEFAULT_STATE);
    }

    // Migrate legacy CI_GITAPI_URL key (from PR#104)
    const legacyUrl = localStorage.getItem(LEGACY_GITAPI_KEY);
    if (legacyUrl) {
        state.runtime = state.runtime || {};
        state.runtime.ci_gitapi_url = legacyUrl;
        localStorage.removeItem(LEGACY_GITAPI_KEY);
        _persist(state);
    }

    return state;
}

function _persist(state) {
    localStorage.setItem(STATE_KEY, JSON.stringify(state));
}

// In-memory copy
let _state = _loadInitialState();

/**
 * Returns a shallow copy of the current state.
 */
function getState() {
    return structuredClone(_state);
}

/**
 * Merges partial update into state, persists, and dispatches ci:state_changed.
 * @param {Object} partial - Partial state object (deep merge at top level).
 */
function commitState(partial) {
    // Two-level shallow merge: top-level objects are merged with Object.assign
    for (const key of Object.keys(partial)) {
        if (
            typeof partial[key] === 'object' &&
            partial[key] !== null &&
            !Array.isArray(partial[key])
        ) {
            _state[key] = Object.assign({}, _state[key] || {}, partial[key]);
        } else {
            _state[key] = partial[key];
        }
    }
    _persist(_state);

    const snapshot = getState();
    window.dispatchEvent(new CustomEvent('ci:state_changed', { detail: snapshot }));
}

/**
 * Returns the derived ci.manifest snapshot object.
 */
function getManifestSnapshot() {
    return {
        schema_version: '1.0.0',
        updated_at: new Date().toISOString(),
        runtime: {
            mode: _state.runtime ? _state.runtime.mode : 'local',
            ci_gitapi_url: _state.runtime ? _state.runtime.ci_gitapi_url : DEFAULT_STATE.runtime.ci_gitapi_url
        },
        ui: {
            fab_enabled: _state.ui ? _state.ui.fab_enabled : true
        }
    };
}

// Expose on window for debug and cross-script use
window.ci = { getState, commitState, getManifestSnapshot };
