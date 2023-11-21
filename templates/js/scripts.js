window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

    // Activate SimpleLightbox plugin for portfolio items
    new SimpleLightbox({
        elements: '#portfolio a.portfolio-box'
    });

});

    // Espera a que el documento esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Obtiene todas las imágenes con la clase "portfolio-box"
    var portfolioImages = document.querySelectorAll('.portfolio-box');

        // Itera sobre cada imagen
    portfolioImages.forEach(function(image) {
        // Agrega un listener de clic a cada imagen
        image.addEventListener('click', function(event) {
            // Evita el comportamiento predeterminado del enlace
            event.preventDefault();
                // Obtiene el destino del enlace desde el atributo "data-target"
            var target = image.getAttribute('data-target');

            // Redirecciona a la página HTML correspondiente
            window.location.href = target;
        });
    });
});
