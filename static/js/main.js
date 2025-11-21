// Script para manejar la interacción del menú
document.querySelectorAll('.menu-item').forEach(item => {
    item.addEventListener('click', function() {
        document.querySelectorAll('.menu-item').forEach(i => {
            i.classList.remove('active');
        });
        this.classList.add('active');
        
        // Cambiar el título de la página según la selección
        const pageTitle = this.querySelector('span').textContent;
        document.querySelector('.page-title').textContent = pageTitle;
    });
});
