// Confirmación antes de eliminar
    document.querySelectorAll('.action-btn.delete').forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('¿Estás seguro de que quieres eliminar esta canción?')) {
                e.preventDefault();
            }
        });
    });