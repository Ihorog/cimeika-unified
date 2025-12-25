/**
 * useKazkarRealtime.ts
 * React hook for real-time WebSocket updates from Kazkar module
 * 
 * Subscribes to legend_sense_activated and other Kazkar events
 */

import { useEffect, useRef, useState, useCallback } from 'react';

interface KazkarEvent {
  event: string;
  legend_id?: number;
  sense?: string;
  timestamp: number;
  data?: any;
}

interface UseKazkarRealtimeOptions {
  /**
   * Enable automatic reconnection on disconnect
   * @default true
   */
  autoReconnect?: boolean;
  
  /**
   * Reconnection delay in milliseconds
   * @default 3000
   */
  reconnectDelay?: number;
  
  /**
   * Maximum number of reconnection attempts
   * @default 5
   */
  maxReconnectAttempts?: number;
  
  /**
   * Enable debug logging
   * @default false
   */
  debug?: boolean;
}

interface UseKazkarRealtimeReturn {
  /**
   * Latest event received from the WebSocket
   */
  lastEvent: KazkarEvent | null;
  
  /**
   * Current connection status
   */
  status: 'connecting' | 'connected' | 'disconnected' | 'error';
  
  /**
   * Manually reconnect to WebSocket
   */
  reconnect: () => void;
  
  /**
   * Manually disconnect from WebSocket
   */
  disconnect: () => void;
  
  /**
   * Check if currently connected
   */
  isConnected: boolean;
}

/**
 * Hook to subscribe to real-time Kazkar events via WebSocket
 * 
 * @example
 * ```tsx
 * function LegendComponent() {
 *   const { lastEvent, status, isConnected } = useKazkarRealtime();
 *   
 *   useEffect(() => {
 *     if (lastEvent?.event === 'legend_sense_activated') {
 *       console.log('Sense activated:', lastEvent.sense);
 *     }
 *   }, [lastEvent]);
 *   
 *   return <div>Status: {status}</div>;
 * }
 * ```
 */
export function useKazkarRealtime(
  options: UseKazkarRealtimeOptions = {}
): UseKazkarRealtimeReturn {
  const {
    autoReconnect = true,
    reconnectDelay = 3000,
    maxReconnectAttempts = 5,
    debug = false,
  } = options;

  const [lastEvent, setLastEvent] = useState<KazkarEvent | null>(null);
  const [status, setStatus] = useState<'connecting' | 'connected' | 'disconnected' | 'error'>(
    'disconnected'
  );

  const wsRef = useRef<WebSocket | null>(null);
  const reconnectAttemptsRef = useRef(0);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const shouldConnectRef = useRef(true);

  const log = useCallback(
    (...args: any[]) => {
      if (debug) {
        console.log('[useKazkarRealtime]', ...args);
      }
    },
    [debug]
  );

  const connect = useCallback(() => {
    if (!shouldConnectRef.current) {
      log('Connection skipped (shouldConnect=false)');
      return;
    }

    // Get WebSocket URL from environment or construct from API URL
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const wsUrl = apiUrl.replace(/^http/, 'ws') + '/ws/kazkar';

    log('Connecting to', wsUrl);
    setStatus('connecting');

    try {
      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onopen = () => {
        log('Connected');
        setStatus('connected');
        reconnectAttemptsRef.current = 0;
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          log('Received event:', data);
          setLastEvent(data);
        } catch (error) {
          console.error('[useKazkarRealtime] Failed to parse event:', error);
        }
      };

      ws.onerror = (error) => {
        log('WebSocket error:', error);
        setStatus('error');
      };

      ws.onclose = () => {
        log('Disconnected');
        setStatus('disconnected');
        wsRef.current = null;

        // Auto-reconnect if enabled and under attempt limit
        if (
          autoReconnect &&
          shouldConnectRef.current &&
          reconnectAttemptsRef.current < maxReconnectAttempts
        ) {
          reconnectAttemptsRef.current += 1;
          log(
            `Scheduling reconnect attempt ${reconnectAttemptsRef.current}/${maxReconnectAttempts}`
          );

          reconnectTimeoutRef.current = setTimeout(() => {
            connect();
          }, reconnectDelay);
        }
      };
    } catch (error) {
      console.error('[useKazkarRealtime] Failed to create WebSocket:', error);
      setStatus('error');
    }
  }, [autoReconnect, reconnectDelay, maxReconnectAttempts, log]);

  const disconnect = useCallback(() => {
    log('Manual disconnect');
    shouldConnectRef.current = false;

    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }

    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }

    setStatus('disconnected');
  }, [log]);

  const reconnect = useCallback(() => {
    log('Manual reconnect');
    disconnect();
    shouldConnectRef.current = true;
    reconnectAttemptsRef.current = 0;
    connect();
  }, [connect, disconnect, log]);

  // Connect on mount
  useEffect(() => {
    connect();

    // Cleanup on unmount
    return () => {
      shouldConnectRef.current = false;
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [connect]);

  return {
    lastEvent,
    status,
    reconnect,
    disconnect,
    isConnected: status === 'connected',
  };
}

export default useKazkarRealtime;
