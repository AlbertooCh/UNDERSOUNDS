
        // Función para desplazarse suavemente al inicio
        function scrollToTop() {
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });

            // Efecto de pulsación
            const btn = document.querySelector('.scroll-to-top');
            btn.classList.add('clicked');
            setTimeout(() => btn.classList.remove('clicked'), 300);
        }

        // Mostrar/ocultar botón al hacer scroll
        window.addEventListener('scroll', () => {
            const scrollToTopButton = document.querySelector('.scroll-to-top');
            if (window.scrollY > 300) {
                scrollToTopButton.classList.add('visible');
            } else {
                scrollToTopButton.classList.remove('visible');
            }
        });

        // Mostrar el botón después de 1 segundo si está en parte inferior
        setTimeout(() => {
            if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 100) {
                document.querySelector('.scroll-to-top').classList.add('visible');
            }
        }, 1000);

          // Función para desplazarse suavemente al inicio
        function scrollToTop() {
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });

            // Efecto de pulsación
            const btn = document.querySelector('.scroll-to-top');
            btn.classList.add('clicked');
            setTimeout(() => btn.classList.remove('clicked'), 300);
        }

        // Mostrar/ocultar botón al hacer scroll
        window.addEventListener('scroll', () => {
            const scrollToTopButton = document.querySelector('.scroll-to-top');
            if (window.scrollY > 300) {
                scrollToTopButton.classList.add('visible');
            } else {
                scrollToTopButton.classList.remove('visible');
            }
        });

        // Mostrar el botón después de 1 segundo si está en parte inferior
        setTimeout(() => {
            if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 100) {
                document.querySelector('.scroll-to-top').classList.add('visible');
            }
        }, 1000);