#!/usr/bin/env node
/**
 * seo_health_report.mjs
 * Генератор SEO health звітів для governance loop
 */

import { readFileSync, writeFileSync } from 'fs';
import { parse } from 'yaml';
import {
  getIndexationDriftPercent,
  getRankingVolatilityScore,
  getAnomalyScore
} from './seo_sources_stub.mjs';
import {
  evaluateAnomalyStatus,
  evaluateVolatilityStatus,
  evaluateDriftStatus
} from './seo_rules.mjs';

/**
 * Читає конфігурацію з YAML
 */
function loadConfig() {
  const configPath = '.governance/seo/cimeika_seo_matrix.yaml';
  try {
    const fileContent = readFileSync(configPath, 'utf8');
    return parse(fileContent);
  } catch (error) {
    console.error(`❌ Не вдалося прочитати конфіг ${configPath}:`, error.message);
    process.exit(1);
  }
}

/**
 * Генерує health report
 */
function generateHealthReport() {
  const config = loadConfig();
  const timestamp = new Date().toISOString();
  
  // Отримуємо дані з stub джерел
  const driftPercent = getIndexationDriftPercent();
  const volatilityScore = getRankingVolatilityScore();
  const anomalyScore = getAnomalyScore();
  
  // Отримуємо tolerance з конфігу
  const driftAutomation = config.seo_automation_layer?.automations?.find(
    a => a.name === 'indexation_drift_monitoring'
  );
  const tolerancePercent = driftAutomation?.tolerance_percent || 3;
  
  // Оцінюємо статуси
  const anomalyStatus = evaluateAnomalyStatus(anomalyScore);
  const volatilityStatus = evaluateVolatilityStatus(volatilityScore);
  const driftStatus = evaluateDriftStatus(driftPercent, tolerancePercent);
  
  // Визначаємо чи потрібен auto-ticket
  const autoTicketRequired = driftPercent > tolerancePercent;
  const autoTicketReason = autoTicketRequired
    ? `Indexation drift ${driftPercent.toFixed(2)}% перевищує tolerance ${tolerancePercent}%`
    : '';
  
  // Формуємо JSON звіт
  const report = {
    timestamp_iso: timestamp,
    matrix_version: config.matrix_version || 'unknown',
    system_reactivity: config.governance_status?.system_reactivity || 'unknown',
    operational_risk: config.governance_status?.operational_risk || 'unknown',
    checks: {
      anomaly_detection: {
        status: anomalyStatus.status,
        score: anomalyScore,
        notes: anomalyStatus.notes
      },
      ranking_volatility: {
        status: volatilityStatus.status,
        score: volatilityScore,
        notes: volatilityStatus.notes
      },
      indexation_drift: {
        status: driftStatus.status,
        drift_percent: driftPercent,
        tolerance_percent: tolerancePercent,
        notes: driftStatus.notes
      }
    },
    actions: {
      notifications: [],
      auto_ticket: {
        required: autoTicketRequired,
        reason: autoTicketReason
      }
    }
  };
  
  // Додаємо notifications якщо є проблеми
  if (anomalyStatus.status !== 'ok') {
    report.actions.notifications.push(`Anomaly detection: ${anomalyStatus.status}`);
  }
  if (volatilityStatus.status !== 'ok') {
    report.actions.notifications.push(`Ranking volatility: ${volatilityStatus.status}`);
  }
  if (driftStatus.status !== 'ok') {
    report.actions.notifications.push(`Indexation drift: ${driftStatus.status}`);
  }
  
  // Зберігаємо JSON
  writeFileSync('health_report.json', JSON.stringify(report, null, 2));
  console.log('✅ health_report.json створено');
  
  // Генеруємо Markdown
  const markdown = generateMarkdown(report);
  writeFileSync('health_report.md', markdown);
  console.log('✅ health_report.md створено');
  
  // Виводимо короткий саммарі
  console.log('\n📊 SEO Health Summary:');
  console.log(`   Anomaly: ${anomalyStatus.status.toUpperCase()}`);
  console.log(`   Volatility: ${volatilityStatus.status.toUpperCase()}`);
  console.log(`   Drift: ${driftStatus.status.toUpperCase()} (${driftPercent.toFixed(2)}%)`);
  console.log(`   Auto-ticket: ${autoTicketRequired ? '🎫 YES' : '✅ NO'}`);
  
  return report;
}

/**
 * Генерує Markdown звіт
 */
function generateMarkdown(report) {
  const { checks, actions } = report;
  
  const statusEmoji = (status) => {
    switch (status) {
      case 'ok': return '✅';
      case 'warn': return '⚠️';
      case 'fail': return '❌';
      default: return '❓';
    }
  };
  
  let md = `# SEO Health Report\n\n`;
  md += `**Timestamp:** ${report.timestamp_iso}\n`;
  md += `**Matrix Version:** ${report.matrix_version}\n`;
  md += `**System Reactivity:** ${report.system_reactivity}\n`;
  md += `**Operational Risk:** ${report.operational_risk}\n\n`;
  
  md += `## Health Checks\n\n`;
  
  md += `### ${statusEmoji(checks.anomaly_detection.status)} Anomaly Detection\n`;
  md += `- **Status:** ${checks.anomaly_detection.status}\n`;
  md += `- **Score:** ${checks.anomaly_detection.score.toFixed(2)}\n`;
  md += `- **Notes:** ${checks.anomaly_detection.notes}\n\n`;
  
  md += `### ${statusEmoji(checks.ranking_volatility.status)} Ranking Volatility\n`;
  md += `- **Status:** ${checks.ranking_volatility.status}\n`;
  md += `- **Score:** ${checks.ranking_volatility.score.toFixed(2)}\n`;
  md += `- **Notes:** ${checks.ranking_volatility.notes}\n\n`;
  
  md += `### ${statusEmoji(checks.indexation_drift.status)} Indexation Drift\n`;
  md += `- **Status:** ${checks.indexation_drift.status}\n`;
  md += `- **Drift:** ${checks.indexation_drift.drift_percent.toFixed(2)}%\n`;
  md += `- **Tolerance:** ${checks.indexation_drift.tolerance_percent}%\n`;
  md += `- **Notes:** ${checks.indexation_drift.notes}\n\n`;
  
  md += `## Actions\n\n`;
  
  if (actions.notifications.length > 0) {
    md += `### 📢 Notifications\n`;
    actions.notifications.forEach(notif => {
      md += `- ${notif}\n`;
    });
    md += `\n`;
  }
  
  md += `### 🎫 Auto-Ticket\n`;
  md += `- **Required:** ${actions.auto_ticket.required ? 'YES' : 'NO'}\n`;
  if (actions.auto_ticket.required) {
    md += `- **Reason:** ${actions.auto_ticket.reason}\n`;
  }
  
  return md;
}

// Запуск
try {
  generateHealthReport();
} catch (error) {
  console.error('❌ Помилка генерації звіту:', error);
  process.exit(1);
}
