// Script para funcionalidades generales

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

function logout() {
    // Borrar token y usuario de ambos storages por compatibilidad
    try {
        sessionStorage.removeItem('erp_token');
        sessionStorage.removeItem('erp_user');
    } catch(e) {}
    try {
        localStorage.removeItem('erp_token');
        localStorage.removeItem('erp_user');
    } catch(e) {}
    // Redirigir al login
    window.location.href = '/login'; 
}