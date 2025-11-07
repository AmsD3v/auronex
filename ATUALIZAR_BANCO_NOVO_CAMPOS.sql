-- ====================================
-- ADICIONAR NOVOS CAMPOS AO BANCO
-- Executar: sqlite3 db.sqlite3 < ATUALIZAR_BANCO_NOVO_CAMPOS.sql
-- ====================================

-- Adicionar is_testnet (se não existir)
ALTER TABLE bot_configurations ADD COLUMN is_testnet BOOLEAN DEFAULT 1;

-- Adicionar analysis_interval (velocidade)
ALTER TABLE bot_configurations ADD COLUMN analysis_interval INTEGER DEFAULT 5;

-- Adicionar hunter_mode (modo caçador)
ALTER TABLE bot_configurations ADD COLUMN hunter_mode BOOLEAN DEFAULT 0;

-- Ver estrutura
.schema bot_configurations


