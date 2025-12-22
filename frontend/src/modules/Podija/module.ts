/**
 * Podija module - Events, future, scenarios
 * Implements ModuleInterface for integration with orchestrator
 */

import type { ModuleInterface, ModuleStatus, ModuleMetadata } from '../../../types';
import { podijaService } from '../service';

/**
 * Podija Module class implementing ModuleInterface
 */
export class PodijaModule implements ModuleInterface {
  private initialized: boolean = false;
  private readonly name: string = 'podija';

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
      const result = await podijaService.getStatus();
      
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
      const result = await podijaService.getStatus();
      this.initialized = result.status === 'success';
      return this.initialized;
    } catch (error) {
      console.error(`Failed to initialize ${this.name}:`, error);
      this.initialized = false;
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
      description: 'Events, future, scenarios - manages upcoming events and potential futures'
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
 * Singleton instance of Podija module
 */
export const podijaModule = new PodijaModule();
