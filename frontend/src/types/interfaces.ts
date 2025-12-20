/**
 * Core interfaces for Cimeika frontend modules
 * Defines the contract that all modules must implement
 */

/**
 * Base module interface that all Cimeika modules must implement
 */
export interface ModuleInterface {
  /**
   * Get the module name
   */
  getName(): string;
  
  /**
   * Get the current status of the module
   */
  getStatus(): Promise<ModuleStatus>;
  
  /**
   * Initialize the module
   */
  initialize(): Promise<boolean>;
  
  /**
   * Get module metadata
   */
  getMetadata(): ModuleMetadata;
}

/**
 * Module status interface
 */
export interface ModuleStatus {
  status: 'active' | 'inactive' | 'error';
  name: string;
  initialized: boolean;
  [key: string]: any;
}

/**
 * Module metadata interface
 */
export interface ModuleMetadata {
  name: string;
  version: string;
  description: string;
  [key: string]: any;
}

/**
 * Service interface for data layer operations
 */
export interface ServiceInterface {
  /**
   * Get status from the API
   */
  getStatus(): Promise<any>;
  
  /**
   * Process data
   */
  process?(data: any): Promise<any>;
  
  /**
   * Validate data
   */
  validate?(data: any): boolean;
}

/**
 * Store interface for state management
 */
export interface StoreInterface<T = any> {
  /**
   * Get the current state
   */
  getState(): T;
  
  /**
   * Subscribe to state changes
   */
  subscribe(listener: (state: T) => void): () => void;
}

/**
 * Common API response interface
 */
export interface ApiResponse<T = any> {
  status: 'success' | 'error';
  data?: T;
  error?: string;
  message?: string;
}

/**
 * Base entity interface implementing minimal contract
 * Required fields according to UI specification:
 * - id: unique identifier
 * - module: module name
 * - time: timestamp
 * - tags: list of tags
 * - source_trace: source tracking information
 * - canon_bundle_id: canonical bundle identifier
 */
export interface BaseEntity {
  id: number;
  module: string;
  time: string | Date;
  tags: string[];
  source_trace?: string;
  canon_bundle_id: string;
}

/**
 * Entity status interface
 * Minimal implementation without simulation of full audit system
 */
export interface EntityStatus {
  status: 'draft' | 'confirmed';
}

/**
 * Entity with status
 */
export interface EntityWithStatus extends BaseEntity {
  entity_status: EntityStatus;
}
