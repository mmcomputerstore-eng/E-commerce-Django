/**
 * User Authentication (Login & Modal Registration) Handler
 * Written in standard Vanilla JavaScript (ES6+)
 */

document.addEventListener('DOMContentLoaded', function () {
    // ----------------------------------------------------
    // 1. Modal Registration Handler
    // ----------------------------------------------------
    const registerForm = document.getElementById('modal-register-form');
    const registerAlertBox = document.getElementById('register-alert-box');
    const registerBtn = document.getElementById('modal-register-btn');

    if (registerForm) {
        registerForm.addEventListener('submit', async function (e) {
            e.preventDefault();

            if (registerAlertBox) registerAlertBox.innerHTML = '';
            const originalBtnHtml = registerBtn.innerHTML;
            registerBtn.disabled = true;
            registerBtn.innerHTML = '<span>Registering...</span> <i class="icon-refresh"></i>';

            const formData = new FormData(registerForm);
            formData.append('ajax', 'true');

            try {
                const response = await fetch(registerForm.action, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: formData
                });

                const data = await response.json();
                registerBtn.disabled = false;
                registerBtn.innerHTML = originalBtnHtml;

                if (response.ok && data.status === 'success') {
                    if (registerAlertBox) {
                        registerAlertBox.innerHTML = `
                            <div class="alert alert-success alert-dismissible fade show" role="alert">
                                <strong>Success!</strong> ${data.message}
                            </div>
                        `;
                    }
                    registerForm.reset();

                    setTimeout(function () {
                        window.location.reload();
                    }, 1200);
                } else {
                    displayErrors(registerAlertBox, data.errors);
                }
            } catch (error) {
                registerBtn.disabled = false;
                registerBtn.innerHTML = originalBtnHtml;
                displayErrors(registerAlertBox, ['An unexpected error occurred. Please try again.']);
            }
        });
    }

    // ----------------------------------------------------
    // 2. Modal Login Handler
    // ----------------------------------------------------
    const loginForm = document.getElementById('modal-login-form');
    const loginAlertBox = document.getElementById('login-alert-box');
    const loginBtn = document.getElementById('modal-login-btn');

    if (loginForm) {
        loginForm.addEventListener('submit', async function (e) {
            e.preventDefault();

            if (loginAlertBox) loginAlertBox.innerHTML = '';
            const originalBtnHtml = loginBtn.innerHTML;
            loginBtn.disabled = true;
            loginBtn.innerHTML = '<span>Logging in...</span> <i class="icon-refresh"></i>';

            const formData = new FormData(loginForm);
            formData.append('ajax', 'true');

            try {
                const response = await fetch(loginForm.action, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: formData
                });

                const data = await response.json();
                loginBtn.disabled = false;
                loginBtn.innerHTML = originalBtnHtml;

                if (response.ok && data.status === 'success') {
                    if (loginAlertBox) {
                        loginAlertBox.innerHTML = `
                            <div class="alert alert-success alert-dismissible fade show" role="alert">
                                <strong>Success!</strong> ${data.message}
                            </div>
                        `;
                    }
                    loginForm.reset();

                    setTimeout(function () {
                        window.location.reload();
                    }, 1000);
                } else {
                    displayErrors(loginAlertBox, data.errors);
                }
            } catch (error) {
                loginBtn.disabled = false;
                loginBtn.innerHTML = originalBtnHtml;
                displayErrors(loginAlertBox, ['An unexpected error occurred. Please try again.']);
            }
        });
    }

    /**
     * Helper function to render error messages inside the target alert box
     */
    function displayErrors(container, errors) {
        if (!container) return;

        let errorItems = '';

        if (Array.isArray(errors)) {
            errorItems = errors.map(err => `<li>${err}</li>`).join('');
        } else if (typeof errors === 'object' && errors !== null) {
            for (const key in errors) {
                if (Object.prototype.hasOwnProperty.call(errors, key)) {
                    const errList = errors[key];
                    if (Array.isArray(errList)) {
                        errorItems += errList.map(e => `<li>${e}</li>`).join('');
                    } else {
                        errorItems += `<li>${errList}</li>`;
                    }
                }
            }
        } else {
            errorItems = `<li>${errors || 'Validation error occurred.'}</li>`;
        }

        container.innerHTML = `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                <strong>Please correct the following:</strong>
                <ul class="mb-0 mt-1 pl-3" style="list-style-type: disc;">
                    ${errorItems}
                </ul>
            </div>
        `;
    }
});
