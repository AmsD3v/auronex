/**
 * Toggle para mostrar/esconder senha
 * Adiciona ícone de olho em todos os inputs de senha
 */

document.addEventListener('DOMContentLoaded', function() {
    // Encontrar todos os inputs de senha
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    
    passwordInputs.forEach(input => {
        // Criar wrapper se não existir
        if (!input.parentElement.classList.contains('password-toggle-wrapper')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'password-toggle-wrapper position-relative';
            
            input.parentNode.insertBefore(wrapper, input);
            wrapper.appendChild(input);
            
            // Criar botão de toggle
            const toggleBtn = document.createElement('button');
            toggleBtn.type = 'button';
            toggleBtn.className = 'btn btn-sm position-absolute top-50 end-0 translate-middle-y me-2';
            toggleBtn.style.background = 'none';
            toggleBtn.style.border = 'none';
            toggleBtn.style.zIndex = '10';
            toggleBtn.innerHTML = '<i class="fas fa-eye text-muted"></i>';
            
            toggleBtn.addEventListener('click', function() {
                if (input.type === 'password') {
                    input.type = 'text';
                    toggleBtn.innerHTML = '<i class="fas fa-eye-slash text-primary"></i>';
                } else {
                    input.type = 'password';
                    toggleBtn.innerHTML = '<i class="fas fa-eye text-muted"></i>';
                }
            });
            
            wrapper.appendChild(toggleBtn);
        }
    });
});

