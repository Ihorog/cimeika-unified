/**
 * SEO Service
 * Provides access to SEO metadata from the backend
 */

import { apiClient } from './api';

export interface SeoMeta {
  title: string;
  description: string;
}

export interface HreflangTag {
  lang: string;
  url: string;
}

export interface SeoValidation {
  value: string;
  length: number;
  max: number;
  valid: boolean;
}

export interface SeoData {
  meta: SeoMeta;
  canonical_url: string;
  hreflang: Record<string, string>;
  validation: {
    title: SeoValidation;
    description: SeoValidation;
  };
}

export interface SeoConfig {
  canonical_lang: string;
  hreflang_patterns: Record<string, string>;
  rules: {
    title_max: number;
    description_max: number;
  };
}

/**
 * SEO Matrix Service
 */
export const seoService = {
  /**
   * Get all available emotional states
   */
  async getStates(): Promise<string[]> {
    try {
      const response = await apiClient.get('/api/v1/seo/states');
      return response.data.states;
    } catch (error) {
      console.error('Failed to fetch SEO states:', error);
      return [];
    }
  },

  /**
   * Get all available intents for a specific state
   */
  async getIntents(state: string): Promise<string[]> {
    try {
      const response = await apiClient.get(`/api/v1/seo/intents/${state}`);
      return response.data.intents;
    } catch (error) {
      console.error(`Failed to fetch intents for state ${state}:`, error);
      return [];
    }
  },

  /**
   * Get complete SEO data for a state/intent combination
   */
  async getSeoData(state: string, intent: string): Promise<SeoData | null> {
    try {
      const response = await apiClient.get(`/api/v1/seo/meta/${state}/${intent}`);
      return response.data.data;
    } catch (error) {
      console.error(`Failed to fetch SEO data for ${state}/${intent}:`, error);
      return null;
    }
  },

  /**
   * Get SEO configuration
   */
  async getConfig(): Promise<SeoConfig | null> {
    try {
      const response = await apiClient.get('/api/v1/seo/config');
      return response.data.config;
    } catch (error) {
      console.error('Failed to fetch SEO config:', error);
      return null;
    }
  },

  /**
   * Update document metadata (title and meta tags)
   */
  updateDocumentMeta(seoData: SeoData, state: string, intent: string): void {
    // Update title
    document.title = seoData.meta.title;

    // Update or create meta description
    let metaDescription = document.querySelector('meta[name="description"]');
    if (!metaDescription) {
      metaDescription = document.createElement('meta');
      metaDescription.setAttribute('name', 'description');
      document.head.appendChild(metaDescription);
    }
    metaDescription.setAttribute('content', seoData.meta.description);

    // Update or create canonical link
    let canonical = document.querySelector('link[rel="canonical"]');
    if (!canonical) {
      canonical = document.createElement('link');
      canonical.setAttribute('rel', 'canonical');
      document.head.appendChild(canonical);
    }
    canonical.setAttribute('href', window.location.origin + seoData.canonical_url);

    // Remove existing hreflang tags
    document.querySelectorAll('link[rel="alternate"][hreflang]').forEach(tag => tag.remove());

    // Add new hreflang tags
    Object.entries(seoData.hreflang).forEach(([lang, url]) => {
      const hreflangLink = document.createElement('link');
      hreflangLink.setAttribute('rel', 'alternate');
      hreflangLink.setAttribute('hreflang', lang);
      hreflangLink.setAttribute('href', window.location.origin + url);
      document.head.appendChild(hreflangLink);
    });

    // Add Open Graph tags
    this.updateOpenGraphTags(seoData, state, intent);
  },

  /**
   * Update Open Graph meta tags for social sharing
   */
  updateOpenGraphTags(seoData: SeoData, state: string, intent: string): void {
    const ogTags = [
      { property: 'og:title', content: seoData.meta.title },
      { property: 'og:description', content: seoData.meta.description },
      { property: 'og:url', content: window.location.origin + seoData.canonical_url },
      { property: 'og:type', content: 'website' },
    ];

    ogTags.forEach(({ property, content }) => {
      let tag = document.querySelector(`meta[property="${property}"]`);
      if (!tag) {
        tag = document.createElement('meta');
        tag.setAttribute('property', property);
        document.head.appendChild(tag);
      }
      tag.setAttribute('content', content);
    });

    // Twitter Card tags
    const twitterTags = [
      { name: 'twitter:card', content: 'summary' },
      { name: 'twitter:title', content: seoData.meta.title },
      { name: 'twitter:description', content: seoData.meta.description },
    ];

    twitterTags.forEach(({ name, content }) => {
      let tag = document.querySelector(`meta[name="${name}"]`);
      if (!tag) {
        tag = document.createElement('meta');
        tag.setAttribute('name', name);
        document.head.appendChild(tag);
      }
      tag.setAttribute('content', content);
    });
  },

  /**
   * Clear all SEO meta tags
   */
  clearDocumentMeta(): void {
    // Reset title to default
    document.title = 'CIMEIKA — Сімейка';

    // Remove meta description
    document.querySelector('meta[name="description"]')?.remove();

    // Remove canonical
    document.querySelector('link[rel="canonical"]')?.remove();

    // Remove hreflang tags
    document.querySelectorAll('link[rel="alternate"][hreflang]').forEach(tag => tag.remove());

    // Remove Open Graph tags
    ['og:title', 'og:description', 'og:url', 'og:type'].forEach(property => {
      document.querySelector(`meta[property="${property}"]`)?.remove();
    });

    // Remove Twitter Card tags
    ['twitter:card', 'twitter:title', 'twitter:description'].forEach(name => {
      document.querySelector(`meta[name="${name}"]`)?.remove();
    });
  },

  /**
   * Apply SEO metadata for a specific state/intent
   */
  async applySeoMeta(state: string, intent: string): Promise<boolean> {
    const seoData = await this.getSeoData(state, intent);
    
    if (!seoData) {
      console.warn(`No SEO data found for ${state}/${intent}`);
      return false;
    }

    this.updateDocumentMeta(seoData, state, intent);
    return true;
  },
};

export default seoService;
