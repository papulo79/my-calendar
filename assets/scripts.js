
function openDayModal(date) {
    htmx.ajax('GET', '/day/' + date, '#day-modal-container');
}

function closeDayModal() {
    document.getElementById('day-modal-container').innerHTML = '';
}

function toggleOptionsPanel() {
    const panel = document.getElementById('options-panel');
    if (panel) panel.classList.toggle('hidden');
}

// Emoji Picker Logic
function toggleEmojiPicker() {
    const picker = document.getElementById('emoji-picker-container');
    picker.classList.toggle('hidden');
}

document.addEventListener('DOMContentLoaded', () => {
    const picker = document.querySelector('emoji-picker');
    if (picker) {
        picker.addEventListener('emoji-click', event => {
            const input = document.getElementById('icon-input');
            input.value = event.detail.unicode;
            document.getElementById('emoji-picker-container').classList.add('hidden');
        });
    }

    // Close picker when clicking outside
    document.addEventListener('click', (e) => {
        const wrapper = document.querySelector('.icon-picker-wrapper');
        const pickerContainer = document.getElementById('emoji-picker-container');
        if (wrapper && !wrapper.contains(e.target) && pickerContainer && !pickerContainer.classList.contains('hidden')) {
            pickerContainer.classList.add('hidden');
        }
    });

    // Initialize Theme
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);

    // Set initial checkbox state
    const checkbox = document.getElementById('theme-toggle-checkbox');
    if (checkbox) {
        checkbox.checked = savedTheme === 'dark';
    }

    // Close modals on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeDayModal();
            const pickerContainer = document.getElementById('emoji-picker-container');
            if (pickerContainer && !pickerContainer.classList.contains('hidden')) {
                pickerContainer.classList.add('hidden');
            }
        }
    });
});

// Theme Toggle
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}
