/**
 * useSeo Hook
 * React hook for managing SEO metadata in components
 */

import { useEffect, useState } from 'react';
import { seoService, SeoData } from '../services/seo';

interface UseSeoOptions {
  state: string;
  intent: string;
  autoApply?: boolean;
}

interface UseSeoReturn {
  seoData: SeoData | null;
  loading: boolean;
  error: string | null;
  applySeo: () => Promise<void>;
  clearSeo: () => void;
}

/**
 * Hook to manage SEO metadata for a specific state/intent combination
 * 
 * @param options - Configuration options
 * @param options.state - Emotional state (e.g., 'fatigue', 'anxiety')
 * @param options.intent - User intent (e.g., 'understand', 'capture')
 * @param options.autoApply - Whether to automatically apply SEO metadata on mount (default: true)
 * 
 * @returns Object containing SEO data, loading state, and control functions
 * 
 * @example
 * ```tsx
 * function MyComponent() {
 *   const { seoData, loading } = useSeo({
 *     state: 'fatigue',
 *     intent: 'understand'
 *   });
 *   
 *   if (loading) return <div>Loading...</div>;
 *   
 *   return <div>{seoData?.meta.title}</div>;
 * }
 * ```
 */
export function useSeo({ state, intent, autoApply = true }: UseSeoOptions): UseSeoReturn {
  const [seoData, setSeoData] = useState<SeoData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const applySeo = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const data = await seoService.getSeoData(state, intent);
      
      if (!data) {
        setError(`No SEO data found for ${state}/${intent}`);
        return;
      }
      
      setSeoData(data);
      seoService.updateDocumentMeta(data, state, intent);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load SEO data';
      setError(errorMessage);
      console.error('SEO loading error:', err);
    } finally {
      setLoading(false);
    }
  };

  const clearSeo = () => {
    seoService.clearDocumentMeta();
    setSeoData(null);
  };

  useEffect(() => {
    if (autoApply) {
      applySeo();
    }

    // Cleanup: restore default meta tags when component unmounts
    return () => {
      if (autoApply) {
        clearSeo();
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [state, intent]);

  return {
    seoData,
    loading,
    error,
    applySeo,
    clearSeo,
  };
}

export default useSeo;
