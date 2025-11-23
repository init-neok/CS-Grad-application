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

  function setFormLoading(form, isLoading) {
    const button = form.querySelector('button[type="submit"]');
    if (!button) return;

    const spinner = button.querySelector('.spinner-border');
    if (!spinner) return;

    if (isLoading) {
      button.disabled = true;
      spinner.classList.remove('d-none');
    } else {
      button.disabled = false;
      spinner.classList.add('d-none');
    }
  }

  function validateForm(form) {
    const email = form.elements.email?.value?.trim();
    const password = form.elements.password?.value;

    if (!email || !email.includes('@')) {
      setAlert('Please enter a valid email address', 'warning');
      return false;
    }

    if (!password || password.length < 6) {
      setAlert('Password must be at least 6 characters', 'warning');
      return false;
    }

    return true;
  }

  async function submitForm(form, endpoint) {
    if (!validateForm(form)) {
      return;
    }

    const payload = formToJSON(form);
    setFormLoading(form, true);

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
      }, 600);
    } catch (error) {
      console.error('Auth error:', error);
      setAlert(error.message, 'danger');
      setFormLoading(form, false);
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
