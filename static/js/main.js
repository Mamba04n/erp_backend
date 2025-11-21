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

async function createRandomOrder() {
    const token = localStorage.getItem('erp_token'); // Recuperar token
    
    const randomProdId = Math.floor(Math.random() * 5) + 1; 
    const orderData = {
        client_id: 1,
        items: [{ product_id: randomProdId, quantity: 1 }]
    };
    
    await fetch(`${API_URL}/orders/`, {
        method: "POST",
        headers: { 
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}` // <--- ESTO ES LA LLAVE MAESTRA
        },
        body: JSON.stringify(orderData)
    });
}