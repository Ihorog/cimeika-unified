/**
 * React hook for accessing module registry
 * Provides easy access to module status and metadata
 */

import { useState, useEffect } from 'react';
import { registry } from '../core';
import type { ModuleStatus, ModuleMetadata } from '../types';

/**
 * Hook to get all module statuses
 */
export function useModulesStatus() {
  const [statuses, setStatuses] = useState<Record<string, ModuleStatus>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchStatuses() {
      try {
        setLoading(true);
        const result = await registry.getAllStatuses();
        setStatuses(result);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch statuses');
      } finally {
        setLoading(false);
      }
    }

    fetchStatuses();
  }, []);

  return { statuses, loading, error };
}

/**
 * Hook to get all module metadata
 */
export function useModulesMetadata() {
  const [metadata, setMetadata] = useState<Record<string, ModuleMetadata>>({});

  useEffect(() => {
    const result = registry.getAllMetadata();
    setMetadata(result);
  }, []);

  return metadata;
}

/**
 * Hook to get a specific module
 */
export function useModule(name: string) {
  const [module, setModule] = useState(() => registry.get(name));

  useEffect(() => {
    const mod = registry.get(name);
    setModule(mod);
  }, [name]);

  return module;
}

/**
 * Hook to get list of all registered modules
 */
export function useModulesList() {
  const [modules, setModules] = useState<string[]>([]);

  useEffect(() => {
    const list = registry.listModules();
    setModules(list);
  }, []);

  return modules;
}
