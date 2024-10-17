document.addEventListener("DOMContentLoaded", function() {
    const emailForm = document.querySelector('form[action="/reset_password"]');
    const passwordForm = document.querySelector('form[action^="/reset/"]');

    if (emailForm) {
        emailForm.addEventListener("submit", function(event) {
            const emailInput = emailForm.querySelector('input[name="email"]');
            const email = emailInput.value.trim();

            if (!validateEmail(email)) {
                event.preventDefault();
                showValidationError(emailInput, "Invalid email address.");
            }
        });
    }

    if (passwordForm) {
        passwordForm.addEventListener("submit", function(event) {
            const passwordInput = passwordForm.querySelector('input[name="password"]');
            const password = passwordInput.value.trim();

            if (!validatePassword(password)) {
                event.preventDefault();
                showValidationError(passwordInput, "Password must be at least 8 characters long and include a number.");
            }
        });
    }

    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    function validatePassword(password) {
        return password.length >= 8 && /\d/.test(password);
    }

    function showValidationError(inputElement, message) {
        const error = document.createElement("div");
        error.className = "error";
        error.textContent = message;
        inputElement.parentElement.appendChild(error);

        setTimeout(() => {
            error.remove();
        }, 5000);
    }
});
