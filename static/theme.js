document.addEventListener('DOMContentLoaded', () => {
    const themeToggleButton = document.getElementById('theme-toggle-button');
    const body = document.body;

    function applyTheme(theme) {
        if (theme === 'dark') {
            body.classList.add('dark-theme');
            if (themeToggleButton) {
                themeToggleButton.textContent = 'Mudar para Tema Claro';
            }
        } else {
            body.classList.remove('dark-theme');
            if (themeToggleButton) {
                themeToggleButton.textContent = 'Mudar para Tema Escuro';
            }
        }
    }

    // Load saved theme from localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        applyTheme(savedTheme);
    } else {
        applyTheme('light'); // Default to light, also sets initial button text if button exists
    }

    // Event listener only if button exists
    if (themeToggleButton) {
        themeToggleButton.addEventListener('click', () => {
            let currentTheme = body.classList.contains('dark-theme') ? 'dark' : 'light';
            let newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            applyTheme(newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }
});
