#!/usr/bin/env node

/**
 * sync_legends_to_api.js
 * 
 * Synchronizes legend markdown files from /docs/legends/ to the Cimeika API
 * 
 * Usage:
 *   node scripts/sync_legends_to_api.js
 * 
 * Environment variables:
 *   API_URL - Base URL for the API (default: http://localhost:8000)
 *   DRY_RUN - If set to 'true', only shows what would be synced without sending
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const LEGENDS_DIR = path.join(__dirname, '..', 'docs', 'legends');
const API_URL = process.env.API_URL || 'http://localhost:8000';
const API_ENDPOINT = `${API_URL}/api/v1/kazkar/import`;
const DRY_RUN = process.env.DRY_RUN === 'true';

/**
 * Parse markdown legend file and extract metadata
 * @param {string} content - Raw markdown content
 * @returns {object} Parsed legend data
 */
function parseLegendMarkdown(content) {
  const lines = content.split('\n');
  const legend = {
    title: '',
    content: '',
    story_type: 'legend',
    participants: [],
    location: '',
    tags: []
  };

  let currentSection = 'metadata';
  let contentLines = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();

    // Extract title (first # heading)
    if (line.startsWith('# ') && !legend.title) {
      legend.title = line.substring(2).trim();
      continue;
    }

    // Parse metadata
    if (line.startsWith('**Тип**:') || line.startsWith('**Тип:**')) {
      legend.story_type = line.split(':')[1].trim();
      continue;
    }

    if (line.startsWith('**Учасники**:') || line.startsWith('**Учасники:**')) {
      const participantsStr = line.split(':')[1].trim();
      legend.participants = participantsStr.split(',').map(p => p.trim());
      continue;
    }

    if (line.startsWith('**Локація**:') || line.startsWith('**Локація:**')) {
      legend.location = line.split(':')[1].trim();
      continue;
    }

    if (line.startsWith('**Теги**:') || line.startsWith('**Теги:**')) {
      const tagsStr = line.split(':')[1].trim();
      legend.tags = tagsStr.split(',').map(t => t.trim());
      continue;
    }

    // Section headers
    if (line === '## Зміст') {
      currentSection = 'content';
      continue;
    }

    if (line === '## Відчуття' || line === '---') {
      if (currentSection === 'content') {
        currentSection = 'senses';
      }
      continue;
    }

    // Collect content
    if (currentSection === 'content' && line) {
      contentLines.push(lines[i]); // Use original line with formatting
    }
  }

  // Join content preserving formatting
  legend.content = contentLines.join('\n').trim();

  return legend;
}

/**
 * Read all legend files from the legends directory
 * @returns {Array<object>} Array of parsed legends
 */
function readLegendFiles() {
  if (!fs.existsSync(LEGENDS_DIR)) {
    console.error(`❌ Legends directory not found: ${LEGENDS_DIR}`);
    process.exit(1);
  }

  const files = fs.readdirSync(LEGENDS_DIR)
    .filter(file => file.endsWith('.md'))
    .sort();

  console.log(`📚 Found ${files.length} legend file(s)`);

  const legends = [];
  for (const file of files) {
    const filePath = path.join(LEGENDS_DIR, file);
    const content = fs.readFileSync(filePath, 'utf-8');
    const legend = parseLegendMarkdown(content);
    legend.source_trace = `docs/legends/${file}`;
    legends.push(legend);
    console.log(`  ✓ Parsed: ${legend.title || file}`);
  }

  return legends;
}

/**
 * Send legends to the API
 * @param {Array<object>} legends - Array of legend objects
 */
async function syncLegendsToAPI(legends) {
  if (legends.length === 0) {
    console.log('⚠️  No legends to sync');
    return;
  }

  console.log(`\n🚀 Syncing ${legends.length} legend(s) to API...`);
  console.log(`   API Endpoint: ${API_ENDPOINT}`);

  if (DRY_RUN) {
    console.log('\n🔍 DRY RUN MODE - Not sending to API\n');
    legends.forEach((legend, index) => {
      console.log(`${index + 1}. ${legend.title}`);
      console.log(`   Type: ${legend.story_type}`);
      console.log(`   Participants: ${legend.participants.join(', ')}`);
      console.log(`   Location: ${legend.location}`);
      console.log(`   Tags: ${legend.tags.join(', ')}`);
      console.log(`   Content length: ${legend.content.length} chars`);
      console.log('');
    });
    return;
  }

  let successCount = 0;
  let errorCount = 0;

  for (const legend of legends) {
    try {
      const response = await fetch(API_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(legend)
      });

      if (response.ok) {
        const result = await response.json();
        console.log(`  ✅ ${legend.title} (ID: ${result.id || 'N/A'})`);
        successCount++;
      } else {
        const errorText = await response.text();
        console.error(`  ❌ ${legend.title}: ${response.status} - ${errorText}`);
        errorCount++;
      }
    } catch (error) {
      console.error(`  ❌ ${legend.title}: ${error.message}`);
      errorCount++;
    }
  }

  console.log(`\n📊 Sync Summary:`);
  console.log(`   Success: ${successCount}`);
  console.log(`   Errors: ${errorCount}`);
  console.log(`   Total: ${legends.length}`);

  if (errorCount > 0) {
    process.exit(1);
  }
}

/**
 * Main execution
 */
async function main() {
  console.log('🔄 Kazkar Legends Sync\n');
  console.log('=' .repeat(50));

  try {
    const legends = readLegendFiles();
    await syncLegendsToAPI(legends);
    console.log('\n✨ Sync completed successfully!');
  } catch (error) {
    console.error('\n❌ Sync failed:', error.message);
    process.exit(1);
  }
}

// Run if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

export { parseLegendMarkdown, readLegendFiles, syncLegendsToAPI };
