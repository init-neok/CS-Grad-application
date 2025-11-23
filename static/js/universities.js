// Universities Analytics Page

let universityData = [];
let programData = [];
let regionalData = [];
let charts = {};
let selectedRegion = null;

const chartColors = [
  '#0d6efd', '#dc3545', '#198754', '#ffc107', '#0dcaf0',
  '#d63384', '#fd7e14', '#6f42c1', '#20c997', '#adb5bd',
  '#e83e8c', '#0099ff', '#00cc99', '#ff9900', '#cc0099'
];

document.addEventListener('DOMContentLoaded', () => {
  loadAnalyticsData();
});

async function loadAnalyticsData() {
  try {
    showLoader(true);

    // Load all data in parallel
    const [uniResponse, programResponse, regionalResponse] = await Promise.all([
      fetch('/api/analytics/universities'),
      fetch('/api/analytics/programs'),
      fetch('/api/analytics/regional')
    ]);

    if (!uniResponse.ok || !programResponse.ok || !regionalResponse.ok) {
      throw new Error('Failed to load analytics data');
    }

    const uniDataWrapper = await uniResponse.json();
    const programDataWrapper = await programResponse.json();
    const regionalDataWrapper = await regionalResponse.json();

    universityData = uniDataWrapper.universities || [];
    programData = programDataWrapper.programs || [];
    regionalData = regionalDataWrapper.regions || [];

    updateStats();
    renderOverviewTab();
    renderProgramsTab();
    renderRegionalTab();
  } catch (error) {
    console.error('Error loading analytics:', error);
    alert('Failed to load analytics data. Please try again.');
  } finally {
    showLoader(false);
  }
}

function updateStats() {
  const totalApps = universityData.reduce((sum, uni) => sum + uni.total_applications, 0);
  document.getElementById('uni-count').textContent = universityData.length;
  document.getElementById('total-apps').textContent = totalApps;
}

function showLoader(show) {
  const spinner = document.getElementById('loading-spinner');
  if (show) {
    spinner.classList.remove('d-none');
  } else {
    spinner.classList.add('d-none');
  }
}

// ===== OVERVIEW TAB =====
function renderOverviewTab() {
  renderUniversityPieChart();
  renderTopUniversitiesList();
  renderUniversityScatterChart();
}

function renderUniversityPieChart() {
  // Sort by application count and take top universities
  const topUnis = universityData
    .sort((a, b) => b.total_applications - a.total_applications)
    .slice(0, 10);

  const ctx = document.getElementById('uni-pie-chart').getContext('2d');

  if (charts.uniPie) {
    charts.uniPie.destroy();
  }

  charts.uniPie = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: topUnis.map(u => u.university),
      datasets: [{
        data: topUnis.map(u => u.total_applications),
        backgroundColor: chartColors.slice(0, topUnis.length),
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
            font: { size: 12 },
            padding: 15,
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
}

function renderTopUniversitiesList() {
  const topUnis = universityData
    .sort((a, b) => b.admit_rate - a.admit_rate)
    .slice(0, 10);

  const html = topUnis.map((uni, idx) => `
    <div class="mb-3 p-3 border rounded hover-highlight" style="cursor: pointer; transition: all 0.3s;" onclick="showUniversityDetails('${uni.university}')">
      <div class="d-flex justify-content-between align-items-start">
        <div>
          <div class="fw-bold">${idx + 1}. ${uni.university}</div>
          <small class="text-muted">${uni.country || 'Unknown'}</small>
        </div>
        <div class="text-end">
          <div class="fw-bold text-success">${(uni.admit_rate * 100).toFixed(1)}%</div>
          <small class="text-muted">${uni.admits}/${uni.total_applications}</small>
        </div>
      </div>
      <div class="mt-2">
        <div class="progress" style="height: 6px;">
          <div class="progress-bar bg-success" style="width: ${uni.admit_rate * 100}%"></div>
        </div>
      </div>
    </div>
  `).join('');

  document.getElementById('top-unis-list').innerHTML = html;

  // Add hover animation
  document.querySelectorAll('.hover-highlight').forEach(el => {
    el.addEventListener('mouseenter', function() {
      this.style.backgroundColor = '#f8f9fa';
      this.style.transform = 'translateX(5px)';
    });
    el.addEventListener('mouseleave', function() {
      this.style.backgroundColor = '';
      this.style.transform = '';
    });
  });
}

function renderUniversityScatterChart() {
  // Create scatter plot: X = applications, Y = admit rate
  const data = universityData.map(uni => ({
    x: uni.total_applications,
    y: uni.admit_rate * 100,
    label: uni.university,
    admits: uni.admits
  }));

  const ctx = document.getElementById('uni-scatter-chart').getContext('2d');

  if (charts.scatter) {
    charts.scatter.destroy();
  }

  charts.scatter = new Chart(ctx, {
    type: 'scatter',
    data: {
      datasets: [{
        label: 'Universities',
        data: data,
        backgroundColor: '#0d6efd',
        borderColor: '#0d6efd',
        borderWidth: 2,
        radius: 6,
        hoverRadius: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          display: true
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const point = context.raw;
              return `${point.label}: ${point.admits}/${point.x} admits`;
            }
          }
        }
      },
      scales: {
        x: {
          type: 'linear',
          position: 'bottom',
          title: {
            display: true,
            text: 'Total Applications'
          }
        },
        y: {
          title: {
            display: true,
            text: 'Admit Rate (%)'
          },
          min: 0,
          max: 100
        }
      }
    }
  });
}

