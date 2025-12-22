/**
 * Module initialization and registration
 * Central setup for all Cimeika modules
 */

import { registry } from '../core';
import { ciModule } from '../modules/Ci';
import { kazkarModule } from '../modules/Kazkar';
import { podijaModule } from '../modules/Podija';
import { nastrijModule } from '../modules/Nastrij';
import { malyaModule } from '../modules/Malya';
import { galleryModule } from '../modules/Gallery';
import { calendarModule } from '../modules/Calendar';

/**
 * Register all modules with the orchestrator
 */
export function registerModules(): void {
  // Register all 7 core modules
  registry.register('ci', ciModule);
  registry.register('kazkar', kazkarModule);
  registry.register('podija', podijaModule);
  registry.register('nastrij', nastrijModule);
  registry.register('malya', malyaModule);
  registry.register('gallery', galleryModule);
  registry.register('calendar', calendarModule);
}

/**
 * Initialize all registered modules
 * @returns Promise with initialization results
 */
export async function initializeModules(): Promise<Record<string, boolean>> {
  return registry.initializeAll();
}

/**
 * Get status of all modules
 * @returns Promise with all module statuses
 */
export async function getModulesStatus() {
  return registry.getAllStatuses();
}

/**
 * Get metadata for all modules
 * @returns Object with all module metadata
 */
export function getModulesMetadata() {
  return registry.getAllMetadata();
}

/**
 * Setup and initialize all modules
 * Call this on app startup
 */
export async function setupModules() {
  registerModules();
  const results = await initializeModules();
  
  console.log('Module initialization results:', results);
  
  const failedModules = Object.entries(results)
    .filter(([_, success]) => !success)
    .map(([name, _]) => name);
  
  if (failedModules.length > 0) {
    console.warn('Failed to initialize modules:', failedModules);
  }
  
  return results;
}

// Export registry for direct access if needed
export { registry };
