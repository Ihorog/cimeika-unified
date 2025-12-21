/**
 * seo_sources_stub.mjs
 * Stub джерела SEO-сигналів для тестування
 * Дозволяє override через environment variables
 */

/**
 * Повертає відсоток дрейфу індексації (stub)
 * @returns {number} Drift percent (0-100)
 */
export function getIndexationDriftPercent() {
  if (process.env.SEO_STUB_DRIFT_PERCENT !== undefined) {
    const value = parseFloat(process.env.SEO_STUB_DRIFT_PERCENT);
    if (!isNaN(value)) {
      return value;
    }
  }
  // Default: стабільний стан (1.5%)
  return 1.5;
}

/**
 * Повертає оцінку волатильності рейтингів (stub)
 * @returns {number} Volatility score (0.0 - 1.0)
 */
export function getRankingVolatilityScore() {
  if (process.env.SEO_STUB_VOLATILITY_SCORE !== undefined) {
    const value = parseFloat(process.env.SEO_STUB_VOLATILITY_SCORE);
    if (!isNaN(value)) {
      return value;
    }
  }
  // Default: низька волатильність (0.3)
  return 0.3;
}

/**
 * Повертає оцінку аномалій (stub)
 * @returns {number} Anomaly score (0.0 - 1.0)
 */
export function getAnomalyScore() {
  if (process.env.SEO_STUB_ANOMALY_SCORE !== undefined) {
    const value = parseFloat(process.env.SEO_STUB_ANOMALY_SCORE);
    if (!isNaN(value)) {
      return value;
    }
  }
  // Default: нормальний стан (0.2)
  return 0.2;
}
