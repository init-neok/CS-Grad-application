document.addEventListener('DOMContentLoaded', () => {
  const logoutButton = document.querySelector('[data-logout]');
  if (logoutButton) {
    logoutButton.addEventListener('click', async () => {
      logoutButton.disabled = true;
      try {
        const resp = await fetch('/api/logout', { method: 'POST', credentials: 'same-origin' });
        if (!resp.ok) {
          throw new Error('Unable to logout');
        }
        window.location.href = '/';
      } catch (err) {
        console.error(err);
        logoutButton.disabled = false;
        alert('Failed to logout. Please try again.');
      }
    });
  }
});
