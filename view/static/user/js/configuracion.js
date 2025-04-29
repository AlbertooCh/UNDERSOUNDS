document.getElementById('avatarInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (!file) return;

    // Validaciones
    if (file.size > 2 * 1024 * 1024) {
        alert('El archivo es demasiado grande. Máximo 2MB permitidos.');
        return;
    }

    if (!file.type.match('image.*')) {
        alert('Por favor selecciona un archivo de imagen (JPG, PNG)');
        return;
    }

    // Previsualización
    const reader = new FileReader();
    reader.onload = function(event) {
        const preview = document.getElementById('avatarPreview');
        preview.src = event.target.result;
        preview.style.transform = 'scale(1.05)';
        setTimeout(() => preview.style.transform = 'scale(1)', 300);
    };
    reader.readAsDataURL(file);

    // Subida al servidor
    const formData = new FormData();
    formData.append('avatar', file);
    formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');

    fetch('{% url "upload_avatar" %}', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) throw new Error('Error en la subida');
        return response.json();
    })
    .then(data => {
        if (!data.success) throw new Error(data.message || 'Error al guardar');
        alert('Avatar actualizado correctamente');
    })
    .catch(error => {
        console.error('Error:', error);
        alert(error.message);
    });
});

    // Función para toggle de contraseña
    function setupPasswordToggle(fieldId, buttonId, iconId) {
        const button = document.getElementById(buttonId);
        const field = document.getElementById(fieldId);
        const icon = document.getElementById(iconId);

        button.addEventListener('click', function(e) {
            e.preventDefault();
            const isPassword = field.type === 'password';
            field.type = isPassword ? 'text' : 'password';
            icon.src = isPassword ?
                "{% static 'images/viendo_oculto.png' %}" :
                "{% static 'images/ver_oculto.png' %}";
            icon.alt = isPassword ? "Ocultar contraseña" : "Mostrar contraseña";
        });
    }

    // Configurar toggles para cada campo
    setupPasswordToggle('current_password', 'toggle-current-password', 'current-password-icon');
    setupPasswordToggle('new_password', 'toggle-new-password', 'new-password-icon');
    setupPasswordToggle('confirm_password', 'toggle-confirm-password', 'confirm-password-icon');

    // Validación de contraseñas
    document.getElementById('passwordForm').addEventListener('submit', function(e) {
        const newPassword = document.getElementById('new_password').value;
        const confirmPassword = document.getElementById('confirm_password').value;
        const errorElement = document.getElementById('password-error');

        if (newPassword !== confirmPassword) {
            e.preventDefault();
            errorElement.style.display = 'block';
            document.getElementById('new_password').classList.add('error-border');
            document.getElementById('confirm_password').classList.add('error-border');
            return false;
        }
        return true;
    });

    // Validación en tiempo real
    document.getElementById('confirm_password').addEventListener('input', function() {
        const newPassword = document.getElementById('new_password').value;
        const confirmPassword = this.value;
        const errorElement = document.getElementById('password-error');

        if (confirmPassword && newPassword !== confirmPassword) {
            errorElement.style.display = 'block';
            document.getElementById('new_password').classList.add('error-border');
            this.classList.add('error-border');
        } else {
            errorElement.style.display = 'none';
            document.getElementById('new_password').classList.remove('error-border');
            this.classList.remove('error-border');
        }
    });

    // Manejo del formulario de perfil con AJAX
    document.getElementById('profileForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            }
        }).then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Perfil actualizado correctamente');
                if (data.new_username) {
                    // Recargar si cambió el username (puede afectar la sesión)
                    window.location.reload();
                }
            } else {
                alert(data.message || 'Error al actualizar el perfil');
            }
        });
    });

    // Manejo de eliminación/desactivación de cuenta
    document.getElementById('delete-btn').addEventListener('click', function() {
        if (confirm('¿Eliminar cuenta permanentemente? Esta acción no se puede deshacer.')) {
            fetch('{% url "delete_account" %}', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}'
                }
            }).then(() => window.location.href = '/');
        }
    });

    document.getElementById('deactivate-btn').addEventListener('click', function() {
        if (confirm('¿Desactivar tu cuenta temporalmente?')) {
            fetch('{% url "deactivate_account" %}', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}'
                }
            }).then(() => window.location.href = '/');
        }
    });