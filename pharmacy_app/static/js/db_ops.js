/**
 * PHARMA Care & Inventory - Database Operations Controller
 * Dedicated for DA2 College Demonstration and Viva Examination
 * Runs predefined SQL queries, executes Stored Procedures, tests Functions,
 * and visually verifies Database Triggers in action.
 */

// 1. Run Predefined Academic SQL Queries
async function runPredefinedQuery(queryKey) {
  const resultCard = document.getElementById('queryResultCard');
  const sqlBox = document.getElementById('querySqlDisplay');
  const resultContainer = document.getElementById('queryResultContainer');
  const queryBadge = document.getElementById('queryCategoryBadge');
  const queryDesc = document.getElementById('queryDescriptionText');

  resultContainer.innerHTML = '<div class="text-center py-4"><i class="fas fa-spinner fa-spin fa-2x text-primary"></i><p class="mt-2 text-muted">Executing query against database...</p></div>';
  resultCard.style.display = 'block';
  resultCard.scrollIntoView({ behavior: 'smooth' });

  try {
    const res = await fetch('/api/db-ops/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query_key: queryKey })
    });
    const response = await res.json();

    if (!response.success) {
      resultContainer.innerHTML = `<div class="alert alert-danger"><i class="fas fa-exclamation-circle me-2"></i>Error: ${response.message || 'Execution error'}</div>`;
      return;
    }

    const data = response.data;
    sqlBox.textContent = data.info.sql.trim();
    queryBadge.textContent = data.info.category;
    queryDesc.textContent = data.info.description;

    if (!data.data || data.data.length === 0) {
      resultContainer.innerHTML = '<div class="alert alert-info">Query executed successfully. 0 rows returned.</div>';
      return;
    }

    // Build interactive HTML table
    let tableHtml = `
      <div class="table-responsive">
        <table class="saas-table">
          <thead>
            <tr>${data.columns.map(c => `<th>${c.replace(/_/g, ' ')}</th>`).join('')}</tr>
          </thead>
          <tbody>
            ${data.data.map(row => `
              <tr>${data.columns.map(c => `<td>${row[c] !== null ? row[c] : '<span class="text-muted">NULL</span>'}</td>`).join('')}</tr>
            `).join('')}
          </tbody>
        </table>
      </div>
      <div class="mt-2 text-muted text-end" style="font-size: 12px;">
        <i class="fas fa-database me-1"></i> Returned ${data.count} records cleanly.
      </div>
    `;

    resultContainer.innerHTML = tableHtml;
    showToast(`✓ Query '${data.info.name}' executed cleanly!`, 'success');
  } catch (err) {
    resultContainer.innerHTML = `<div class="alert alert-danger">Network failure while executing query.</div>`;
  }
}

// 2. Call Stored Procedures
async function submitProcedureCall(event, procName) {
  event.preventDefault();
  const form = event.target;
  const formData = new FormData(form);
  const args = Array.from(formData.values());

  const feedbackDiv = form.querySelector('.proc-feedback') || document.getElementById('procGlobalFeedback');

  try {
    const res = await fetch('/api/db-ops/procedure', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ proc_name: procName, args: args })
    });
    const result = await res.json();

    if (result.success) {
      showToast(`✓ ${result.message || 'Procedure executed successfully!'}`, 'success');
      if (feedbackDiv) {
        feedbackDiv.className = 'alert alert-success mt-3';
        feedbackDiv.innerHTML = `<i class="fas fa-check-circle me-2"></i>${result.message}`;
        feedbackDiv.style.display = 'block';
      }
    } else {
      showToast(result.message || 'Procedure returned exception.', 'error');
      if (feedbackDiv) {
        feedbackDiv.className = 'alert alert-danger mt-3';
        feedbackDiv.innerHTML = `<i class="fas fa-exclamation-triangle me-2"></i>${result.message || 'Database Exception Signal'}`;
        feedbackDiv.style.display = 'block';
      }
    }
  } catch (err) {
    showToast('Failed to invoke stored procedure.', 'error');
  }
}

