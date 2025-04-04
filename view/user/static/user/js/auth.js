// Función para mostrar/ocultar contraseña (compatible con ambos formularios)
function togglePasswordVisibility(inputId, icon) {
    const input = document.getElementById(inputId);
    if (!input) return; // Si no existe el elemento, salir

    if (input.type === "password") {
        input.type = "text";
        icon.src = icon.src.replace("ver_oculto.png", "viendo_oculto.png");
    } else {
        input.type = "password";
        icon.src = icon.src.replace("viendo_oculto.png", "ver_oculto.png");
    }
}

// Configuración de eventos para formularios
function setupFormValidation(formId, password1Id, password2Id, errorId) {
    const form = document.getElementById(formId);
    if (!form) return; // Si no existe el formulario, salir

    // Validación al enviar
    form.addEventListener('submit', function(e) {
        const password1 = document.getElementById(password1Id).value;
        const password2 = document.getElementById(password2Id).value;
        const errorElement = document.getElementById(errorId);

        if (password1 !== password2) {
            e.preventDefault();
            errorElement.style.display = 'block';
            document.getElementById(password2Id).style.borderColor = '#ff4d4d';
        }
    });

    // Validación en tiempo real
    const password2Field = document.getElementById(password2Id);
    if (password2Field) {
        password2Field.addEventListener('input', function() {
            const password1 = document.getElementById(password1Id).value;
            const password2 = this.value;
            const errorElement = document.getElementById(errorId);

            if (password2 && password1 !== password2) {
                errorElement.style.display = 'block';
                this.style.borderColor = '#ff4d4d';
            } else {
                errorElement.style.display = 'none';
                this.style.borderColor = '#ddd';
            }
        });
    }
}

// Configuración de eventos para botones de mostrar contraseña
document.querySelectorAll('.toggle-password').forEach(icon => {
    const inputId = icon.getAttribute('data-target');
    icon.addEventListener('click', function() {
        togglePasswordVisibility(inputId, icon);
    });
});

// Inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Configuración para register.html
    setupFormValidation('registerForm', 'password1', 'password2', 'passwordError');

    // Configuración para artist_register.html
    setupFormValidation('artistRegisterForm', 'password1', 'password2', 'passwordError');
});