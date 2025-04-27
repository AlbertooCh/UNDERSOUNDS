// static/js/dropdown.js

document.addEventListener('DOMContentLoaded', function() {
    // Configuración general para todos los dropdowns
    const dropdownSelectors = ['.profile-dropdown', '.register-dropdown'];

    /**
     * Función unificada para mostrar/ocultar menús desplegables
     * @param {Event} event - Evento del DOM
     * @param {string} dropdownId - ID del dropdown a togglear
     */
    window.toggleDropdown = function(event, dropdownId = 'profileDropdown') {
        event.preventDefault();
        event.stopPropagation();

        const dropdown = document.getElementById(dropdownId);
        if (dropdown) {
            dropdown.classList.toggle("active");

            // Cerrar otros dropdowns excepto el actual
            dropdownSelectors.forEach(selector => {
                document.querySelectorAll(selector).forEach(item => {
                    if (item.id !== dropdownId) {
                        item.classList.remove("active");
                    }
                });
            });
        }
    };

    /**
     * Cierra todos los dropdowns
     */
    function closeAllDropdowns() {
        dropdownSelectors.forEach(selector => {
            document.querySelectorAll(selector).forEach(item => {
                item.classList.remove("active");
            });
        });
    }

    // Cerrar menús al hacer clic fuera
    document.addEventListener('click', function(e) {
        let shouldClose = true;

        // Verificar si el clic fue dentro de algún dropdown
        dropdownSelectors.forEach(selector => {
            if (e.target.closest(selector)) {
                shouldClose = false;
            }
        });

        if (shouldClose) {
            closeAllDropdowns();
        }
    });

    // Cerrar menús al hacer scroll
    window.addEventListener('scroll', closeAllDropdowns);
});