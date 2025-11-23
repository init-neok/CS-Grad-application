(function () {
  const form = document.getElementById('search-form');
  const resultsBody = document.getElementById('results-body');
  const resultsCount = document.getElementById('results-count');
  const resetButton = document.getElementById('reset-search');
  const searchSpinner = document.getElementById('search-spinner');

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

    if (!results || results.length === 0) {
      resultsBody.innerHTML = `
        <tr>
          <td colspan="8" class="text-center text-muted py-4">
            No matching records found. Try adjusting your filters.
          </td>
        </tr>
      `;
      if (resultsCount) {
        resultsCount.textContent = 'No results found.';
      }
      return;
    }

    resultsBody.innerHTML = results
      .map(
        (item) => `
        <tr>
          <td><strong>${escapeHtml(item.university)}</strong></td>
          <td>${escapeHtml(item.program)}</td>
          <td>${item.degree || '–'}</td>
          <td>${item.term || '–'}</td>
          <td>
            <span class="badge bg-${badgeForResult(item.result)}">${escapeHtml(item.result)}</span>
          </td>
          <td>${formatScore(item.gpa, item.gpa_scale)}</td>
          <td>${item.gre_total ?? '–'}</td>
          <td class="text-center">
            <span title="Research & Internship Experience">
              ${getExperienceBadges(item)}
            </span>
          </td>
        </tr>
      `,
      )
      .join('');
    if (resultsCount) {
      resultsCount.textContent = `Showing ${results.length} entries.`;
    }
  }

  function escapeHtml(text) {
    const map = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
  }

  function getExperienceBadges(item) {
    let badges = '';
    if (item.research_experience) {
      badges += '<span class="badge bg-primary me-1" title="Research experience">R</span>';
    }
    if (item.internship_experience) {
      badges += '<span class="badge bg-info" title="Internship experience">I</span>';
    }
    return badges || '–';
  }

  function badgeForResult(result) {
    switch ((result || '').toLowerCase()) {
      case 'admit':
        return 'success';
      case 'waitlist':
        return 'warning text-dark';
      case 'reject':
        return 'danger';
      default:
        return 'secondary';
    }
  }

  function formatScore(gpa, scale) {
    if (!gpa || gpa === null || gpa === undefined) return '–';
    if (scale && scale > 0) {
      return `${Number(gpa).toFixed(2)}/${Number(scale).toFixed(1)}`;
    }
    return Number(gpa).toFixed(2);
  }

  function setSearchLoading(isLoading) {
    if (searchSpinner) {
      if (isLoading) {
        searchSpinner.classList.remove('d-none');
      } else {
        searchSpinner.classList.add('d-none');
      }
    }
  }

  async function performSearch(event) {
    event?.preventDefault();
    setSearchLoading(true);
    try {
      const params = formToParams();
      const query = new URLSearchParams(params);
      const resp = await fetch(`/api/search/applications?${query.toString()}`);

      if (!resp.ok) {
        throw new Error('Failed to fetch search results');
      }

      const results = await resp.json();
      renderResults(results);
    } catch (error) {
      console.error('Search error:', error);
      resultsBody.innerHTML = `
        <tr>
          <td colspan="8" class="text-center text-danger py-3">
            <strong>Error loading results:</strong> ${escapeHtml(error.message)}
          </td>
        </tr>
      `;
    } finally {
      setSearchLoading(false);
    }
  }

  form.addEventListener('submit', performSearch);
  resetButton?.addEventListener('click', () => {
    setTimeout(() => performSearch(), 100);
  });

  // Initial search on page load
  performSearch();
})();
