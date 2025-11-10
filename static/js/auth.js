(function () {
  const scriptTag = document.currentScript;
  const nextUrl = scriptTag?.dataset?.next || '/dashboard';
  const alertBox = document.getElementById('auth-alert');
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');

  function formToJSON(form) {
    const data = new FormData(form);
    return Object.fromEntries(data.entries());
  }

  function setAlert(message, type = 'info') {
    if (!alertBox) return;
    alertBox.textContent = message;
    alertBox.className = `alert alert-${type}`;
  }

  async function submitForm(form, endpoint) {
    const payload = formToJSON(form);
    try {
      const resp = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify(payload),
      });
      const data = await resp.json().catch(() => ({}));
      if (!resp.ok) {
        throw new Error(data.error || 'Request failed');
      }
      setAlert('Success! Redirecting...', 'success');
      setTimeout(() => {
        window.location.href = nextUrl;
      }, 400);
    } catch (error) {
      setAlert(error.message, 'danger');
    }
  }

  loginForm?.addEventListener('submit', (event) => {
    event.preventDefault();
    submitForm(loginForm, '/api/login');
  });

  registerForm?.addEventListener('submit', (event) => {
    event.preventDefault();
    submitForm(registerForm, '/api/register');
  });
})();
