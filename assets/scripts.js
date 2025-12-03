
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

// Event Editing
function editEvent(eventId, date) {
    const eventItem = document.querySelector(`[data-event-id="${eventId}"]`);
    const noteSpan = document.getElementById(`event-note-${eventId}`);
    const actionsDiv = eventItem.querySelector('.event-actions');
    
    if (!noteSpan || noteSpan.classList.contains('editing')) return;
    
    const currentNote = noteSpan.textContent;
    
    // Crear input de edición
    const input = document.createElement('input');
    input.type = 'text';
    input.value = currentNote;
    input.className = 'event-note-input';
    input.id = `event-input-${eventId}`;
    
    // Crear botones de guardar y cancelar
    const saveBtn = document.createElement('button');
    saveBtn.textContent = '✓';
    saveBtn.className = 'btn-icon save-small';
    saveBtn.title = 'Guardar';
    saveBtn.onclick = () => saveEventEdit(eventId, date);
    
    const cancelBtn = document.createElement('button');
    cancelBtn.textContent = '✕';
    cancelBtn.className = 'btn-icon cancel-small';
    cancelBtn.title = 'Cancelar';
    cancelBtn.onclick = () => cancelEventEdit(eventId, currentNote);
    
    // Reemplazar span con input
    noteSpan.replaceWith(input);
    noteSpan.classList.add('editing');
    
    // Reemplazar botones de acción con botones de guardar/cancelar
    actionsDiv.innerHTML = '';
    actionsDiv.appendChild(saveBtn);
    actionsDiv.appendChild(cancelBtn);
    
    // Focus en el input
    input.focus();
    input.select();
    
    // Permitir guardar con Enter
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            saveEventEdit(eventId, date);
        } else if (e.key === 'Escape') {
            cancelEventEdit(eventId, currentNote);
        }
    });
}

function saveEventEdit(eventId, date) {
    const input = document.getElementById(`event-input-${eventId}`);
    if (!input) return;
    
    const newNote = input.value.trim();
    
    // Usar HTMX para hacer la petición PUT
    htmx.ajax('PUT', `/events/${eventId}`, {
        values: { note: newNote },
        target: `#event-input-${eventId}`,
        swap: 'outerHTML'
    }).then(() => {
        // Después de actualizar, restaurar los botones de acción
        restoreEventActions(eventId, date);
    });
}

function cancelEventEdit(eventId, originalNote) {
    const input = document.getElementById(`event-input-${eventId}`);
    if (!input) return;
    
    // Restaurar el span original
    const noteSpan = document.createElement('span');
    noteSpan.textContent = originalNote;
    noteSpan.className = 'event-note';
    noteSpan.id = `event-note-${eventId}`;
    
    input.replaceWith(noteSpan);
    
    // Restaurar botones de acción
    restoreEventActions(eventId, '');
}

function restoreEventActions(eventId, date) {
    const eventItem = document.querySelector(`[data-event-id="${eventId}"]`);
    if (!eventItem) return;
    
    const actionsDiv = eventItem.querySelector('.event-actions');
    if (!actionsDiv) return;
    
    // Recrear botones originales
    actionsDiv.innerHTML = `
        <button class="btn-icon edit-small" onclick="editEvent(${eventId}, '${date}')" title="Editar">✏️</button>
        <button class="btn-icon delete-small" 
                hx-delete="/events/${eventId}" 
                hx-target="closest .event-item" 
                hx-swap="outerHTML"
                title="Eliminar">✕</button>
    `;
    
    // Re-procesar HTMX en los nuevos botones
    htmx.process(actionsDiv);
}