// 3. Test Stored Functions
async function runFunctionDemo(funcName, inputId, secondaryInputId = null, outputId = 'funcOutput') {
  const inputEl = document.getElementById(inputId);
  const outputEl = document.getElementById(outputId);
  const argVal = inputEl ? inputEl.value : null;
  const secVal = secondaryInputId ? document.getElementById(secondaryInputId)?.value : null;

  if (!argVal) {
    showToast('Please select or provide an input argument.', 'warning');
    return;
  }

  try {
    const res = await fetch('/api/db-ops/function', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        func_name: funcName,
        arg: argVal,
        secondary_arg: secVal
      })
    });
    const data = await res.json();

    if (data.success) {
      outputEl.innerHTML = `
        <div class="card bg-light border-0 p-3 mt-2">
          <span class="text-muted small">${data.data.label}:</span>
          <h4 class="fw-bold text-primary mb-0 mt-1">${data.data.result}</h4>
        </div>
      `;
      showToast(`✓ Function ${funcName}() evaluated successfully!`, 'success');
    } else {
      outputEl.innerHTML = `<div class="alert alert-danger mt-2">${data.message}</div>`;
    }
  } catch (err) {
    showToast('Error executing stored function.', 'error');
  }
}

// 4. Live Trigger Demonstration
async function runTriggerLiveDemo() {
  const pharmacyId = document.getElementById('triggerPharmSelect').value;
  const medicineId = document.getElementById('triggerMedSelect').value;
  const delta = document.getElementById('triggerDeltaInput').value || 25;
  const displayContainer = document.getElementById('triggerDemoDisplay');

  displayContainer.innerHTML = '<div class="text-center py-4"><i class="fas fa-spinner fa-spin fa-2x text-primary"></i><p class="mt-2 text-muted">Executing trigger demonstration workflow...</p></div>';

  try {
    const res = await fetch('/api/db-ops/trigger-demo', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        pharmacy_id: pharmacyId,
        medicine_id: medicineId,
        delta: delta
      })
    });
    const data = await res.json();

    if (!data.success) {
      displayContainer.innerHTML = `<div class="alert alert-danger">${data.message || 'Trigger demo failed.'}</div>`;
      return;
    }

    const d = data.data;
    displayContainer.innerHTML = `
      <div class="row g-3">
        <div class="col-md-4">
          <div class="trigger-step-card border-start border-4 border-secondary">
            <span class="badge bg-light text-dark mb-2">Step 1: Before Mutation</span>
            <h5>Initial Stock</h5>
            <div class="display-6 fw-bold text-dark">${d.qty_before}</div>
            <p class="text-muted small mb-0">Units on record in INVENTORY</p>
          </div>
        </div>
        <div class="col-md-4">
          <div class="trigger-step-card border-start border-4 border-primary">
            <span class="badge bg-primary mb-2">Step 2: Applied Mutation</span>
            <h5>Delta Operation</h5>
            <div class="display-6 fw-bold text-primary">+${d.delta_applied}</div>
            <p class="text-muted small mb-0">Units added via restock_medicine()</p>
          </div>
        </div>
        <div class="col-md-4">
          <div class="trigger-step-card border-start border-4 border-success">
            <span class="badge bg-success mb-2">Step 3: After Trigger</span>
            <h5>New Stock on Hand</h5>
            <div class="display-6 fw-bold text-success">${d.qty_after}</div>
            <p class="text-muted small mb-0">Updated in INVENTORY table</p>
          </div>
        </div>
      </div>

      <div class="card mt-4 border-0 bg-light p-3">
        <div class="d-flex align-items-center justify-content-between mb-2">
          <h6 class="fw-bold mb-0 text-dark">
            <i class="fas fa-bolt text-warning me-2"></i>Trigger <code>trg_after_inventory_update</code> Audit Output:
          </h6>
          <span class="badge bg-success">Automated Record</span>
        </div>
        <div class="table-responsive">
          <table class="table table-sm bg-white rounded border mb-0">
            <thead>
              <tr class="table-light">
                <th>Log ID</th>
                <th>Pharmacy ID</th>
                <th>Medicine ID</th>
                <th>Quantity Change</th>
                <th>Change Type</th>
                <th>Change Timestamp</th>
                <th>Reference ID</th>
              </tr>
            </thead>
            <tbody>
              <tr class="fw-semibold text-primary">
                <td>#${d.audit_log.Log_ID}</td>
                <td>${d.audit_log.Pharmacy_ID}</td>
                <td>${d.audit_log.Medicine_ID}</td>
                <td><span class="badge bg-success">+${d.audit_log.Quantity_Change}</span></td>
                <td>${d.audit_log.Change_Type}</td>
                <td>${d.audit_log.Change_Date}</td>
                <td><code>${d.audit_log.Reference_ID}</code></td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="mt-2 text-muted small">
          <i class="fas fa-check-double text-success me-1"></i> Verified: No manual insert was made into STOCK_LOG. The database trigger automatically populated this row!
        </div>
      </div>
    `;

    showToast('✓ Trigger executed and audit trail verified!', 'success');
  } catch (err) {
    displayContainer.innerHTML = `<div class="alert alert-danger">Error during trigger execution test.</div>`;
  }
}