// ===== PROGRAMS TAB =====
function renderProgramsTab() {
  renderProgramBarChart();
  renderProgramsTable();
}

function renderProgramBarChart() {
  // Sort by application count
  const sortedPrograms = programData
    .sort((a, b) => b.total_applications - a.total_applications)
    .slice(0, 15);

  const ctx = document.getElementById('program-bar-chart').getContext('2d');

  if (charts.programBar) {
    charts.programBar.destroy();
  }

  charts.programBar = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: sortedPrograms.map(p => p.program),
      datasets: [
        {
          label: 'Total Applications',
          data: sortedPrograms.map(p => p.total_applications),
          backgroundColor: '#0d6efd',
          borderColor: '#0d6efd',
          borderWidth: 1
        },
        {
          label: 'Admits',
          data: sortedPrograms.map(p => p.admits),
          backgroundColor: '#198754',
          borderColor: '#198754',
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      indexAxis: 'y',
      plugins: {
        legend: {
          position: 'top'
        }
      },
      scales: {
        x: {
          stacked: false
        }
      }
    }
  });
}

function renderProgramsTable() {
  const sortedPrograms = programData.sort((a, b) => b.total_applications - a.total_applications);

  const rows = sortedPrograms.map(prog => `
    <tr>
      <td class="fw-bold">${prog.program}</td>
      <td class="text-end">${prog.total_applications}</td>
      <td class="text-end">${prog.admits}</td>
      <td class="text-end">
        <span class="badge bg-primary">${(prog.admit_rate * 100).toFixed(1)}%</span>
      </td>
      <td class="text-center">
        <span class="badge bg-secondary">${prog.universities.length}</span>
      </td>
    </tr>
  `).join('');

  document.getElementById('programs-table-body').innerHTML = rows;
}

// ===== REGIONAL TAB =====
function renderRegionalTab() {
  renderRegionSelector();
  if (regionalData.length > 0) {
    selectRegion(regionalData[0].country);
  }
}

function renderRegionSelector() {
  const regions = regionalData.map(r => r.country);

  const html = regions.map(country => `
    <button
      class="btn btn-outline-primary region-btn"
      data-region="${country}"
      onclick="selectRegion('${country}')"
      style="transition: all 0.3s ease;"
    >
      ${country}
      <span class="badge bg-primary ms-2">${regionalData.find(r => r.country === country).total_applications}</span>
    </button>
  `).join('');

  document.getElementById('region-selector').innerHTML = html;
}

function selectRegion(country) {
  selectedRegion = country;

  // Update button styles
  document.querySelectorAll('.region-btn').forEach(btn => {
    if (btn.getAttribute('data-region') === country) {
      btn.classList.remove('btn-outline-primary');
      btn.classList.add('btn-primary');
    } else {
      btn.classList.add('btn-outline-primary');
      btn.classList.remove('btn-primary');
    }
  });

  const regionData = regionalData.find(r => r.country === country);
  if (regionData) {
    renderRegionalChart(regionData);
    renderRegionalTable(regionData);
    document.getElementById('region-chart-title').textContent = `${country} - Universities`;
  }
}

