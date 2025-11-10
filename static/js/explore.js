(function () {
  const form = document.getElementById('search-form');
  const resultsBody = document.getElementById('results-body');
  const resultsCount = document.getElementById('results-count');
  const resetButton = document.getElementById('reset-search');

  if (!form) return;

  function formToParams() {
    const data = new FormData(form);
    const params = {};
    data.forEach((value, key) => {
      if (value) {
        params[key] = value;
      }
    });
    return params;
  }

  function renderResults(results) {
    if (!resultsBody) return;
    resultsBody.innerHTML = results
      .map(
        (item) => `
        <tr>
          <td>${item.university}</td>
          <td>${item.program}</td>
          <td>${item.degree || '-'}</td>
          <td>${item.term || '-'}</td>
          <td>
            <span class="badge bg-${badgeForResult(item.result)}">${item.result}</span>
          </td>
          <td>${formatScore(item.gpa, item.gpa_scale)}</td>
          <td>${item.gre_total ?? '—'}</td>
        </tr>
      `,
      )
      .join('');
    if (resultsCount) {
      resultsCount.textContent = `Showing ${results.length} entries.`;
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

  function formatScore(gpa, scale) {
    if (!gpa) return '—';
    if (scale) {
      return `${gpa}/${scale}`;
    }
    return gpa;
  }

  async function performSearch(event) {
    event?.preventDefault();
    try {
      const params = formToParams();
      const query = new URLSearchParams(params);
      const resp = await fetch(`/api/search/applications?${query.toString()}`);
      const results = await resp.json();
      renderResults(results);
    } catch (error) {
      resultsBody.innerHTML = `<tr><td colspan="7" class="text-danger">${error.message}</td></tr>`;
    }
  }

  form.addEventListener('submit', performSearch);
  resetButton?.addEventListener('click', () => {
    setTimeout(() => performSearch(), 0);
  });

  performSearch();
})();
