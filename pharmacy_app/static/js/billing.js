/**
 * PHARMA Care & Inventory - Billing & Invoice Controller
 * Calculations, stored procedure generation, and print view formatting
 */

async function viewBillModal(billId) {
  try {
    const res = await fetch(`/api/bills/${billId}`);
    const data = await res.json();
    if (!data.success) {
      showToast('Could not load bill details.', 'error');
      return;
    }

    const bill = data.data;
    document.getElementById('modalBillId').textContent = bill.Bill_ID;
    document.getElementById('modalBillPharm').textContent = `${bill.Pharmacy_Name} (${bill.Pharmacy_City})`;
    document.getElementById('modalBillPatient').textContent = `${bill.Patient_First} ${bill.Patient_Last}`;
    document.getElementById('modalBillPatientAddr').textContent = `${bill.Patient_Street}, ${bill.Patient_City}`;
    
    if (bill.prescription) {
      document.getElementById('modalBillPresc').textContent = `#${bill.prescription.Prescription_ID} (${bill.prescription.Date})`;
      document.getElementById('modalBillDoctor').textContent = `Dr. ${bill.prescription.Doctor_First} ${bill.prescription.Doctor_Last}`;
    } else {
      document.getElementById('modalBillPresc').textContent = 'Direct Walk-in';
      document.getElementById('modalBillDoctor').textContent = 'N/A';
    }

    // Render items
    const itemsTbody = document.getElementById('modalBillItemsBody');
    if (bill.items && bill.items.length > 0) {
      itemsTbody.innerHTML = bill.items.map(i => `
        <tr>
          <td><strong>${i.Medicine_Name}</strong></td>
          <td>${i.Dosage} (${i.Duration})</td>
          <td class="text-end">${formatINR(i.Price)}</td>
          <td class="text-end fw-bold">${formatINR(i.Price)}</td>
        </tr>
      `).join('');
    } else {
      itemsTbody.innerHTML = `
        <tr>
          <td>Standard Dispensation & Formulation Care</td>
          <td>Prescription Medication Fee</td>
          <td class="text-end">${formatINR(bill.Amount)}</td>
          <td class="text-end fw-bold">${formatINR(bill.Amount)}</td>
        </tr>
      `;
    }

    const subtotal = bill.Amount;
    const tax = subtotal * 0.05; // 5% GST on medicines
    const total = subtotal + tax;

    document.getElementById('modalBillSubtotal').textContent = formatINR(subtotal);
    document.getElementById('modalBillTax').textContent = formatINR(tax);
    document.getElementById('modalBillTotal').textContent = formatINR(total);

    const billModal = new bootstrap.Modal(document.getElementById('viewBillModal'));
    billModal.show();
  } catch (err) {
    showToast('Network error while retrieving bill details.', 'error');
  }
}

async function submitGenerateBill(event) {
  event.preventDefault();
  const form = event.target;
  const formData = new FormData(form);
  const payload = Object.fromEntries(formData.entries());

  try {
    const res = await fetch('/api/bills/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await res.json();

    if (result.success) {
      showToast(`✓ ${result.message || 'Bill generated successfully!'}`, 'success');
      setTimeout(() => window.location.reload(), 1200);
    } else {
      showToast(result.message || 'Error generating bill.', 'error');
    }
  } catch (err) {
    showToast('Failed to invoke bill generation stored procedure.', 'error');
  }
}

function printCurrentInvoice() {
  window.print();
}
