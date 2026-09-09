/**
 * PHARMA Care & Inventory - Main UI Controller
 * Toast notifications, modal utilities, and global AJAX helpers
 */

// Toast notification manager
function showToast(message, type = 'success') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `saas-toast ${type}`;
  
  let icon = 'fa-check-circle text-success';
  if (type === 'error') icon = 'fa-exclamation-circle text-danger';
  if (type === 'warning') icon = 'fa-exclamation-triangle text-warning';
  
  toast.innerHTML = `
    <i class="fas ${icon} fa-lg"></i>
    <div style="flex:1;">${message}</div>
    <button type="button" class="btn-close" style="font-size:10px;" onclick="this.parentElement.remove()"></button>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => toast.remove(), 400);
  }, 4500);
}

// Global quick search filter for table views
function setupTableSearch(inputId, tableId) {
  const input = document.getElementById(inputId);
  const table = document.getElementById(tableId);
  if (!input || !table) return;

  input.addEventListener('keyup', function () {
    const filter = this.value.toLowerCase();
    const rows = table.getElementsByTagName('tr');
    
    for (let i = 1; i < rows.length; i++) {
      const text = rows[i].textContent.toLowerCase();
      rows[i].style.display = text.includes(filter) ? '' : 'none';
    }
  });
}

// Format number as Indian Rupee string
function formatINR(val) {
  return '₹' + parseFloat(val || 0).toLocaleString('en-IN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
}

document.addEventListener('DOMContentLoaded', () => {
  console.log('[*] PHARMA Care & Inventory SaaS Frontend Loaded');
});
