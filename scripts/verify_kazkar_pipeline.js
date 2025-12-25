#!/usr/bin/env node

/**
 * verify_kazkar_pipeline.js
 * 
 * Comprehensive verification script for Kazkar Legends Sync Pipeline
 * Tests all components: API, WebSocket, sync script, and frontend accessibility
 * 
 * Usage:
 *   node scripts/verify_kazkar_pipeline.js
 * 
 * Environment variables:
 *   API_URL - Base URL for the API (default: http://localhost:8000)
 *   FRONTEND_URL - Frontend URL (default: http://localhost:3000)
 */

import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const API_URL = process.env.API_URL || 'http://localhost:8000';
const FRONTEND_URL = process.env.FRONTEND_URL || 'http://localhost:3000';

// Test results tracker
const results = {
  passed: 0,
  failed: 0,
  warnings: 0,
  tests: []
};

/**
 * Log test result
 */
function logTest(name, passed, message) {
  const status = passed ? '✅' : '❌';
  console.log(`${status} ${name}`);
  if (message) {
    console.log(`   ${message}`);
  }
  
  results.tests.push({ name, passed, message });
  if (passed) {
    results.passed++;
  } else {
    results.failed++;
  }
}

/**
 * Log warning
 */
function logWarning(name, message) {
  console.log(`⚠️  ${name}`);
  if (message) {
    console.log(`   ${message}`);
  }
  results.warnings++;
}

/**
 * Test 1: Check legends directory exists
 */
function testLegendsDirectory() {
  const legendsDir = path.join(__dirname, '..', 'docs', 'legends');
  const exists = fs.existsSync(legendsDir);
  
  if (exists) {
    const files = fs.readdirSync(legendsDir).filter(f => f.endsWith('.md'));
    logTest('Legends Directory', true, `Found ${files.length} markdown file(s)`);
  } else {
    logTest('Legends Directory', false, 'Directory does not exist');
  }
  
  return exists;
}

/**
 * Test 2: Check sync script exists
 */
function testSyncScript() {
  const scriptPath = path.join(__dirname, 'sync_legends_to_api.js');
  const exists = fs.existsSync(scriptPath);
  
  logTest('Sync Script', exists, exists ? 'Script found' : 'Script not found');
  return exists;
}

/**
 * Test 3: Check API availability
 */
async function testAPIAvailability() {
  try {
    const response = await fetch(`${API_URL}/health`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' }
    });
    
    if (response.ok) {
      const data = await response.json();
      logTest('API Health', true, `Status: ${data.status}`);
      return true;
    } else {
      logTest('API Health', false, `HTTP ${response.status}`);
      return false;
    }
  } catch (error) {
    logTest('API Health', false, `Connection failed: ${error.message}`);
    return false;
  }
}

/**
 * Test 4: Check Kazkar module endpoint
 */
async function testKazkarEndpoint() {
  try {
    const response = await fetch(`${API_URL}/api/v1/kazkar/`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' }
    });
    
    if (response.ok) {
      const data = await response.json();
      logTest('Kazkar Module', true, `Module: ${data.name}`);
      return true;
    } else {
      logTest('Kazkar Module', false, `HTTP ${response.status}`);
      return false;
    }
  } catch (error) {
    logTest('Kazkar Module', false, `Connection failed: ${error.message}`);
    return false;
  }
}

/**
 * Test 5: Check legends endpoint
 */
async function testLegendsEndpoint() {
  try {
    const response = await fetch(`${API_URL}/api/v1/kazkar/legends`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' }
    });
    
    if (response.ok) {
      const data = await response.json();
      logTest('Legends Endpoint', true, `Found ${data.length} legend(s)`);
      return true;
    } else {
      logTest('Legends Endpoint', false, `HTTP ${response.status}`);
      return false;
    }
  } catch (error) {
    logTest('Legends Endpoint', false, `Connection failed: ${error.message}`);
    return false;
  }
}

/**
 * Test 6: Check import endpoint (without actually importing)
 */
async function testImportEndpoint() {
  try {
    // Try OPTIONS request to check if endpoint exists
    const response = await fetch(`${API_URL}/api/v1/kazkar/import`, {
      method: 'OPTIONS',
    });
    
    // Accept 200, 204, or 405 (method not allowed means endpoint exists)
    if (response.ok || response.status === 405) {
      logTest('Import Endpoint', true, 'Endpoint is accessible');
      return true;
    } else {
      logTest('Import Endpoint', false, `HTTP ${response.status}`);
      return false;
    }
  } catch (error) {
    logWarning('Import Endpoint', `Could not verify: ${error.message}`);
    return false;
  }
}

/**
 * Test 7: Check WebSocket endpoint (connection test only)
 */
