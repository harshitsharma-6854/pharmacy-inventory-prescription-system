/**
 * PHARMA Care & Inventory - Prescription Wizard & Workflow Controller
 * Step-by-step clinical prescription builder with live prescription summary
 */

let prescriptionMedicines = [];

function addMedicineRow() {
  const medSelect = document.getElementById('itemMedicineSelect');
  const dosageInput = document.getElementById('itemDosageInput');
  const freqSelect = document.getElementById('itemFreqSelect');
  const durationInput = document.getElementById('itemDurationInput');

  const medId = medSelect.value;
  const medName = medSelect.options[medSelect.selectedIndex].text;
  const medPrice = parseFloat(medSelect.options[medSelect.selectedIndex].dataset.price || 0);
  const dosage = dosageInput.value.trim() || '500mg';
  const freq = freqSelect.value;
  const duration = durationInput.value.trim() || '5 Days';

  if (!medId) {
    showToast('Please select a medicine formulation.', 'warning');
    return;
  }

  prescriptionMedicines.push({
    medicine_id: medId,
    medicine_name: medName,
    price: medPrice,
    dosage: dosage,
    frequency: freq,
    duration: duration
  });

  renderMedicineRows();
  updateLiveSummary();

  // Reset inputs
  dosageInput.value = '500mg';
  durationInput.value = '5 Days';
}

function removeMedicineRow(index) {
  prescriptionMedicines.splice(index, 1);
  renderMedicineRows();
  updateLiveSummary();
}

function renderMedicineRows() {
  const tbody = document.getElementById('prescItemsTableBody');
  if (!tbody) return;

  if (prescriptionMedicines.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="5" class="text-center text-muted py-4">
          <i class="fas fa-pills mb-2 fa-2x d-block text-secondary opacity-50"></i>
          No medicines added yet. Use the selector above to add therapeutics.
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = prescriptionMedicines.map((m, idx) => `
    <tr>
      <td class="fw-semibold">${m.medicine_name}</td>
      <td><span class="badge bg-light text-dark">${m.dosage}</span></td>
      <td>${m.frequency}</td>
      <td>${m.duration}</td>
      <td class="text-end">
        <button type="button" class="btn btn-sm btn-outline-danger" onclick="removeMedicineRow(${idx})">
          <i class="fas fa-trash-alt"></i>
        </button>
      </td>
    </tr>
  `).join('');
}

function updateLiveSummary() {
  const patientSelect = document.getElementById('prescPatientSelect');
  const doctorSelect = document.getElementById('prescDoctorSelect');
  const dateInput = document.getElementById('prescDateInput');

  const summaryPatient = document.getElementById('summaryPatient');
  const summaryDoctor = document.getElementById('summaryDoctor');
  const summaryDate = document.getElementById('summaryDate');
  const summaryMeds = document.getElementById('summaryMedsList');
  const summaryTotal = document.getElementById('summaryEstTotal');

  if (summaryPatient && patientSelect) {
    summaryPatient.textContent = patientSelect.options[patientSelect.selectedIndex]?.text || 'Select Patient';
  }
  if (summaryDoctor && doctorSelect) {
    summaryDoctor.textContent = doctorSelect.options[doctorSelect.selectedIndex]?.text || 'Select Doctor';
  }
  if (summaryDate && dateInput) {
    summaryDate.textContent = dateInput.value || 'Today';
  }

  if (summaryMeds) {
    if (prescriptionMedicines.length === 0) {
      summaryMeds.innerHTML = '<li class="text-muted">No medicines added</li>';
    } else {
      summaryMeds.innerHTML = prescriptionMedicines.map(m => `
        <li class="d-flex justify-content-between py-1 border-bottom border-light">
          <span><strong>${m.medicine_name.split('(')[0]}</strong> (${m.dosage}, ${m.frequency})</span>
          <span class="text-muted">${m.duration}</span>
        </li>
      `).join('');
    }
  }

  if (summaryTotal) {
    const total = prescriptionMedicines.reduce((acc, m) => acc + m.price, 0);
    summaryTotal.textContent = formatINR(total);
  }
}

async function submitPrescriptionForm(event) {
  event.preventDefault();

  const patientId = document.getElementById('prescPatientSelect').value;
  const doctorId = document.getElementById('prescDoctorSelect').value;
  const prescDate = document.getElementById('prescDateInput').value;

  if (!patientId || !doctorId) {
    showToast('Patient and Doctor selections are required.', 'warning');
    return;
  }

  if (prescriptionMedicines.length === 0) {
    showToast('Please add at least one medicine to the prescription.', 'warning');
    return;
  }

  const payload = {
    patient_id: patientId,
    doctor_id: doctorId,
    date: prescDate,
    items: prescriptionMedicines
  };

  try {
    const res = await fetch('/api/prescriptions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await res.json();

    if (result.success) {
      showToast(`✓ ${result.message || 'Prescription registered successfully!'}`, 'success');
      setTimeout(() => window.location.reload(), 1200);
    } else {
      showToast(result.message || 'Failed to register prescription.', 'error');
    }
  } catch (err) {
    showToast('Network error while saving prescription.', 'error');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const patientSelect = document.getElementById('prescPatientSelect');
  const doctorSelect = document.getElementById('prescDoctorSelect');
  const dateInput = document.getElementById('prescDateInput');

  if (patientSelect) patientSelect.addEventListener('change', updateLiveSummary);
  if (doctorSelect) doctorSelect.addEventListener('change', updateLiveSummary);
  if (dateInput) dateInput.addEventListener('change', updateLiveSummary);

  updateLiveSummary();
});
