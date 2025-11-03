from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from .models import UserProfile, ExchangeAPIKey

# Unregister padrão
admin.site.unregister(User)

# Inline para editar perfil junto com User
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    fields = ['plan', 'cpf', 'trial_ends_at', 'stripe_customer_id']

# Customizar User Admin para incluir perfil
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'get_plan']
    
    def get_plan(self, obj):
        try:
            return obj.userprofile.plan.upper()
        except:
            return '-'
    get_plan.short_description = 'Plano'

admin.site.register(User, UserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 
        'user_email_display', 
        'plan', 
        'payment_status_display', 
        'total_bots_display',
        'monthly_price_display',
        'trial_ends_at', 
        'created_at'
    ]
    list_filter = ['plan', 'created_at', 'user__is_active']
    search_fields = ['user__email', 'user__username', 'cpf']
    
    def payment_status_display(self, obj):
        """Mostrar status de pagamento"""
        if obj.plan == 'free':
            return '✅ FREE'
        elif obj.plan in ['pro', 'premium']:
            # Se tem plano pago mas não tem stripe_customer_id = não pagou ainda
            if not obj.stripe_customer_id:
                return '⏳ Pagamento Pendente'
            else:
                return f'✅ {obj.plan.upper()}'
        return obj.plan.upper()
    payment_status_display.short_description = 'Status Pagamento'
    
    def total_bots_display(self, obj):
        """Mostrar total de bots (base + extras)"""
        base = obj.get_plan_limits()['max_bots']
        if obj.extra_bots > 0:
            return f"{base} ({obj.extra_bots} extras)"
        return str(base)
    total_bots_display.short_description = 'Total Bots'
    
    def monthly_price_display(self, obj):
        """Mostrar preço mensal"""
        if obj.plan == 'free':
            return 'R$ 0,00'
        return f'R$ {obj.monthly_price:.2f}'.replace('.', ',')
    monthly_price_display.short_description = 'Mensalidade'
    
    # CAMPOS EDITÁVEIS (incluindo PLANO e BOTS EXTRAS!)
    fieldsets = [
        ('Informações Básicas', {
            'fields': ['user', 'plan', 'cpf', 'trial_ends_at', 'stripe_customer_id']
        }),
        ('🤖 BOTS EXTRAS - ADICIONAR AQUI!', {
            'fields': ['extra_bots_info', 'extra_bots', 'monthly_price_readonly'],
            'classes': ['wide'],
            'description': '⚠️ O CAMPO "EXTRA BOTS" ESTÁ LOGO ABAIXO DA TABELA AZUL!'
        }),
        ('Datas', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]
    
    readonly_fields = [
        'created_at', 
        'updated_at',
        'extra_bots_info',
        'monthly_price_readonly'
    ]
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)
    
    def user_email_display(self, obj):
        """Mostrar email do usuário"""
        return obj.user.email
    user_email_display.short_description = 'Email'
    
    def extra_bots_info(self, obj):
        """Instruções sobre bots extras"""
        base_bots = {
            'free': 1,
            'pro': 3,
            'premium': 10
        }.get(obj.plan, 0)
        
        base_prices = {
            'pro': 29.90,
            'premium': 99.99
        }
        
        # Preço por bot extra: R$ 9,90 FIXO
        PRICE_PER_BOT = 9.90
        
        # Mínimo por plano
        min_bots = {
            'pro': 2,
            'premium': 5
        }.get(obj.plan, 5)
        
        total_bots = base_bots + obj.extra_bots
        base_price = base_prices.get(obj.plan, 0)
        
        # Tabelas diferentes por plano
        if obj.plan == 'pro':
            table_rows = f"""
                <tr>
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">0 (base)</td>
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">R$ 0,00</td>
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;"><strong>R$ 29,90</strong></td>
                </tr>
                <tr style="background: #f9f9f9;">
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">2 bots</td>
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">R$ 19,80</td>
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;"><strong>R$ 49,70</strong></td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">5 bots</td>
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">R$ 49,50</td>
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;"><strong>R$ 79,40</strong></td>
                </tr>
                <tr style="background: #f9f9f9;">
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">10 bots</td>
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">R$ 99,00</td>
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;"><strong>R$ 128,90</strong></td>
                </tr>
            """
        else:  # premium
            table_rows = f"""
                <tr>
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">0 (base)</td>
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">R$ 0,00</td>
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;"><strong>R$ 99,99</strong></td>
                </tr>
                <tr style="background: #f9f9f9;">
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">5 bots</td>
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">R$ 49,50</td>
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;"><strong>R$ 149,49</strong></td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">10 bots</td>
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">R$ 99,00</td>
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;"><strong>R$ 198,99</strong></td>
                </tr>
                <tr style="background: #f9f9f9;">
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">20 bots</td>
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">R$ 198,00</td>
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;"><strong>R$ 297,99</strong></td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">50 bots</td>
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;">R$ 495,00</td>
                    <td style="padding: 8px; border: 1px solid #ccc; text-align: center;"><strong>R$ 594,99</strong></td>
                </tr>
            """
        
        info_html = f"""
        <div style="background: #f0f8ff; padding: 15px; border-radius: 5px; border: 2px solid #2196F3; margin: 10px 0;">
            <h3 style="margin-top: 0; color: #1976D2;">💡 Sistema de Bots Extras</h3>
            
            <p><strong>Plano {obj.plan.upper()}:</strong> {base_bots} bots inclusos (R$ {base_price:.2f}/mês)</p>
            <p><strong>Bots Extras Atuais:</strong> {obj.extra_bots}</p>
            <p style="font-size: 18px;"><strong>Total de Bots:</strong> <span style="color: #2196F3;">{total_bots}</span></p>
            
            <div style="background: #fff3cd; padding: 15px; border-radius: 5px; border: 3px solid #ff9800; margin: 15px 0;">
                <p style="font-size: 16px; font-weight: bold; color: #e65100; margin: 0;">
                    ⚠️ O CAMPO "EXTRA BOTS" ESTÁ LOGO ABAIXO DESTA TABELA! ⬇️⬇️⬇️
                </p>
            </div>
            
            <hr style="border: 1px solid #ddd;">
            
            <h4>📋 Regras para Adicionar Bots:</h4>
            <ul>
                <li>✅ <strong>Preço por bot extra:</strong> R$ 9,90 (fixo)</li>
                <li>✅ <strong>Múltiplos de {min_bots}:</strong> Apenas {min_bots}, {min_bots*2}, {min_bots*3}, {min_bots*4}...</li>
                <li>✅ <strong>Máximo:</strong> 100 bots extras (total 113 bots PRO ou 110 PREMIUM)</li>
                <li>✅ <strong>Exemplo {min_bots} bots:</strong> + R$ {PRICE_PER_BOT * min_bots:.2f}/mês</li>
            </ul>
            
            <div style="background: #ffebee; padding: 10px; border-radius: 3px; border-left: 4px solid #f44336; margin: 10px 0;">
                <p style="margin: 0; color: #c62828;">
                    <strong>⚠️ ATENÇÃO:</strong><br>
                    • PRO: Digite apenas 2, 4, 6, 8, 10, 12...<br>
                    • PREMIUM: Digite apenas 5, 10, 15, 20, 25...<br>
                    • Sistema arredonda automaticamente se digitar errado
                </p>
            </div>
            
            <h4>💰 Tabela de Preços {obj.plan.upper()}:</h4>
            <table style="border-collapse: collapse; width: 100%; margin-top: 10px;">
                <tr style="background: #2196F3; color: white;">
                    <th style="padding: 8px; border: 1px solid #1976D2;">Bots Extras</th>
                    <th style="padding: 8px; border: 1px solid #1976D2;">Custo Extra/mês</th>
                    <th style="padding: 8px; border: 1px solid #1976D2;">Total {obj.plan.upper()}</th>
                </tr>
                {table_rows}
            </table>
            
            <p style="margin-top: 15px; padding: 10px; background: #e8f5e9; border-radius: 3px; border-left: 4px solid #4caf50;">
                <strong>💡 Dica:</strong> Digite a quantidade total de bots extras e clique em "Salvar". O preço mensal será recalculado automaticamente!
            </p>
        </div>
        """
        PRICE_PER_BOT = 9.90
        return mark_safe(info_html)
    extra_bots_info.short_description = ''
    
    def monthly_price_readonly(self, obj):
        """Mostrar preço calculado"""
        price = obj.calculate_monthly_price()
        html = f"""
        <div style="background: #e8f5e9; padding: 15px; border-radius: 5px; border-left: 5px solid #4CAF50;">
            <strong style="font-size: 20px; color: #2E7D32;">R$ {price:.2f}</strong>
            <p style="margin: 5px 0 0 0; color: #666; font-size: 12px;">
                ✅ Calculado automaticamente ao salvar
            </p>
        </div>
        """
        return mark_safe(html)
    monthly_price_readonly.short_description = 'Preço Mensal'
    
    def save_model(self, request, obj, form, change):
        """Validar bots extras antes de salvar"""
        from django.contrib import messages
        
        # Múltiplos por plano
        multiples = {
            'pro': 2,      # Apenas 0, 2, 4, 6, 8, 10...
            'premium': 5   # Apenas 0, 5, 10, 15, 20...
        }
        
        multiple = multiples.get(obj.plan, 1)
        
        # Validar se é múltiplo correto
        if obj.extra_bots > 0:
            if obj.extra_bots % multiple != 0:
                messages.error(
                    request,
                    f'❌ Plano {obj.plan.upper()}: Bots extras devem ser múltiplos de {multiple}! '
                    f'Valores válidos: {multiple}, {multiple*2}, {multiple*3}, {multiple*4}... Você digitou: {obj.extra_bots}'
                )
                # Arredondar para múltiplo mais próximo
                obj.extra_bots = (obj.extra_bots // multiple) * multiple
                messages.warning(
                    request,
                    f'⚠️ Ajustado automaticamente para: {obj.extra_bots} bots'
                )
        
        # Validar máximo razoável (prevenir infinito)
        MAX_EXTRA_BOTS = 100
        if obj.extra_bots > MAX_EXTRA_BOTS:
            messages.error(
                request,
                f'❌ Máximo de {MAX_EXTRA_BOTS} bots extras! Para mais, crie nova assinatura.'
            )
            obj.extra_bots = MAX_EXTRA_BOTS
        
        super().save_model(request, obj, form, change)
    
    # Ações em massa para alterar planos rapidamente
    actions = ['upgrade_to_pro', 'upgrade_to_premium', 'downgrade_to_free', 'delete_user_and_profile']
    
    def delete_user_and_profile(self, request, queryset):
        """Deletar perfil E usuário (libera email)"""
        count = 0
        for profile in queryset:
            user_email = profile.user.email
            user = profile.user
            profile.delete()  # Deleta perfil
            try:
                user.delete()  # Deleta user (libera email)
                count += 1
            except:
                pass
        self.message_user(request, f'{count} usuário(s) deletado(s) completamente (email liberado)')
    delete_user_and_profile.short_description = '🗑️ Deletar usuário completamente (libera email)'
    
    def is_trial_expired_display(self, obj):
        """Mostrar se trial expirou"""
        if obj.plan == 'free' and obj.trial_ends_at:
            from django.utils import timezone
            if timezone.now() > obj.trial_ends_at:
                return '🔴 Expirado'
            return '🟢 Ativo'
        return '-'
    is_trial_expired_display.short_description = 'Status Trial'
    
    # Ações em massa
    def upgrade_to_pro(self, request, queryset):
        count = queryset.update(plan='pro', trial_ends_at=None)
        self.message_user(request, f'{count} usuário(s) atualizado(s) para PRO')
    upgrade_to_pro.short_description = '⬆️ Upgrade para PRO'
    
    def upgrade_to_premium(self, request, queryset):
        count = queryset.update(plan='premium', trial_ends_at=None)
        self.message_user(request, f'{count} usuário(s) atualizado(s) para PREMIUM')
    upgrade_to_premium.short_description = '⬆️ Upgrade para PREMIUM'
    
    def downgrade_to_free(self, request, queryset):
        from django.utils import timezone
        from datetime import timedelta
        for profile in queryset:
            profile.plan = 'free'
            profile.trial_ends_at = timezone.now() + timedelta(days=7)
            profile.save()
        self.message_user(request, f'{queryset.count()} usuário(s) revertido(s) para FREE (7 dias trial)')
    downgrade_to_free.short_description = '⬇️ Reverter para FREE'

@admin.register(ExchangeAPIKey)
class ExchangeAPIKeyAdmin(admin.ModelAdmin):
    list_display = ['user', 'exchange', 'is_testnet', 'is_active', 'created_at', 'masked_key']
    list_filter = ['exchange', 'is_testnet', 'is_active']
    search_fields = ['user__email']
    readonly_fields = ['api_key_encrypted', 'secret_key_encrypted', 'passphrase_encrypted', 'created_at']
    
    # Campos editáveis
    fields = [
        'user',
        'exchange',
        'is_testnet',  # ← EDITÁVEL! Pode mudar Testnet/Produção
        'is_active',
        'api_key_encrypted',
        'secret_key_encrypted',
        'passphrase_encrypted',
        'created_at'
    ]
    
    def masked_key(self, obj):
        """Mostrar chave mascarada"""
        key = obj.api_key
        return f"***{key[-4:]}"
    masked_key.short_description = 'API Key'
