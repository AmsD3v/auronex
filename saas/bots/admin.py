from django.contrib import admin
from .models import BotConfiguration, Trade

@admin.register(BotConfiguration)
class BotConfigurationAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'exchange', 'is_active', 'created_at']
    list_filter = ['exchange', 'is_active', 'strategy']
    search_fields = ['user__email', 'name']

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ['user', 'symbol', 'side', 'entry_price', 'profit_loss', 'status', 'entry_time']
    list_filter = ['status', 'side', 'exchange']
    search_fields = ['user__email', 'symbol']
    readonly_fields = ['entry_time', 'exit_time']
