function showSection(event, sectionId) {
    event.preventDefault();
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(sectionId).classList.add('active');

    document.querySelectorAll('.menu a').forEach(link => {
        link.classList.remove('active');
    });
    event.target.classList.add('active');
}

function enableButton() {
    document.getElementById("actualizarBtn").disabled = false;
}
