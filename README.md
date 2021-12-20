<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.imgur.com/5yGxUhW.jpg" alt="Bot logo"></a>
</p>


<div align="center">

[![Status](https://img.shields.io/badge/status-ativo-success.svg)]()
[![Telegram](https://img.shields.io/badge/platform-telegram-blue.svg)](https://t.me/NanoBrasil)
[![GitHub Issues](https://img.shields.io/github/issues/SmookeyDev/PortalNano_bot.svg)](https://github.com/SmookeyDev/PortalNano_bot/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/SmookeyDev/PortalNano_bot.svg)](https://github.com/SmookeyDev/PortalNano_bot/pulls)
</div>

---

## 📝 Tabela de conteúdos

- [Sobre](#about)
- [Comandos](#commands)
- [Requisitos para rodar ambiente de desenvolvimento](#developmentrequirements)
- [Instalação](#installation)
- [Créditos](#credits)

## 🧐 Sobre <a name="about"></a>

O PortalNano_bot surgiu da ideia de levar as noticias do [PortalNano](https://portalnano.com.br/) para a comunidade da [NanoBrasil](https://t.me/NanoBrasil) no Telegram.

## 📲 Comandos <a name="commands"></a>

| Comando  | Status |
| ------------- | ------------- |
| /start = Inicia o robô.  | ✅  |
| /info = Mostra informações do portal.  | ✅  |
| /creditos = Mostra os desenvolvedores do bot e um endereço de doação para apoiar-los.  | ✅  |
| /registrar = Ativa o recebimento de noticias.  | ✅ |
| /cancelar = Cancela o recebimento de noticias.  | ✅  |
| /ultimas = Lista as ultimas 5 noticias lançadas no portal.  | ✅  |
| /cot [quantidade] = Mostra a atual cotação da NANO.  | ✅  |
| /sugerir [mensagem] = Possibilita nos sugerir uma nova funcionalidade ou noticia.  | ✅  |
| /node [endereço] = Mostra algumas estátisticas do node informado ou caso não seja informado, mostrará por padrão o da NanoBrasil.  | ✅  |
| /rede = Mostra algumas informações da rede da Nano.  | ✅  |
| /me - Envia algumas informações sobre o grupo e/ou usuário.  | ✅  |

---

## 📝 Requisitos para rodar ambiente de desenvolvimento <a name="developmentrequirements"></a>

- Docker
- Docker compose
- Node.js

## 💭 Instalação <a name="installation"></a>

1.Clone este repositório usando o seguinte comando:
```terminal
$ git clone -b remake https://github.com/SmookeyDev/PortalNano_bot
```
2.Acesse a pasta do projeto em seu terminal:
```terminal
$ cd PortalNano_bot
```
3.Rode o comando de instalação das bibliotecas utilizada no projeto.
```terminal
$ npm install
```
4.Copie o arquivo de configuração de exemplo para um arquivo de configuração real:
```terminal
$ cp .env.example .env
```
5.Troque os valores existentes no arquivo de configuração, os valores são:
  * **BOT_TOKEN**: Token do robô que será usado. (Obrigatorio)
  * **ADMIN_CHAT**: ID do grupo direcionado para envio das sugestões. (Obrigatorio)
  * **ROOTS**: ID das pessoas que terão acesso aos comandos de administrador. (Obrigatorio)
  * **DB_HOST**: Endereço IPV4 a ser utilizado para conexão do banco de dados. (Opcional)
  * **DB_PORT**: Porta que será usada para o banco de dados. (Opcional)
  * **DB_NAME**: Nome do banco de dados. (Opcional)
  * **DB_USER**: Usuário do banco de dados. (Opcional)
  * **DB_PASS**: Senha do usuário do banco de dados. (Opcional)

6.Inicie o banco de dados rodando o seguinte comando:
```terminal
$ make up
```
7.Inicie o robô rodando o seguinte comando:
```terminal
$ npm start
```

## 🔰 Créditos <a name="credits"></a>

* [Ícaro Sant'Ana](https://github.com/SmookeyDev)
* [Caio Cristiano](https://github.com/ArTombado)
* [Igor Melo](https://github.com/igorcmelo)
* [João Gabriel](https://github.com/JgBr123)