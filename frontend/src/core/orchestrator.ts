/**
 * Core orchestrator for module coordination
 * Frontend equivalent of backend/app/core/orchestrator.py
 */

import type { ModuleInterface, ModuleStatus, ModuleMetadata } from '../types';

/**
 * Registry for all Cimeika frontend modules
 */
export class ModuleRegistry {
  private modules: Map<string, ModuleInterface> = new Map();

  /**
   * Register a module
   * @param name - Module name
   * @param module - Module instance implementing ModuleInterface
   * @throws TypeError if module doesn't implement ModuleInterface
   */
  register(name: string, module: ModuleInterface): void {
    if (!this.isValidModule(module)) {
      throw new TypeError(
        `Module ${name} must implement ModuleInterface`
      );
    }
    this.modules.set(name, module);
  }

  /**
   * Get a registered module
   * @param name - Module name
   * @returns Module instance or undefined if not found
   */
  get(name: string): ModuleInterface | undefined {
    return this.modules.get(name);
  }

  /**
   * List all registered modules
   * @returns Array of module names
   */
  listModules(): string[] {
    return Array.from(this.modules.keys());
  }

  /**
   * Get status of all registered modules
   * @returns Object mapping module names to their status
   */
  async getAllStatuses(): Promise<Record<string, ModuleStatus>> {
    const statuses: Record<string, ModuleStatus> = {};
    
    for (const [name, module] of this.modules.entries()) {
      try {
        statuses[name] = await module.getStatus();
      } catch (error) {
        statuses[name] = {
          status: 'error',
          name,
          initialized: false,
          error: error instanceof Error ? error.message : 'Unknown error'
        };
      }
    }
    
    return statuses;
  }

  /**
   * Initialize all registered modules
   * @returns Object mapping module names to initialization success
   */
  async initializeAll(): Promise<Record<string, boolean>> {
    const results: Record<string, boolean> = {};
    
    for (const [name, module] of this.modules.entries()) {
      try {
        results[name] = await module.initialize();
      } catch (error) {
        results[name] = false;
        console.error(`Failed to initialize ${name}:`, error);
      }
    }
    
    return results;
  }

  /**
   * Get metadata for all registered modules
   * @returns Object mapping module names to their metadata
   */
  getAllMetadata(): Record<string, ModuleMetadata> {
    const metadata: Record<string, ModuleMetadata> = {};
    
    for (const [name, module] of this.modules.entries()) {
      try {
        metadata[name] = module.getMetadata();
      } catch (error) {
        metadata[name] = {
          name,
          version: '0.1.0',
          description: `${name} module`,
          error: error instanceof Error ? error.message : 'Unknown error'
        };
      }
    }
    
    return metadata;
  }

  /**
   * Unregister a module
   * @param name - Module name
   * @returns True if module was unregistered, false if not found
   */
  unregister(name: string): boolean {
    return this.modules.delete(name);
  }

  /**
   * Clear all registered modules
   */
  clear(): void {
    this.modules.clear();
  }

  /**
   * Check if a module is registered
   * @param name - Module name
   * @returns True if module is registered
   */
  has(name: string): boolean {
    return this.modules.has(name);
  }

  /**
   * Get the number of registered modules
   * @returns Number of modules
   */
  size(): number {
    return this.modules.size;
  }

  /**
   * Validate that an object implements ModuleInterface
   * @param module - Object to validate
   * @returns True if object implements ModuleInterface
   */
  private isValidModule(module: any): module is ModuleInterface {
    return (
      module &&
      typeof module.getName === 'function' &&
      typeof module.getStatus === 'function' &&
      typeof module.initialize === 'function' &&
      typeof module.getMetadata === 'function'
    );
  }
}

/**
 * Global registry instance
 * Singleton pattern for module management
 */
export const registry = new ModuleRegistry();
