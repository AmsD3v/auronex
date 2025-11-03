/**
 * Helper para abrir Streamlit com autenticação automática
 */

function openStreamlitDashboard() {
    const token = localStorage.getItem('access_token');
    if (token) {
        // Abrir Streamlit com token como query param para auto-login
        window.open(`http://localhost:8501?token=${token}`, '_blank');
    } else {
        alert('❌ Sessão expirada. Faça login novamente.');
        window.location.href = '/login';
    }
}





