/**
 * CIMEIKA Module Core v3.1
 * Y.js CRDT engine with IndexedDB persistence and WebRTC sync
 */

import * as Y from 'https://esm.sh/yjs@13.6.8';
import { IndexeddbPersistence } from 'https://esm.sh/y-indexeddb@9.0.12';
import { WebrtcProvider } from 'https://esm.sh/y-webrtc@10.2.5';

/**
 * Base class for all CIMEIKA modules
 */
export class CimeikaModule {
    constructor(config) {
        this.id = config.id;
        this.name = config.name;
        
        // Initialize Y.Doc
        this.doc = new Y.Doc();
        
        // IndexedDB persistence (offline storage)
        this.providerDB = new IndexeddbPersistence(`cimeika-${this.id}`, this.doc);
        
        // WebRTC provider (P2P sync)
        this.providerSync = new WebrtcProvider(`cimeika-global-${this.id}`, this.doc, {
            signaling: ['wss://signaling.yjs.dev']
        });
        
        // Awareness API for presence
        this.awareness = this.providerSync.awareness;
        
        // Shared data structure
        this.sharedItems = this.doc.getArray('items');
        
        // Setup user identity
        this.setupUser();
        
        // Setup awareness
        this.setupAwareness();
        
        // Listen for changes
        this.sharedItems.observe(() => {
            if (this.onItemsChange) {
                this.onItemsChange(this.getItems());
            }
        });
        
        // Listen for presence changes
        this.awareness.on('change', () => {
            if (this.onPresenceChange) {
                this.onPresenceChange(this.getPresenceUsers());
            }
        });
    }
    
    /**
     * Setup user identity
     */
    setupUser() {
        // Get or create username
        this.username = this.getUserName();
        
        // Get or create device ID
        this.deviceId = this.getDeviceId();
        
        // Get or create user color
        this.userColor = this.getUserColor();
    }
    
    /**
     * Setup awareness with user info
     */
    setupAwareness() {
        this.awareness.setLocalStateField('user', {
            name: this.username,
            color: this.userColor,
            deviceId: this.deviceId
        });
    }
    
    /**
     * Get username from localStorage or prompt
     */
    getUserName() {
        let name = localStorage.getItem('cimeika-username');
        if (!name) {
            name = prompt('Введіть ваше ім\'я:') || 'Анонім';
            localStorage.setItem('cimeika-username', name);
        }
        return name;
    }
    
    /**
     * Get or generate device ID
     */
    getDeviceId() {
        let deviceId = localStorage.getItem('cimeika-device-id');
        if (!deviceId) {
            deviceId = 'device-' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('cimeika-device-id', deviceId);
        }
        return deviceId;
    }
    
    /**
     * Get or generate user color
     */
    getUserColor() {
        let color = localStorage.getItem('cimeika-user-color');
        if (!color) {
            const colors = [
                '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A',
                '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2'
            ];
            color = colors[Math.floor(Math.random() * colors.length)];
            localStorage.setItem('cimeika-user-color', color);
        }
        return color;
    }
    
    /**
     * Get all items as plain array
     */
    getItems() {
        return this.sharedItems.toArray();
    }
    
    /**
     * Add new item to CRDT
     */
    addItem(data) {
        const item = {
            ...data,
            id: Date.now(),
            createdAt: new Date().toISOString(),
            by: this.username,
            deviceId: this.deviceId
        };
        this.sharedItems.push([item]);
        return item;
    }
    
    /**
     * Update item at index (delete + insert transaction)
     */
    updateItem(index, data) {
        this.doc.transact(() => {
            this.sharedItems.delete(index, 1);
            this.sharedItems.insert(index, [data]);
        });
    }
    
    /**
     * Delete item at index
     */
    deleteItem(index) {
        this.sharedItems.delete(index, 1);
    }
    
    /**
     * Get presence users
     */
    getPresenceUsers() {
        const users = [];
        this.awareness.getStates().forEach((state, clientId) => {
            if (state.user && clientId !== this.awareness.clientID) {
                users.push(state.user);
            }
        });
        return users;
    }
    
    /**
     * Migrate data from localStorage to CRDT
     */
    migrateFromLocalStorage(key) {
        const oldData = localStorage.getItem(key);
        if (oldData && this.sharedItems.length === 0) {
            try {
                const items = JSON.parse(oldData);
                if (Array.isArray(items)) {
                    items.forEach(item => {
                        this.sharedItems.push([{
                            ...item,
                            migratedAt: new Date().toISOString()
                        }]);
                    });
                    console.log(`Migrated ${items.length} items from ${key}`);
                }
            } catch (e) {
                console.error('Migration failed:', e);
            }
        }
    }
    
    /**
     * Render presence avatars in dock
     */
    renderPresence(containerId = 'presence-dock') {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        const users = this.getPresenceUsers();
        const localUser = {
            name: this.username,
            color: this.userColor,
            deviceId: this.deviceId
        };
        
        // Include local user
        const allUsers = [localUser, ...users];
        
        container.innerHTML = allUsers.map(user => {
            const initials = user.name.substring(0, 2).toUpperCase();
            return `
                <div class="presence-avatar" style="background-color: ${user.color}" title="${user.name} (${user.deviceId})">
                    ${initials}
                </div>
            `;
        }).join('');
    }
    
    /**
     * Destroy module and cleanup
     */
    destroy() {
        this.providerSync.destroy();
        this.providerDB.destroy();
    }
}
