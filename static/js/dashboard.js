(function () {
  const profileForm = document.getElementById('profile-form');
  const applicationForm = document.getElementById('application-form');
  const applicationsTable = document.getElementById('applications-table');
  const suggestionsContainer = document.getElementById('suggestions');
  const alertBox = document.getElementById('dashboard-alert');
  const refreshApplicationsBtn = document.getElementById('refresh-applications');
  const refreshSuggestionsBtn = document.getElementById('refresh-suggestions');

  if (!profileForm || !applicationForm) {
    return;
  }

  function formToJSON(form) {
    const data = new FormData(form);
    const json = {};
    data.forEach((value, key) => {
      json[key] = value;
    });
    // booleans
    ['research_experience', 'internship_experience'].forEach((field) => {
      if (form.elements[field]) {
        json[field] = form.elements[field].checked;
      }
    });
    return json;
  }

  function cleanupPayload(payload) {
    const numericFields = [
      'gpa',
      'gpa_scale',
      'gre_total',
      'toefl_total',
      'start_year',
      'end_year',
    ];
    numericFields.forEach((field) => {
      if (field in payload) {
        const value = payload[field];
        if (value === '' || value === null || Number.isNaN(Number(value))) {
          delete payload[field];
        } else {
          payload[field] = Number(value);
        }
      }
    });
    return payload;
  }

  function showAlert(message, type = 'info') {
    if (!alertBox) return;
    alertBox.textContent = message;
    alertBox.className = `alert alert-${type}`;
  }

  async function apiFetch(url, options = {}) {
    const response = await fetch(url, {
      credentials: 'same-origin',
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      const message = data.error || 'Request failed';
      throw new Error(message);
    }
    return data;
  }

  async function loadProfile() {
    try {
      const data = await apiFetch('/api/profile');
      const profile = data.profile || {};
      Object.entries(profile).forEach(([key, value]) => {
        const field = profileForm.elements[key];
        if (!field) return;
        if (field.type === 'checkbox') {
          field.checked = Boolean(value);
        } else {
          field.value = value ?? '';
        }
      });
    } catch (error) {
      showAlert(error.message, 'danger');
    }
  }

  async function saveProfile(event) {
    event.preventDefault();
    const payload = cleanupPayload(formToJSON(profileForm));
    try {
      await apiFetch('/api/profile', {
        method: 'PUT',
        body: JSON.stringify(payload),
      });
      showAlert('Profile saved', 'success');
      await loadSuggestions();
    } catch (error) {
      showAlert(error.message, 'danger');
    }
  }

  async function loadApplications() {
    try {
      const apps = await apiFetch('/api/applications/my');
      if (applicationsTable) {
        applicationsTable.innerHTML =
          apps
            .map(
              (app) => `
            <tr>
              <td>${app.university}</td>
              <td>${app.program}</td>
              <td>${app.term || '-'}</td>
              <td>
                <span class="badge bg-${badgeForResult(app.result)}">${app.result}</span>
              </td>
              <td class="text-end">
                <button class="btn btn-sm btn-link text-danger" data-delete="${app.id}">Delete</button>
              </td>
            </tr>
          `,
            )
            .join('');
      }
    } catch (error) {
      showAlert(error.message, 'danger');
    }
  }

  function badgeForResult(result) {
    switch ((result || '').toLowerCase()) {
      case 'admit':
        return 'success';
      case 'waitlist':
        return 'warning text-dark';
      default:
        return 'secondary';
    }
  }

  async function createApplication(event) {
    event.preventDefault();
    const payload = cleanupPayload(formToJSON(applicationForm));
    try {
      await apiFetch('/api/applications', {
        method: 'POST',
        body: JSON.stringify(payload),
      });
      applicationForm.reset();
      showAlert('Application added', 'success');
      await loadApplications();
      await loadSuggestions();
    } catch (error) {
      showAlert(error.message, 'danger');
    }
  }

  async function deleteApplication(id) {
    if (!id) return;
    try {
      await apiFetch(`/api/applications/${id}`, { method: 'DELETE' });
      showAlert('Application deleted', 'info');
      await loadApplications();
      await loadSuggestions();
    } catch (error) {
      showAlert(error.message, 'danger');
    }
  }

  async function loadSuggestions() {
    if (!suggestionsContainer) return;
    suggestionsContainer.innerHTML = '<p class="text-muted">Loading…</p>';
    try {
      const data = await apiFetch('/api/match/suggestions', { method: 'GET', headers: {} });
      const sections = ['reach', 'match', 'safe'];
      suggestionsContainer.innerHTML = sections
        .map((section) => renderSuggestionSection(section, data[section] || []))
        .join('');
    } catch (error) {
      suggestionsContainer.innerHTML = `<p class="text-danger">${error.message}</p>`;
    }
  }

  function renderSuggestionSection(section, list) {
    if (!list.length) {
      return `
        <div class="suggestion-card ${section}">
          <div class="fw-semibold text-capitalize">${section}</div>
          <p class="mb-0 text-muted">Not enough data yet.</p>
        </div>`;
    }
    return `
      <div class="suggestion-card ${section}">
        <div class="fw-semibold text-capitalize mb-1">${section} (${list.length})</div>
        ${
          list
            .map(
              (item) => `
                <div class="mb-2">
                  <div>${item.university} · ${item.program}</div>
                  <small class="text-muted">Admit rate: ${(item.admit_rate * 100 || 0).toFixed(1)}% · Avg GPA: ${
                    item.avg_gpa ?? 'N/A'
                  }</small>
                </div>
              `,
            )
            .join('')
        }
      </div>`;
  }

  applicationsTable?.addEventListener('click', (event) => {
    const target = event.target;
    if (target.matches('[data-delete]')) {
      const id = target.getAttribute('data-delete');
      deleteApplication(id);
    }
  });

  profileForm.addEventListener('submit', saveProfile);
  applicationForm.addEventListener('submit', createApplication);
  refreshApplicationsBtn?.addEventListener('click', loadApplications);
  refreshSuggestionsBtn?.addEventListener('click', loadSuggestions);

  loadProfile();
  loadApplications();
  loadSuggestions();
})();