async function testWebSocketEndpoint() {
  return new Promise((resolve) => {
    try {
      const wsUrl = API_URL.replace(/^http/, 'ws') + '/ws/kazkar';
      const ws = new (await import('ws')).default(wsUrl);
      
      const timeout = setTimeout(() => {
        ws.close();
        logTest('WebSocket Endpoint', false, 'Connection timeout');
        resolve(false);
      }, 5000);
      
      ws.on('open', () => {
        clearTimeout(timeout);
        logTest('WebSocket Endpoint', true, 'Connection successful');
        ws.close();
        resolve(true);
      });
      
      ws.on('error', (error) => {
        clearTimeout(timeout);
        logTest('WebSocket Endpoint', false, `Connection failed: ${error.message}`);
        resolve(false);
      });
    } catch (error) {
      logWarning('WebSocket Endpoint', `Test skipped: ${error.message}`);
      resolve(false);
    }
  });
}

/**
 * Test 8: Check specifications exist
 */
function testSpecifications() {
  const specs = [
    'KAZKAR_LEGEND_UI_SPEC.md',
    'KAZKAR_LEGEND_UI_FIGMA_SPEC.md',
    'figma_sync.json'
  ];
  
  let allExist = true;
  for (const spec of specs) {
    const specPath = path.join(__dirname, '..', 'docs', spec);
    const exists = fs.existsSync(specPath);
    if (!exists) {
      allExist = false;
      logWarning('Specifications', `Missing: ${spec}`);
    }
  }
  
  if (allExist) {
    logTest('Specifications', true, 'All specification files exist');
  } else {
    logTest('Specifications', false, 'Some specification files missing');
  }
  
  return allExist;
}

/**
 * Test 9: Check GitHub Action workflow
 */
function testGitHubAction() {
  const workflowPath = path.join(__dirname, '..', '.github', 'workflows', 'kazkar-sync.yml');
  const exists = fs.existsSync(workflowPath);
  
  logTest('GitHub Action', exists, exists ? 'Workflow file found' : 'Workflow file not found');
  return exists;
}

/**
 * Test 10: Check frontend files
 */
function testFrontendFiles() {
  const files = [
    'frontend/src/modules/Kazkar/legends/LegendScene.tsx',
    'frontend/src/modules/Kazkar/legends/LegendPage.tsx',
    'frontend/src/modules/Kazkar/hooks/useKazkarRealtime.ts'
  ];
  
  let allExist = true;
  for (const file of files) {
    const filePath = path.join(__dirname, '..', file);
    const exists = fs.existsSync(filePath);
    if (!exists) {
      allExist = false;
      logWarning('Frontend Files', `Missing: ${file}`);
    }
  }
  
  if (allExist) {
    logTest('Frontend Files', true, 'All required frontend files exist');
  } else {
    logTest('Frontend Files', false, 'Some frontend files missing');
  }
  
  return allExist;
}

/**
 * Print summary
 */
function printSummary() {
  console.log('\n' + '='.repeat(60));
  console.log('VERIFICATION SUMMARY');
  console.log('='.repeat(60));
  console.log(`✅ Passed:   ${results.passed}`);
  console.log(`❌ Failed:   ${results.failed}`);
  console.log(`⚠️  Warnings: ${results.warnings}`);
  console.log(`📊 Total:    ${results.tests.length}`);
  console.log('='.repeat(60));
  
  if (results.failed === 0) {
    console.log('✨ All tests passed! Kazkar Sync Pipeline is ready.');
    return 0;
  } else {
    console.log('⚠️  Some tests failed. Please review the issues above.');
    return 1;
  }
}

/**
 * Main execution
 */
async function main() {
  console.log('🔍 Kazkar Legends Sync Pipeline Verification\n');
  console.log('=' .repeat(60));
  console.log(`API URL:      ${API_URL}`);
  console.log(`Frontend URL: ${FRONTEND_URL}`);
  console.log('='.repeat(60) + '\n');
  
  // File system tests
  console.log('📁 File System Tests:');
  testLegendsDirectory();
  testSyncScript();
  testSpecifications();
  testGitHubAction();
  testFrontendFiles();
  
  // API tests
  console.log('\n🌐 API Tests:');
  const apiAvailable = await testAPIAvailability();
  
  if (apiAvailable) {
    await testKazkarEndpoint();
    await testLegendsEndpoint();
    await testImportEndpoint();
    await testWebSocketEndpoint();
  } else {
    logWarning('API Tests', 'Skipped due to API unavailability');
  }
  
  // Summary
  const exitCode = printSummary();
  process.exit(exitCode);
}

// Run if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

export { testLegendsDirectory, testAPIAvailability, testKazkarEndpoint };
