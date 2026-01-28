/**
 * CIMEIKA Service Worker v2.0.1
 * Offline-first PWA support with cache-first strategy
 */

const CACHE_VERSION = 'cimeika-v2.0.1';
const CACHE_ASSETS = [
  '/',
  '/index.html',
  '/style.css',
  '/app.js',
  '/modules.json',
  '/manifest.json',
  '/abilities/module-core.js',
  '/abilities/podiya.html',
  '/abilities/kazkar.html',
  '/abilities/nastriy.html',
  '/abilities/malya.html',
  '/abilities/calendar.html',
  '/abilities/gallery.html'
];

/**
 * Install event - cache assets
 */
self.addEventListener('install', (event) => {
  console.log('[SW] Installing service worker...', CACHE_VERSION);
  
  event.waitUntil(
    caches.open(CACHE_VERSION)
      .then((cache) => {
        console.log('[SW] Caching assets');
        return cache.addAll(CACHE_ASSETS);
      })
      .then(() => self.skipWaiting())
  );
});

/**
 * Activate event - clean old caches
 */
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating service worker...', CACHE_VERSION);
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== CACHE_VERSION) {
              console.log('[SW] Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => self.clients.claim())
  );
});

/**
 * Fetch event - cache-first with network fallback
 */
self.addEventListener('fetch', (event) => {
  // Skip cross-origin requests
  if (!event.request.url.startsWith(self.location.origin)) {
    return;
  }
  
  event.respondWith(
    caches.match(event.request)
      .then((cachedResponse) => {
        if (cachedResponse) {
          // Return cached version and update in background
          fetch(event.request)
            .then((response) => {
              if (response && response.status === 200) {
                caches.open(CACHE_VERSION)
                  .then((cache) => cache.put(event.request, response));
              }
            })
            .catch(() => {
              // Network failed, but we have cached version
            });
          
          return cachedResponse;
        }
        
        // Not in cache, fetch from network
        return fetch(event.request)
          .then((response) => {
            // Don't cache non-successful responses
            if (!response || response.status !== 200 || response.type === 'error') {
              return response;
            }
            
            // Clone response for caching
            const responseToCache = response.clone();
            
            caches.open(CACHE_VERSION)
              .then((cache) => {
                cache.put(event.request, responseToCache);
              });
            
            return response;
          })
          .catch(() => {
            // Network failed and not in cache - fallback to index
            if (event.request.mode === 'navigate') {
              return caches.match('/index.html');
            }
          });
      })
  );
});

/**
 * Message event - for manual cache updates
 */
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'CACHE_URLS') {
    event.waitUntil(
      caches.open(CACHE_VERSION)
        .then((cache) => cache.addAll(event.data.urls))
    );
  }
});
