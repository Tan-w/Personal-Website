particlesJS("particles-js", {
    "particles": {
        "number": { "value": 80 },
        "color": { "value": "#3a86ff" },
        "shape": { "type": "circle" },
        "opacity": { "value": 0.5 },
        "size": { "value": 3 },
        "line_linked": {
            "enable": true,
            "distance": 150,
            "color": "#ffffff",
            "opacity": 0.4,
            "width": 1
        },
        "move": { "enable": true, "speed": 2 }
    },
    "interactivity": {
        "events": { "onhover": { "enable": true, "mode": "repulse" } }
    }
});

// UI helpers for the Work Allocation page
function showSection(name) {
    const allocationCol = document.querySelector('.allocation-col');
    const assignedCol = document.querySelector('.assigned-col');
    const adminPanel = document.querySelector('.admin-panel');
    // update visibility
    if (allocationCol) allocationCol.style.display = (name === 'available') ? '' : 'none';
    if (assignedCol) assignedCol.style.display = (name === 'progress') ? '' : 'none';
    if (adminPanel) adminPanel.style.display = (name === 'add-task') ? '' : 'none';

    // update nav active class
    document.querySelectorAll('.sfa-sidebar .nav-item').forEach(el => el.classList.remove('active'));
    const selector = `.sfa-sidebar .nav-item[onclick="showSection('${name}')"]`;
    const active = document.querySelector(selector);
    if (active) active.classList.add('active');
}

function filterCourses() {
    const q = (document.getElementById('courseSearch') || { value: '' }).value.toLowerCase();
    document.querySelectorAll('.allocation-col .sfa-card').forEach(card => {
        const text = card.textContent.toLowerCase();
        card.style.display = text.includes(q) ? '' : 'none';
    });
}

// Calculation helper for admin form: requested by template
document.addEventListener('DOMContentLoaded', () => {
    const durationInput = document.querySelector('input[name="duration"]');
    const multiplierSelect = document.querySelector('select[name="multiplier"]');
    const reqTimeInput = document.querySelector('input[name="req_time"]');

    function updateCalculations() {
        if (!durationInput || !multiplierSelect || !reqTimeInput) return;
        let duration = parseFloat(durationInput.value) || 0;
        let multiplier = parseFloat(multiplierSelect.value) || 1.0;
        // Calculation: (Duration * 0.1) * Multiplier
        let baseReqTime = duration * 0.1;
        let finalReqTime = baseReqTime * multiplier;
        reqTimeInput.value = finalReqTime.toFixed(2);
    }

    if (durationInput) durationInput.addEventListener('input', updateCalculations);
    if (multiplierSelect) multiplierSelect.addEventListener('change', updateCalculations);

    // wire search input if present
    const search = document.getElementById('courseSearch');
    if (search) search.addEventListener('keyup', filterCourses);
});
function filterCourses() {
    // Get the text from the search bar
    let input = document.getElementById('courseSearch').value.toUpperCase();
    
    // Get all task cards in the Allocation column
    let cards = document.querySelectorAll('.allocation-col .sfa-card');

    cards.forEach(card => {
        // Find the CourseCode text within the card
        let textContent = card.innerText || card.textContent;
        
        // If the CourseCode exists in the card's text, show it; otherwise, hide it
        if (textContent.toUpperCase().indexOf(input) > -1) {
            card.style.display = "";
        } else {
            card.style.display = "none";
        }
    });
}
// Function to auto-calculate Required Time based on Duration and Multiplier
document.addEventListener('DOMContentLoaded', () => {
    const durationInput = document.querySelector('input[name="duration"]');
    const multiplierSelect = document.querySelector('select[name="multiplier"]');
    const reqTimeInput = document.querySelector('input[name="req_time"]');

    function calculateReqTime() {
        let duration = parseFloat(durationInput.value) || 0;
        let multiplier = parseFloat(multiplierSelect.value) || 1;
        
        // Custom Logic: Required Time = (Duration * 0.1) * Multiplier
        let result = (duration * 0.1) * multiplier;
        reqTimeInput.value = result.toFixed(2);
    }

    if(durationInput) {
        durationInput.addEventListener('input', calculateReqTime);
        multiplierSelect.addEventListener('change', calculateReqTime);
    }
});
function showSection(sectionId) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(section => {
        section.classList.remove('active');
    });
    // Remove active class from all nav items
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });

    // Show selected section and activate nav item
    document.getElementById(sectionId).classList.add('active');
    event.currentTarget.classList.add('active');
}