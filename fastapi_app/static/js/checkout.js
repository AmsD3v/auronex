/**
 * Checkout - Integração com MercadoPago e Stripe
 */

let currentPaymentMethod = 'pix';
let currentPlan = 'pro';

// Pegar plano da URL
const urlParams = new URLSearchParams(window.location.search);
currentPlan = urlParams.get('plan') || 'pro';

function selectPaymentMethod(method) {
    currentPaymentMethod = method;
    
    // Atualizar visual dos cards
    document.getElementById('card-method').classList.remove('active');
    document.getElementById('pix-method').classList.remove('active');
    document.getElementById('card-method').style.borderColor = '#dee2e6';
    document.getElementById('pix-method').style.borderColor = '#dee2e6';
    
    if (method === 'credit-card') {
        document.getElementById('card-method').classList.add('active');
        document.getElementById('card-method').style.borderColor = '#667eea';
        document.getElementById('credit-card-form').style.display = 'block';
        document.getElementById('pix-form').style.display = 'none';
    } else if (method === 'pix') {
        document.getElementById('pix-method').classList.add('active');
        document.getElementById('pix-method').style.borderColor = '#28a745';
        document.getElementById('credit-card-form').style.display = 'none';
        document.getElementById('pix-form').style.display = 'block';
    }
}

// ========================================
// MERCADOPAGO - PIX
// ========================================

async function generatePix() {
    const btn = document.getElementById('generate-pix-btn');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Gerando...';
    
    try {
        // Pegar token OU pending_user_id
        let token = document.cookie.split('; ').find(row => row.startsWith('access_token='))?.split('=')[1]?.replace('Bearer%20', '');
        const pending = document.cookie.split('; ').find(row => row.startsWith('pending_user_id='))?.split('=')[1];
        
        // Se não tem token MAS tem pending, precisa criar sessão temporária
        if (!token && pending) {
            alert('Por favor, aguarde enquanto processamos seu pagamento...');
            // Por enquanto, solicita que escolha FREE primeiro ou faça login
            // Em produção, você criaria uma sessão temporária aqui
            return;
        }
        
        if (!token && !pending) {
            alert('Você precisa estar logado!');
            window.location.href = '/login';
            return;
        }
        
        // Criar pagamento via MercadoPago
        const response = await fetch('/api/payments/mercadopago/create-payment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                plan: currentPlan,
                payment_method: 'mercadopago_pix'
            })
        });
        
        if (!response.ok) {
            throw new Error('Erro ao criar pagamento PIX');
        }
        
        const data = await response.json();
        
        // Mostrar QR Code
        document.getElementById('generate-pix-btn').style.display = 'none';
        document.getElementById('pix-qrcode-area').style.display = 'block';
        
        // Atualizar código PIX
        if (data.pix_copy_paste) {
            document.getElementById('pix-code').value = data.pix_copy_paste;
        }
        
        // Iniciar polling para verificar pagamento
        startPixPolling(data.payment_id);
        
    } catch (error) {
        alert('Erro ao gerar PIX: ' + error.message + '\n\nVerifique se instalou o MercadoPago SDK:\npip install mercadopago');
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-qrcode"></i> Gerar QR Code PIX';
    }
}

async function startPixPolling(paymentId) {
    // Verificar status a cada 3 segundos
    const interval = setInterval(async () => {
        try {
            const token = document.cookie.split('; ').find(row => row.startsWith('access_token='))?.split('=')[1]?.replace('Bearer%20', '');
            
            const response = await fetch(`http://localhost:8001/api/payments/payment-history`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            const payments = await response.json();
            const currentPayment = payments.find(p => p.id === paymentId);
            
            if (currentPayment && currentPayment.status === 'approved') {
                clearInterval(interval);
                alert('PIX aprovado! Bem-vindo ao RoboTrader!');
                window.location.href = '/dashboard';
            }
        } catch (error) {
            console.error('Erro ao verificar pagamento:', error);
        }
    }, 3000);
    
    // Parar polling após 10 minutos
    setTimeout(() => {
        clearInterval(interval);
    }, 600000);
}

function copyPixCode() {
    const pixCode = document.getElementById('pix-code');
    pixCode.select();
    pixCode.setSelectionRange(0, 99999); // Mobile
    document.execCommand('copy');
    
    // Feedback visual
    const btn = event.target.closest('button');
    const originalHTML = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-check"></i> Copiado!';
    btn.classList.remove('btn-outline-primary');
    btn.classList.add('btn-success');
    
    setTimeout(function() {
        btn.innerHTML = originalHTML;
        btn.classList.remove('btn-success');
        btn.classList.add('btn-outline-primary');
    }, 2000);
}

// ========================================
// STRIPE - CARTÃO DE CRÉDITO
// ========================================

async function processStripePayment(e) {
    e.preventDefault();
    
    const btn = document.getElementById('card-submit-btn');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Processando...';
    
    try {
        // Pegar token
        const token = document.cookie.split('; ').find(row => row.startsWith('access_token='))?.split('=')[1]?.replace('Bearer%20', '');
        
        if (!token) {
            alert('Você precisa estar logado!');
            window.location.href = '/login';
            return;
        }
        
        // Criar checkout session do Stripe
        const response = await fetch('http://localhost:8001/api/payments/stripe/create-checkout-session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                plan: currentPlan,
                payment_method: 'stripe'
            })
        });
        
        if (!response.ok) {
            throw new Error('Erro ao criar checkout Stripe');
        }
        
        const data = await response.json();
        
        // Redirecionar para checkout do Stripe
        window.location.href = data.checkout_url;
        
    } catch (error) {
        alert('Erro ao processar pagamento: ' + error.message + '\n\nVerifique se instalou o Stripe SDK:\npip install stripe');
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-lock"></i> Finalizar com Cartão';
    }
}

// Vincular formulário de cartão
document.getElementById('credit-card-form')?.addEventListener('submit', processStripePayment);

// Formatação automática do número do cartão
document.getElementById('cardNumber')?.addEventListener('input', function(e) {
    let value = e.target.value.replace(/\s/g, '');
    let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
    e.target.value = formattedValue.slice(0, 19); // Máximo 16 dígitos + 3 espaços
});

// Formatação automática da validade
document.getElementById('cardExpiry')?.addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length >= 2) {
        value = value.slice(0,2) + '/' + value.slice(2,4);
    }
    e.target.value = value;
});

// Limite CVV
document.getElementById('cardCVC')?.addEventListener('input', function(e) {
    e.target.value = e.target.value.replace(/\D/g, '').slice(0, 4);
});



