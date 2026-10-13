/** Local demonstration of the three Python monitoring rules. Not a cryptographic proof. */
const anomalyTerms = ['DISCORDANT', 'ANOMALY', 'MUTANT', 'VIOLATION', 'FAIL', 'REJECT'];

export function evaluatePayload(payload) {
  const primary = Number(payload.primary_metric);
  const secondary = Number(payload.secondary_metric);
  if (String(payload.primary_metric).trim() === '' || String(payload.secondary_metric).trim() === '' ||
      !Number.isFinite(primary) || !Number.isFinite(secondary)) {
    throw new Error('Enter finite numeric values for both metrics.');
  }
  for (const field of ['task_id', 'target_identifier', 'status_descriptor']) {
    if (typeof payload[field] !== 'string' || !payload[field].trim() || payload[field].length > 128) {
      throw new Error(`${field} must contain 1–128 characters.`);
    }
  }
  const alerts = [];
  const add = (origin_worker, urgency, summary, technical_details) => {
    alerts.push({origin_worker, urgency, summary, technical_details});
  };
  if (primary > 25) {
    add('InvariantQCWorker', 'ELEVATED_RISK', 'Primary Metric Threshold Exceeded',
      `Primary metric ${primary} exceeds the demonstration threshold 25.`);
  }
  if (payload.is_critical_flag || secondary > 12) {
    add('SafetyEscalationWorker', payload.is_critical_flag ? 'CRITICAL_STAT_PANIC' : 'ELEVATED_RISK',
      'Safety Interlock Triggered', `Critical flag: ${Boolean(payload.is_critical_flag)}; secondary metric: ${secondary}.`);
  }
  if (anomalyTerms.some(term => payload.status_descriptor.toUpperCase().includes(term))) {
    add('ProtocolConformanceWorker', 'ELEVATED_RISK', 'Descriptor Anomaly Detected',
      `Descriptor '${payload.status_descriptor}' matched a demonstration anomaly term.`);
  }
  const critical_alerts_count = alerts.filter(a => a.urgency === 'CRITICAL_STAT_PANIC').length;
  const overall_urgency = critical_alerts_count ? 'CRITICAL_STAT_PANIC' : alerts.length ? 'ELEVATED_RISK' : 'ROUTINE';
  const integrity_status = critical_alerts_count ? 'RECALIBRATION_REQUIRED' : alerts.length ? 'DISCORDANT_ANOMALY' : 'VALIDATED_OPTIMAL';
  return {
    mode: 'local_rule_based_demo', task_id: payload.task_id,
    target_identifier: payload.target_identifier, overall_urgency,
    integrity_status, total_alerts: alerts.length, critical_alerts_count,
    alerts, disclaimer: 'No cryptographic commitment, Bulletproof, digital signature, or server-side audit was performed.'
  };
}

if (typeof document !== 'undefined') {
  let lastResult = null;
  let evaluations = 0;
  const form = document.getElementById('audit-form');
  const output = document.getElementById('outputConsole');
  const download = document.getElementById('download');
  form.addEventListener('submit', event => {
    event.preventDefault();
    try {
      const payload = {
        task_id: form.elements.namedItem('task_id').value.trim(),
        target_identifier: form.elements.namedItem('target_identifier').value.trim(),
        primary_metric: form.elements.namedItem('primary_metric').value,
        secondary_metric: form.elements.namedItem('secondary_metric').value,
        status_descriptor: form.elements.namedItem('status_descriptor').value.trim(),
        is_critical_flag: form.elements.namedItem('is_critical_flag').checked,
      };
      if (!form.checkValidity()) { form.reportValidity(); return; }
      lastResult = evaluatePayload(payload);
      evaluations += 1;
      output.textContent = JSON.stringify(lastResult, null, 2);
      document.getElementById('m-tasks').textContent = String(evaluations);
      document.getElementById('m-alerts').textContent = String(lastResult.total_alerts);
      document.getElementById('m-status').textContent = lastResult.overall_urgency;
      download.disabled = false;
    } catch (error) {
      lastResult = null;
      download.disabled = true;
      output.textContent = `Validation error: ${error.message}`;
    }
  });
  download.addEventListener('click', () => {
    if (!lastResult) return;
    const url = URL.createObjectURL(new Blob([JSON.stringify(lastResult, null, 2)], {type: 'application/json'}));
    const a = document.createElement('a');
    a.href = url;
    a.download = 'monitoring-result.json';
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
}
