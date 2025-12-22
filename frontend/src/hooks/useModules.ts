/**
 * React hook for accessing module registry
 * Provides easy access to module status and metadata
 */

import { useState, useEffect, useCallback } from 'react';
import { registry } from '../core';
import type { ModuleStatus, ModuleMetadata } from '../types';

/**
 * Hook to get all module statuses
 */
export function useModulesStatus() {
  const [statuses, setStatuses] = useState<Record<string, ModuleStatus>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStatuses = useCallback(async () => {
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
  }, []);

  useEffect(() => {
    fetchStatuses();
  }, [fetchStatuses]);

  return { statuses, loading, error, refresh: fetchStatuses };
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

/**
 * Hook to get status of a specific module
 */
export function useModuleStatus(moduleName: string) {
  const [status, setStatus] = useState<ModuleStatus | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStatus = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const module = registry.get(moduleName);
      if (!module) {
        throw new Error(`Module '${moduleName}' not found`);
      }
      
      const moduleStatus = await module.getStatus();
      setStatus(moduleStatus);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }, [moduleName]);

  useEffect(() => {
    fetchStatus();
  }, [fetchStatus]);

  return { status, loading, error, refresh: fetchStatus };
}

/**
 * Hook to get module metadata
 */
export function useModuleMetadata(moduleName: string): ModuleMetadata | null {
  const [metadata, setMetadata] = useState<ModuleMetadata | null>(null);

  useEffect(() => {
    const module = registry.get(moduleName);
    if (module) {
      try {
        const meta = module.getMetadata();
        setMetadata(meta);
      } catch (err) {
        console.error(`Failed to get metadata for ${moduleName}:`, err);
      }
    }
  }, [moduleName]);

  return metadata;
}

/**
 * Hook to initialize a module
 */
export function useModuleInitialize(moduleName: string) {
  const [initializing, setInitializing] = useState<boolean>(false);
  const [initialized, setInitialized] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const initialize = useCallback(async () => {
    setInitializing(true);
    setError(null);
    
    try {
      const module = registry.get(moduleName);
      if (!module) {
        throw new Error(`Module '${moduleName}' not found`);
      }
      
      const result = await module.initialize();
      setInitialized(result);
      return result;
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Unknown error';
      setError(errorMsg);
      return false;
    } finally {
      setInitializing(false);
    }
  }, [moduleName]);

  return { initialize, initializing, initialized, error };
}

/**
 * Hook to check if a module is initialized
 */
export function useModuleInitialized(moduleName: string): boolean {
  const [initialized, setInitialized] = useState<boolean>(false);

  useEffect(() => {
    const module = registry.get(moduleName);
    if (module && 'isInitialized' in module) {
      setInitialized((module as any).isInitialized());
    }
  }, [moduleName]);

  return initialized;
}
