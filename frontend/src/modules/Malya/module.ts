/**
 * Malya module - Ideas, creativity, innovations
 * Implements ModuleInterface for integration with orchestrator
 */

import type { ModuleInterface, ModuleStatus, ModuleMetadata } from '../../../types';
import { malyaService } from './service';

/**
 * Malya Module class implementing ModuleInterface
 */
export class MalyaModule implements ModuleInterface {
  private initialized: boolean = false;
  private readonly name: string = 'malya';

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
      const result = await malyaService.getStatus();
      
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
      const result = await malyaService.getStatus();
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
      description: 'Ideas, creativity, innovations - captures and nurtures creative thoughts and concepts'
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
 * Singleton instance of Malya module
 */
export const malyaModule = new MalyaModule();
