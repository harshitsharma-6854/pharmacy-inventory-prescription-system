/**
 * PHARMA Care & Inventory - Dashboard Charts Controller
 * 6 Dynamic Chart.js charts driven by live MySQL / database metrics
 */

document.addEventListener('DOMContentLoaded', async () => {
  try {
    const res = await fetch('/api/dashboard/charts');
    const charts = await res.json();

    // Chart.js global defaults
    Chart.defaults.font.family = "'Inter', -apple-system, sans-serif";
    Chart.defaults.color = '#64748b';

    // 1. Revenue Overview Chart (Bar)
    const ctxRevenue = document.getElementById('chartRevenue');
    if (ctxRevenue && charts.revenue) {
      new Chart(ctxRevenue, {
        type: 'bar',
        data: {
          labels: charts.revenue.labels,
          datasets: [{
            label: 'Revenue (INR)',
            data: charts.revenue.values,
            backgroundColor: 'rgba(13, 148, 136, 0.85)',
            borderColor: '#0d9488',
            borderWidth: 1,
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: (ctx) => ` Gross Revenue: ₹${ctx.raw.toLocaleString('en-IN')}`
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: (val) => '₹' + val
              },
              grid: { color: '#f1f5f9' }
            },
            x: { grid: { display: false } }
          }
        }
      });
    }

    // 2. Prescription Trends Chart (Line)
    const ctxPresc = document.getElementById('chartPrescriptions');
    if (ctxPresc && charts.prescriptions) {
      new Chart(ctxPresc, {
        type: 'line',
        data: {
          labels: charts.prescriptions.labels,
          datasets: [{
            label: 'Prescriptions Issued',
            data: charts.prescriptions.values,
            borderColor: '#3b82f6',
            backgroundColor: 'rgba(59, 130, 246, 0.12)',
            fill: true,
            tension: 0.35,
            borderWidth: 2.5,
            pointBackgroundColor: '#2563eb',
            pointRadius: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            y: {
              beginAtZero: true,
              ticks: { stepSize: 1 },
              grid: { color: '#f1f5f9' }
            },
            x: { grid: { display: false } }
          }
        }
      });
    }

    // 3. Inventory Distribution Chart (Doughnut)
    const ctxInv = document.getElementById('chartInventory');
    if (ctxInv && charts.inventory) {
      new Chart(ctxInv, {
        type: 'doughnut',
        data: {
          labels: charts.inventory.labels,
          datasets: [{
            data: charts.inventory.values,
            backgroundColor: [
              '#0d9488', '#3b82f6', '#f59e0b', '#8b5cf6', 
              '#ec4899', '#10b981', '#64748b'
            ],
            borderWidth: 2,
            borderColor: '#ffffff'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'bottom', labels: { boxWidth: 12, padding: 12 } }
          },
          cutout: '68%'
        }
      });
    }

    // 4. Order Status Breakdown (Pie)
    const ctxOrders = document.getElementById('chartOrders');
    if (ctxOrders && charts.orders) {
      new Chart(ctxOrders, {
        type: 'pie',
        data: {
          labels: charts.orders.labels,
          datasets: [{
            data: charts.orders.values,
            backgroundColor: ['#10b981', '#f59e0b', '#3b82f6', '#6366f1', '#ef4444'],
            borderWidth: 2,
            borderColor: '#ffffff'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'bottom', labels: { boxWidth: 12, padding: 12 } }
          }
        }
      });
    }

    // 5. Low Stock Medicines Chart (Bar)
    const ctxLowStock = document.getElementById('chartLowStock');
    if (ctxLowStock && charts.low_stock) {
      new Chart(ctxLowStock, {
        type: 'bar',
        data: {
          labels: charts.low_stock.labels,
          datasets: [
            {
              label: 'Stock on Hand',
              data: charts.low_stock.stock,
              backgroundColor: 'rgba(239, 68, 68, 0.85)',
              borderRadius: 4
            },
            {
              label: 'Reorder Threshold',
              data: charts.low_stock.reorder,
              backgroundColor: 'rgba(203, 213, 225, 0.7)',
              borderRadius: 4
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'top', labels: { boxWidth: 12 } }
          },
          scales: {
            y: { beginAtZero: true, grid: { color: '#f1f5f9' } },
            x: { grid: { display: false }, ticks: { font: { size: 11 } } }
          }
        }
      });
    }

    // 6. Top 5 Prescribed Medicines (Horizontal Bar)
    const ctxTopMeds = document.getElementById('chartTopMeds');
    if (ctxTopMeds && charts.top_medicines) {
      new Chart(ctxTopMeds, {
        type: 'bar',
        indexAxis: 'y',
        data: {
          labels: charts.top_medicines.labels,
          datasets: [{
            label: 'Prescription Frequency',
            data: charts.top_medicines.values,
            backgroundColor: 'rgba(15, 52, 96, 0.85)',
            borderColor: '#0f3460',
            borderWidth: 1,
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { beginAtZero: true, ticks: { stepSize: 1 }, grid: { color: '#f1f5f9' } },
            y: { grid: { display: false } }
          }
        }
      });
    }

  } catch (err) {
    console.error('Error loading dashboard analytics charts:', err);
  }
});
