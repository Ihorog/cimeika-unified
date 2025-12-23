/**
 * Ci module - Central orchestration core
 * Implements ModuleInterface for integration with orchestrator
 */

import type { ModuleInterface, ModuleStatus, ModuleMetadata } from '../../../types';
import { ciService } from './service';

/**
 * Ci Module class implementing ModuleInterface
 */
export class CiModule implements ModuleInterface {
  private initialized: boolean = false;
  private readonly name: string = 'ci';

  /**
   * Get the module name
   */
  getName(): string {
    return this.name;
  }

  /**
   * Get the current status of the module
   */
  async getStatus(): Promise<ModuleStatus> {
    try {
      const result = await ciService.getStatus();
      
      if (result.status === 'success' && result.data) {
        return {
          status: 'active',
          name: this.name,
          initialized: this.initialized,
          ...result.data
        };
      }
      
      return {
        status: 'error',
        name: this.name,
        initialized: this.initialized,
        error: result.error || 'Failed to get status'
      };
    } catch (error) {
      return {
        status: 'error',
        name: this.name,
        initialized: this.initialized,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * Initialize the module
   */
  async initialize(): Promise<boolean> {
    try {
      // Perform any initialization logic here
      // For now, just verify the service is accessible
      const result = await ciService.getStatus();
      this.initialized = result.status === 'success';
      return this.initialized;
    } catch (error) {
      console.error(`Failed to initialize ${this.name}:`, error);
      this.initialized = false;
      return false;
    }
  }

  /**
   * Shutdown the module gracefully
   */
  async shutdown(): Promise<boolean> {
    try {
      this.initialized = false;
      return true;
    } catch (error) {
      console.error(`Failed to shutdown ${this.name}:`, error);
      return false;
    }
  }

  /**
   * Get module metadata
   */
  getMetadata(): ModuleMetadata {
    return {
      name: this.name,
      version: '0.1.0',
      description: 'Central orchestration core - coordinates all modules and manages system-wide operations'
    };
  }

  /**
   * Check if module is initialized
   */
  isInitialized(): boolean {
    return this.initialized;
  }
}

/**
 * Singleton instance of Ci module
 */
export const ciModule = new CiModule();
