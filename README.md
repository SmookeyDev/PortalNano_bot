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

## 🧐 Sobre `<a name="about"></a>`

O PortalNano_bot surgiu da ideia de levar as noticias do [PortalNano](https://portalnano.com.br/) para a comunidade da [NanoBrasil](https://t.me/NanoBrasil) no Telegram.

## 📲 Comandos `<a name="commands"></a>`

| Comando                                                                                                        | Status |
| -------------------------------------------------------------------------------------------------------------- | ------ |
| /start = Inicia o robô.                                                                                        | ✅     |
| /ajuda = Mostra todos os comandos disponíveis.                                                                 | ✅     |
| /creditos = Mostra os desenvolvedores do bot e um endereço de doação para apoiar-los.                          | ✅     |
| /registrar = Ativa o recebimento de noticias.                                                                  | ✅     |
| /cancelar = Cancela o recebimento de noticias.                                                                 | ✅     |
| /cot [quantidade] = Mostra a atual cotação da NANO.                                                            | ✅     |
| /sugerir [mensagem] = Possibilita nos sugerir uma nova funcionalidade ou noticia.                              | ✅     |
| /rede = Mostra algumas informações da rede da Nano.                                                            | ✅     |
| /me - Envia algumas informações sobre o grupo e/ou usuário.                                                    | ✅     |
| /campanha = Mostra informações sobre a campanha de doação para custear o servidor em que o bot está hospedado. | ✅     |

---

## 📝 Requisitos para rodar ambiente de desenvolvimento `<a name="developmentrequirements"></a>`

- Node.js
- Nodemon
- TypeScript

## 💭 Instalação `<a name="installation"></a>`

1.Clone este repositório usando o seguinte comando:

```terminal
$ git clone https://github.com/SmookeyDev/PortalNano_bot
```

2.Acesse a pasta do projeto em seu terminal:

```terminal
$ cd PortalNano_bot
```

3.Rode o comando de instalação das bibliotecas utilizada no projeto.

```terminal
$ yarn
```

4.Copie o arquivo de configuração de exemplo para um arquivo de configuração real:

```terminal
$ cp .env.example .env
```

5.Troque os valores existentes no arquivo de configuração, os valores são:

- **BOT_TOKEN**: Token do robô que será usado. (Obrigatorio)
- **ADMIN_CHAT**: ID do grupo direcionado para envio das sugestões. (Obrigatorio)
- **ROOTS**: ID das pessoas que terão acesso aos comandos de administrador. (Obrigatorio)
- **DB_URL**: Endereço de conexão para o banco de dados. (Obrigatorio)
- **NANO_WALLET**: Endereço da carteira para doações. (Opcional)

````
6.Inicie o robô rodando os seguintes comando:
```terminal
$ yarn dev
````

## 🔰 Créditos `<a name="credits"></a>`

- [Ícaro Sant&#39;Ana](https://github.com/SmookeyDev)
- [Caio Cristiano](https://github.com/ArTombado)
- [Igor Melo](https://github.com/igorcmelo)
- [João Gabriel](https://github.com/JgBr123)
