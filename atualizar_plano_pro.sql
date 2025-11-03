-- Atualizar usuário aisha.rafa137@gmail.com para plano PRO

UPDATE subscriptions 
SET 
    plan = 'pro',
    status = 'active',
    amount = 1.00,
    currency = 'BRL',
    payment_method = 'mercadopago'
WHERE user_id = 61;

-- Verificar
SELECT u.email, s.plan, s.status, s.amount
FROM auth_user u
LEFT JOIN subscriptions s ON s.user_id = u.id
WHERE u.email = 'aisha.rafa137@gmail.com';






