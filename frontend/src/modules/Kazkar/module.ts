/**
 * Kazkar module - Memory, stories, legends
 * Implements ModuleInterface for integration with orchestrator
 */

import type { ModuleInterface, ModuleStatus, ModuleMetadata } from '../../../types';
import { kazkarService } from './service';

/**
 * Kazkar Module class implementing ModuleInterface
 */
export class KazkarModule implements ModuleInterface {
  private initialized: boolean = false;
  private readonly name: string = 'kazkar';

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
      const result = await kazkarService.getStatus();
      
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
      const result = await kazkarService.getStatus();
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
      description: 'Memory, stories, legends - preserves and organizes personal and family narratives'
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
 * Singleton instance of Kazkar module
 */
export const kazkarModule = new KazkarModule();
