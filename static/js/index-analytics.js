// Home Page Analytics

let applicationsChart = null;
let programsChart = null;

document.addEventListener('DOMContentLoaded', () => {
  initializeTooltips();
  preloadChartsData();
});

function initializeTooltips() {
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
}

// Preload chart data when modals are about to show
document.getElementById('applicationsModal')?.addEventListener('show.bs.modal', renderApplicationsChart);
document.getElementById('programsModal')?.addEventListener('show.bs.modal', renderProgramsChart);

async function preloadChartsData() {
  try {
    // Preload data for faster modal opening
    const [uniResponse, programResponse] = await Promise.all([
      fetch('/api/analytics/universities'),
      fetch('/api/analytics/programs')
    ]);

    if (!uniResponse.ok || !programResponse.ok) {
      console.warn('Failed to preload analytics data');
      return;
    }

    window.uniData = await uniResponse.json();
    window.programData = await programResponse.json();
  } catch (error) {
    console.warn('Error preloading analytics:', error);
  }
}

function showApplicationsModal() {
  const modal = new bootstrap.Modal(document.getElementById('applicationsModal'));
  modal.show();
}

function showProgramsModal() {
  const modal = new bootstrap.Modal(document.getElementById('programsModal'));
  modal.show();
}

async function renderApplicationsChart() {
  try {
    let uniData = window.uniData;

    if (!uniData) {
      const response = await fetch('/api/analytics/universities');
      if (!response.ok) throw new Error('Failed to fetch data');
      uniData = await response.json();
      window.uniData = uniData;
    }

    const universities = uniData.universities || [];
    const totalApps = universities.reduce((sum, u) => sum + u.total_applications, 0);
    const totalAdmits = universities.reduce((sum, u) => sum + u.admits, 0);
    const totalRejects = universities.reduce((sum, u) => sum + u.rejects, 0);
    const totalWaitlists = universities.reduce((sum, u) => sum + u.waitlists, 0);

    // Update stats
    document.getElementById('modal-total-apps').textContent = totalApps;
    const successRate = totalApps > 0 ? ((totalAdmits / totalApps) * 100).toFixed(1) : 0;
    document.getElementById('modal-success-rate').textContent = successRate + '%';

    // Render pie chart
    const ctx = document.getElementById('applications-pie-chart').getContext('2d');

    if (applicationsChart) {
      applicationsChart.destroy();
    }

    applicationsChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Admits', 'Rejects', 'Waitlists'],
        datasets: [{
          data: [totalAdmits, totalRejects, totalWaitlists],
          backgroundColor: ['#198754', '#dc3545', '#ffc107'],
          borderColor: '#fff',
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              usePointStyle: true,
              padding: 15,
              font: { size: 13 }
            }
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                const label = context.label || '';
                const value = context.parsed || 0;
                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                const percentage = ((value / total) * 100).toFixed(1);
                return `${label}: ${value} (${percentage}%)`;
              }
            }
          }
        }
      }
    });
  } catch (error) {
    console.error('Error rendering applications chart:', error);
    document.getElementById('applications-pie-chart').parentElement.innerHTML =
      '<p class="text-danger text-center">Failed to load chart</p>';
  }
}

async function renderProgramsChart() {
  try {
    let programData = window.programData;

    if (!programData) {
      const response = await fetch('/api/analytics/programs');
      if (!response.ok) throw new Error('Failed to fetch data');
      programData = await response.json();
      window.programData = programData;
    }

    const programs = (programData.programs || [])
      .sort((a, b) => b.total_applications - a.total_applications)
      .slice(0, 8);

    // Render pie chart
    const ctx = document.getElementById('programs-pie-chart').getContext('2d');

    if (programsChart) {
      programsChart.destroy();
    }

    const chartColors = [
      '#0d6efd', '#dc3545', '#198754', '#ffc107', '#0dcaf0',
      '#d63384', '#fd7e14', '#6f42c1'
    ];

    programsChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: programs.map(p => p.program),
        datasets: [{
          data: programs.map(p => p.total_applications),
          backgroundColor: chartColors.slice(0, programs.length),
          borderColor: '#fff',
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: {
            position: 'right',
            labels: {
              font: { size: 11 },
              padding: 10,
              usePointStyle: true
            }
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                const label = context.label || '';
                const value = context.parsed || 0;
                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                const percentage = ((value / total) * 100).toFixed(1);
                return `${label}: ${value} (${percentage}%)`;
              }
            }
          }
        }
      }
    });
  } catch (error) {
    console.error('Error rendering programs chart:', error);
    document.getElementById('programs-pie-chart').parentElement.innerHTML =
      '<p class="text-danger text-center">Failed to load chart</p>';
  }
}

// Add animation to stat cards on page load
window.addEventListener('load', () => {
  const statCards = document.querySelectorAll('.stat-card');
  statCards.forEach((card, index) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    setTimeout(() => {
      card.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, index * 100);
  });
});
