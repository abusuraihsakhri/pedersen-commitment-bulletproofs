import test from 'node:test';
import assert from 'node:assert/strict';
import {evaluatePayload} from '../web/app.mjs';

const payload = {task_id: 'T', target_identifier: 'KEY', primary_metric: 25, secondary_metric: 12, status_descriptor: 'NOMINAL', is_critical_flag: false};

test('threshold boundary remains nominal', () => {
  const result = evaluatePayload(payload);
  assert.equal(result.overall_urgency, 'ROUTINE');
  assert.equal(result.total_alerts, 0);
});

test('all three rules and critical precedence', () => {
  const result = evaluatePayload({...payload, primary_metric: 25.001, secondary_metric: 12.001, status_descriptor: 'DISCORDANT', is_critical_flag: true});
  assert.equal(result.total_alerts, 3);
  assert.equal(result.critical_alerts_count, 1);
  assert.equal(result.overall_urgency, 'CRITICAL_STAT_PANIC');
});

test('secondary threshold without critical flag remains elevated', () => {
  const result = evaluatePayload({...payload, secondary_metric: 13});
  assert.equal(result.overall_urgency, 'ELEVATED_RISK');
});

test('reject nonfinite numeric values and missing identifiers', () => {
  assert.throws(() => evaluatePayload({...payload, primary_metric: 'NaN'}), /finite/);
  assert.throws(() => evaluatePayload({...payload, secondary_metric: 'Infinity'}), /finite/);
  assert.throws(() => evaluatePayload({...payload, task_id: ''}), /task_id/);
});
