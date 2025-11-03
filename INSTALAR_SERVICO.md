# 🔧 Instalando RoboTrader como Serviço Windows

## ⚠️ **IMPORTANTE:**

Serviço Windows é para **desenvolvimento avançado**. Para produção real, use **SOLUÇÃO 2** (deploy cloud).

## **Passo 1: Instalar dependências**

```bash
pip install pywin32
```

## **Passo 2: Instalar serviço**

```bash
# CMD como Administrador
cd I:\Robo
python install_service.py install
```

## **Passo 3: Iniciar serviço**

```bash
python install_service.py start
```

## **Comandos úteis:**

```bash
# Ver status
python install_service.py status

# Parar
python install_service.py stop

# Remover
python install_service.py remove
```

---

## ⚠️ **LIMITAÇÃO:**

Localhost **NUNCA** será acessível pela internet!
- http://localhost:8001 = Apenas no seu PC
- Outros não conseguem acessar

**Para site real:** Use SOLUÇÃO 2


