// Tab Switcher Notification
document.addEventListener("visibilitychange", () => {
    const favicon = document.getElementById("favicon");
    if (document.hidden) {
        // User switched away
        document.title = "404: Attention Not Found 💻";
        // 2. Change Favicon to "Away" icon
        favicon.href = "static/images/favicon.png";
    } else {
        // User came back
        document.title = "Let's build something great! 🚀";
        // 2. Restore Original
        favicon.href = "static/images/akm.jpg";
    }
});


$(document).ready(function() {
    $('#contactForm').on('submit', function(e) {
        e.preventDefault();
        
        let formData = $(this).serialize();
        
        $.ajax({
            url: '/save-message',
            type: 'POST',
            data: formData,
            success: function(response) {
                $('#responseMessage').text(response.message).addClass('text-success');
                $('#contactForm')[0].reset(); // Clear the form
            },
            error: function() {
                $('#responseMessage').text("Something went wrong. Please try again.").addClass('text-danger');
            }
        });
    });
});

function filterProjects(category) {
    // Highlight active button
    $('.btn').removeClass('active');
    event.target.classList.add('active');

    // Filter logic
    if (category === 'all') {
        $('.project-item').show();
    } else {
        $('.project-item').hide();
        $('.project-item[data-category="' + category + '"]').show();
    }
}

// 1. Disable Right-Click
document.addEventListener('contextmenu', (e) => {
    e.preventDefault();
}, false);

// 2. Disable Common Inspect Element Shortcuts
document.addEventListener('keydown', (e) => {
    // Disable F12
    if (e.key === 'F12') {
        e.preventDefault();
    }
    // Disable Ctrl+Shift+I (Inspect) and Ctrl+U (View Source)
    if ((e.ctrlKey && e.shiftKey && e.key === 'I') || (e.ctrlKey && e.key === 'U')) {
        e.preventDefault();
    }
});


// Mobile Navbar Toggle Icon Transition
const navbarToggler = document.getElementById('navbarToggler');
const togglerIcon = document.getElementById('togglerIcon');

navbarToggler.addEventListener('click', () => {
    // If the menu is currently open (will close)
    if (togglerIcon.classList.contains('fa-times')) {
        togglerIcon.classList.replace('fa-times', 'fa-bars');
    } 
    // If the menu is currently closed (will open)
    else {
        togglerIcon.classList.replace('fa-bars', 'fa-times');
    }
});

// Optional: Automatically reset icon if user clicks a link (closes menu)
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        const bsCollapse = new bootstrap.Collapse(document.getElementById('navbarNav'), { toggle: false });
        bsCollapse.hide();
        togglerIcon.classList.replace('fa-times', 'fa-bars');
    });
});

window.addEventListener('load', () => {
    const preloader = document.getElementById('preloader');
    
    // Add the fade-out class to start the transition
    preloader.classList.add('fade-out');
    
    // Remove from DOM after the animation finishes
    setTimeout(() => {
        preloader.style.display = 'none';
    }, 500); // Wait 500ms for the opacity transition to finish
});

// Get the button
const scrollToTopBtn = document.getElementById("scrollToTopBtn");

// Show button when user scrolls down 300px
window.onscroll = function() {
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
        scrollToTopBtn.style.display = "block";
    } else {
        scrollToTopBtn.style.display = "none";
    }
};

// Scroll to top when clicked
scrollToTopBtn.addEventListener("click", () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});