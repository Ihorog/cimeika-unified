/**
 * CIMEIKA App.js v2.0
 * Router + Grid Navigation + Service Worker Registration
 */

// State management
let modules = [];
let currentParent = null;
let navigationHistory = [];

/**
 * Initialize application
 */
async function init() {
    console.log('[CIMEIKA] Initializing...');
    
    // Load modules first
    await loadModules();
    
    // Check germination state
    const isGerminated = localStorage.getItem('isGerminated');
    
    if (!isGerminated) {
        // First time - show seed animation
        setTimeout(() => {
            localStorage.setItem('isGerminated', 'true');
            transitionToCore();
        }, 6000); // 3s animation + 3s delay
    } else {
        // Already germinated - go straight to core
        transitionToCore();
    }
    
    // Register service worker
    registerServiceWorker();
    
    // Setup event listeners
    setupEventListeners();
}

/**
 * Transition from seed to core
 */
function transitionToCore() {
    const seedContainer = document.getElementById('seed-container');
    const coreContainer = document.getElementById('core-container');
    
    seedContainer.style.display = 'none';
    coreContainer.style.display = 'block';
    
    // Render grid
    renderGrid();
}

/**
 * Load modules from JSON
 */
async function loadModules() {
    try {
        const response = await fetch('/modules.json');
        const data = await response.json();
        modules = data.modules;
        console.log('[CIMEIKA] Loaded modules:', modules);
    } catch (error) {
        console.error('[CIMEIKA] Failed to load modules:', error);
        modules = [];
    }
}

/**
 * Render bento grid
 */
function renderGrid(parentId = null) {
    const grid = document.getElementById('bentoGrid');
    if (!grid) return;
    
    // Filter modules by parent
    let visibleModules;
    if (parentId) {
        visibleModules = modules.filter(m => m.parent === parentId);
    } else {
        visibleModules = modules.filter(m => !m.parent);
    }
    
    // Update breadcrumb
    updateBreadcrumb(parentId);
    
    // Render cards
    grid.innerHTML = visibleModules.map(module => {
        const isContainer = module.type === 'container';
        const sizeClass = module.size === 'large' ? 'large' : '';
        
        return `
            <div class="bento-card ${sizeClass}" 
                 data-module-id="${module.id}"
                 data-is-container="${isContainer}"
                 data-route="${module.route || ''}"
                 style="--card-theme: ${module.theme}">
                <div class="bento-card-content">
                    <div class="bento-card-icon">${module.icon}</div>
                    <div class="bento-card-title">${module.title}</div>
                    <div class="bento-card-subtitle">${module.subtitle || ''}</div>
                </div>
            </div>
        `;
    }).join('');
    
    // Add click handlers
    grid.querySelectorAll('.bento-card').forEach(card => {
        card.addEventListener('click', () => handleCardClick(card));
    });
}

/**
 * Handle card click
 */
function handleCardClick(card) {
    const moduleId = card.dataset.moduleId;
    const isContainer = card.dataset.isContainer === 'true';
    const route = card.dataset.route;
    
    if (isContainer) {
        // Navigate to container children
        currentParent = moduleId;
        navigationHistory.push(moduleId);
        renderGrid(moduleId);
    } else if (route) {
        // Navigate to module page
        window.location.href = route;
    }
}

/**
 * Update breadcrumb navigation
 */
function updateBreadcrumb(parentId) {
    const breadcrumb = document.getElementById('breadcrumb');
    if (!breadcrumb) return;
    
    if (!parentId) {
        breadcrumb.innerHTML = `
            <span class="breadcrumb-item active">Cimeika</span>
        `;
    } else {
        const parent = modules.find(m => m.id === parentId);
        breadcrumb.innerHTML = `
            <span class="breadcrumb-item" data-parent="">Cimeika</span>
            <span class="breadcrumb-item active">${parent?.title || parentId}</span>
        `;
        
        // Add click handler to go back
        breadcrumb.querySelector('[data-parent=""]').addEventListener('click', () => {
            currentParent = null;
            navigationHistory = [];
            renderGrid();
        });
    }
}

/**
 * Register service worker
 */
function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('[SW] Registered:', registration);
                
                // Check for updates
                registration.addEventListener('updatefound', () => {
                    const newWorker = registration.installing;
                    console.log('[SW] Update found');
                    
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            console.log('[SW] New version available');
                            // Could show update notification here
                        }
                    });
                });
            })
            .catch(error => {
                console.error('[SW] Registration failed:', error);
            });
    }
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Listen for online/offline events
    window.addEventListener('online', () => {
        updateSyncBadge(true);
    });
    
    window.addEventListener('offline', () => {
        updateSyncBadge(false);
    });
    
    // Initial sync badge state
    updateSyncBadge(navigator.onLine);
}

/**
 * Update sync badge
 */
function updateSyncBadge(isOnline) {
    const badge = document.getElementById('syncBadge');
    if (!badge) return;
    
    const dot = badge.querySelector('.sync-dot');
    const text = badge.querySelector('span:last-child');
    
    if (isOnline) {
        dot.style.background = '#4ade80';
        text.textContent = 'Синхронізовано';
    } else {
        dot.style.background = '#fbbf24';
        text.textContent = 'Офлайн';
    }
}

/**
 * Navigate programmatically
 */
function navigate(state, moduleId = null) {
    if (state === 'seed') {
        localStorage.removeItem('isGerminated');
        location.reload();
    } else if (state === 'core') {
        currentParent = null;
        renderGrid();
    } else if (state === 'module' && moduleId) {
        currentParent = moduleId;
        renderGrid(moduleId);
    }
}

// Start the app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Export for debugging
window.cimeika = {
    navigate,
    renderGrid,
    modules: () => modules,
    currentParent: () => currentParent
};
