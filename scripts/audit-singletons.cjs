#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const ROOT = process.cwd();
const TARGET_EXTENSIONS = new Set(['.ts', '.tsx', '.js', '.jsx']);
const IGNORE_DIRS = new Set(['node_modules', '.git', 'dist', 'build', '.next', 'coverage']);

function walk(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (IGNORE_DIRS.has(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(full, out);
    } else if (TARGET_EXTENSIONS.has(path.extname(entry.name))) {
      out.push(full);
    }
  }
  return out;
}

function read(file) {
  return fs.readFileSync(file, 'utf8');
}

const files = walk(ROOT);

const ciMountCandidates = [];
const overlayRootCandidates = [];
const singletonMarkers = [];

for (const file of files) {
  const text = read(file);

  // Check for CI mount/controller patterns
  if (/CiController|CiProvider|CiMount/i.test(text)) {
    ciMountCandidates.push(file);
  }

  // Check for overlay root patterns
  if (/OverlayRoot|createOverlayRoot|ReactDOM\.createRoot.*overlay/i.test(text)) {
    overlayRootCandidates.push(file);
  }

  // Check for explicit singleton patterns
  const singletonPatterns = [
    /class\s+\w+\s*{[^}]*static\s+instance\s*[:=]/,
    /export\s+const\s+\w+\s*=\s*new\s+\w+\(\)/,
    /let\s+instance\s*[:=]\s*null.*getInstance/s,
    /private\s+static\s+instance\s*:/,
    /static\s+getInstance\s*\(/,
  ];

  for (const pattern of singletonPatterns) {
    if (pattern.test(text)) {
      singletonMarkers.push(file);
      break;
    }
  }
}

let hasViolations = false;

if (ciMountCandidates.length > 1) {
  console.error('VIOLATION: Multiple CI mount/controller candidates found:');
  ciMountCandidates.forEach(f => console.error(`  - ${path.relative(ROOT, f)}`));
  hasViolations = true;
}

if (overlayRootCandidates.length > 1) {
  console.error('VIOLATION: Multiple overlay root candidates found:');
  overlayRootCandidates.forEach(f => console.error(`  - ${path.relative(ROOT, f)}`));
  hasViolations = true;
}

if (singletonMarkers.length > 0) {
  console.warn('WARNING: Singleton pattern markers detected:');
  singletonMarkers.forEach(f => console.warn(`  - ${path.relative(ROOT, f)}`));
  // Note: warnings don't fail the build by default, but we report them
}

if (hasViolations) {
  console.error('\nSingleton audit failed: multiple instances of critical singletons detected.');
  process.exit(1);
}

console.log('Singleton audit passed.');