function renderRegionalChart(regionData) {
  // Sort universities by applications
  const universities = regionData.universities
    .sort((a, b) => b.applications - a.applications)
    .slice(0, 12);

  const ctx = document.getElementById('regional-chart').getContext('2d');

  if (charts.regional) {
    charts.regional.destroy();
  }

  charts.regional = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: universities.map(u => u.university),
      datasets: [
        {
          label: 'Total Applications',
          data: universities.map(u => u.applications),
          backgroundColor: '#0d6efd',
          borderColor: '#0d6efd',
          borderWidth: 1
        },
        {
          label: 'Admits',
          data: universities.map(u => u.admits),
          backgroundColor: '#198754',
          borderColor: '#198754',
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      indexAxis: 'y',
      plugins: {
        legend: {
          position: 'top'
        }
      }
    }
  });
}

function renderRegionalTable(regionData) {
  const universities = regionData.universities.sort((a, b) => b.applications - a.applications);

  const rows = universities.map(uni => `
    <tr style="cursor: pointer; transition: background-color 0.2s;"
        onmouseover="this.style.backgroundColor='#f8f9fa'"
        onmouseout="this.style.backgroundColor=''"
        onclick="showUniversityDetails('${uni.university}')">
      <td class="fw-bold">${uni.university}</td>
      <td class="text-end">${uni.applications}</td>
      <td class="text-end">${uni.admits}</td>
      <td class="text-end">
        <span class="badge bg-success">${(uni.admit_rate * 100).toFixed(1)}%</span>
      </td>
    </tr>
  `).join('');

  document.getElementById('regional-table-body').innerHTML = rows || '<tr><td colspan="4" class="text-center text-muted py-4">No universities found</td></tr>';
}

// ===== MODAL & DETAILS =====
function showUniversityDetails(universityName) {
  const uni = universityData.find(u => u.university === universityName);
  if (!uni) return;

  const admitRateColor = uni.admit_rate > 0.5 ? 'success' : uni.admit_rate > 0.3 ? 'warning' : 'danger';

  const html = `
    <div>
      <h5 class="mb-1">${uni.university}</h5>
      <p class="text-muted mb-3">${uni.country || 'Unknown'}</p>

      <div class="row g-3 mb-4">
        <div class="col-md-4">
          <div class="p-3 bg-light rounded">
            <div class="text-muted small">Total Applications</div>
            <div class="display-5">${uni.total_applications}</div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="p-3 bg-light rounded">
            <div class="text-muted small">Admits</div>
            <div class="display-5 text-success">${uni.admits}</div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="p-3 bg-light rounded">
            <div class="text-muted small">Admit Rate</div>
            <div class="display-5"><span class="badge bg-${admitRateColor}">${(uni.admit_rate * 100).toFixed(1)}%</span></div>
          </div>
        </div>
      </div>

      <div class="row g-3 mb-4">
        <div class="col-md-6">
          <div class="p-3 bg-light rounded">
            <div class="text-muted small">Rejects</div>
            <div class="display-6 text-danger">${uni.rejects}</div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="p-3 bg-light rounded">
            <div class="text-muted small">Waitlists</div>
            <div class="display-6 text-warning">${uni.waitlists}</div>
          </div>
        </div>
      </div>

      <div class="mb-3">
        <h6 class="mb-2">Programs Offered</h6>
        <div class="d-flex flex-wrap gap-2">
          ${uni.programs.map(prog => `<span class="badge bg-primary">${prog}</span>`).join('')}
        </div>
      </div>

      <div class="mb-0">
        <h6 class="mb-2">Result Distribution</h6>
        <div class="progress mb-2" style="height: 24px;">
          <div class="progress-bar bg-success" style="width: ${(uni.admits / uni.total_applications * 100).toFixed(1)}%" title="Admits">
            <small class="text-dark fw-bold">${uni.admits}</small>
          </div>
          <div class="progress-bar bg-danger" style="width: ${(uni.rejects / uni.total_applications * 100).toFixed(1)}%" title="Rejects">
            <small class="text-dark fw-bold">${uni.rejects}</small>
          </div>
          <div class="progress-bar bg-warning" style="width: ${(uni.waitlists / uni.total_applications * 100).toFixed(1)}%" title="Waitlists">
            <small class="text-dark fw-bold">${uni.waitlists}</small>
          </div>
        </div>
      </div>
    </div>
  `;

  document.getElementById('universityDetails').innerHTML = html;

  const modal = new bootstrap.Modal(document.getElementById('universityModal'));
  modal.show();
}
