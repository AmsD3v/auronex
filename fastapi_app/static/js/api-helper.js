/**
 * Helper para chamadas de API com autenticação
 * Pega token do cookie e envia no header
 */

// Função para pegar cookie
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Função para fazer fetch autenticado
async function authenticatedFetch(url, options = {}) {
    // Pegar token do cookie
    let token = getCookie('access_token');
    
    if (!token) {
        console.error('❌ Token não encontrado no cookie!');
        console.log('Cookies:', document.cookie);
        throw new Error('Não autenticado. Faça login novamente.');
    }
    
    // Limpar token (remover encodings e aspas!)
    token = decodeURIComponent(token);
    token = token.replace('Bearer%20', '').replace('Bearer ', '').trim();
    token = token.replace(/"/g, '');  // Remover aspas
    token = token.replace(/'/g, '');  // Remover aspas simples
    
    console.log('✅ Token limpo:', token.substring(0, 30) + '...');
    
    // Adicionar Authorization header
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
        'Authorization': `Bearer ${token}`
    };
    
    console.log('📤 Fazendo request para:', url);
    
    // Fazer requisição
    const response = await fetch(url, {
        ...options,
        headers: headers,
        credentials: 'include'
    });
    
    console.log('📥 Resposta:', response.status, response.statusText);
    
    return response;
}

// Exportar para uso global
window.authenticatedFetch = authenticatedFetch;
window.getCookie = getCookie;

