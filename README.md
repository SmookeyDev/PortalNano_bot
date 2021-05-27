# [PortalNano_bot](https://t.me/PortalNano_bot)
## Descrição
Código fonte do bot do Portal Nano.
> O Portal Nano tem como missão informar, instruir e apresentar a Nano para todos. Trazer o melhor conteúdo sobre essa tecnologia e demais novidades sobre o mundo das criptomoedas. Nano é a Luz!

Considere [visitar o Portal](http://portalnano.com.br) ou [conversar com o bot pelo Telegram](https://t.me/PortalNano_bot).

<hr>

## Criando um ambiente de testes
### 1. Crie um bot no Telegram
Mais informações em:
https://core.telegram.org/bots/api

### 2. Clone o repositório e instale as dependências
```
git clone https://github.com/SmookeyDev/PortalNano_bot.git
pip3 install -r requirements.txt
```
### 3. Crie um arquivo .env
Crie um arquivo com nome `.env` na raíz do projeto e adicione as variáveis de ambiente.

**Exemplo:**
```
TOKEN=8740950923:hJqFyRxHpD-fYmXhYwCkMeBpElPgTuDiDvS
SUDOS=1234567890 1111111111
MAINTAINERS=1234567890 0987654321
BOT_USERNAME=@PortalNano_bot
```

Onde:
- `TOKEN` é o token da API do Telegram
- `SUDOS` são os `chat_id` dos usuários administrativos do bot
- `MAINTAINERS` são os `chat_id` dos desenvolvedores que desejam receber sugestões / elogios
- `BOT_USERNAME` é o `username` do bot no Telegram

### 4. Execute o main.py
```
python3 main.py
```
Agora envie mensagens para o bot para testar se está funcionando.