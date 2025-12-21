/**
 * seo_rules.mjs
 * Правила маппінгу scoring → status для SEO перевірок
 */

/**
 * Оцінює статус на основі anomaly score
 * @param {number} score - Anomaly score (0.0 - 1.0)
 * @returns {{status: string, notes: string}}
 */
export function evaluateAnomalyStatus(score) {
  if (score <= 0.6) {
    return {
      status: 'ok',
      notes: `Anomaly score ${score.toFixed(2)} — нормальний рівень`
    };
  } else if (score <= 0.8) {
    return {
      status: 'warn',
      notes: `Anomaly score ${score.toFixed(2)} — підвищена увага`
    };
  } else {
    return {
      status: 'fail',
      notes: `Anomaly score ${score.toFixed(2)} — критичний рівень аномалій`
    };
  }
}

/**
 * Оцінює статус на основі volatility score
 * @param {number} score - Volatility score (0.0 - 1.0)
 * @returns {{status: string, notes: string}}
 */
export function evaluateVolatilityStatus(score) {
  if (score <= 0.5) {
    return {
      status: 'ok',
      notes: `Volatility score ${score.toFixed(2)} — стабільні рейтинги`
    };
  } else if (score <= 0.7) {
    return {
      status: 'warn',
      notes: `Volatility score ${score.toFixed(2)} — помірна волатильність`
    };
  } else {
    return {
      status: 'fail',
      notes: `Volatility score ${score.toFixed(2)} — висока волатильність рейтингів`
    };
  }
}

/**
 * Оцінює статус дрейфу індексації
 * @param {number} driftPercent - Drift percent
 * @param {number} tolerancePercent - Tolerance threshold
 * @returns {{status: string, notes: string}}
 */
export function evaluateDriftStatus(driftPercent, tolerancePercent) {
  if (driftPercent <= tolerancePercent) {
    return {
      status: 'ok',
      notes: `Drift ${driftPercent.toFixed(2)}% в межах tolerance ${tolerancePercent}%`
    };
  } else if (driftPercent <= tolerancePercent * 1.5) {
    return {
      status: 'warn',
      notes: `Drift ${driftPercent.toFixed(2)}% перевищує tolerance ${tolerancePercent}%`
    };
  } else {
    return {
      status: 'fail',
      notes: `Drift ${driftPercent.toFixed(2)}% критично перевищує tolerance ${tolerancePercent}%`
    };
  }
}
