# 🔍 EMAIL TRACE

**FERRAMENTA OSINT QUE DESCOBRE EM QUAIS SITES UM E-MAIL TEM CONTA REGISTRADA.**

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Plataforma](https://img.shields.io/badge/Plataforma-Termux%20%7C%20Linux-green)
![Motor](https://img.shields.io/badge/Motor-holehe-important)

---

## 📖 O QUE A FERRAMENTA FAZ

O EMAIL TRACE VERIFICA SE UM ENDERECO DE E-MAIL POSSUI CONTA REGISTRADA EM **MAIS DE 120 SERVICOS ONLINE**, INCLUINDO:

INSTAGRAM, GOOGLE, SNAPCHAT, SPOTIFY, PAYPAL, ADOBE, GITHUB, EBAY, DISCORD, AMAZON, TWITTER/X, TIKTOK, IMGUR, PATREON, PINTEREST, TUMBLR, SOUNDCLOUD, YAHOO, OFFICE365, SAMSUNG, E MUITOS OUTROS.

### COMO FUNCIONA

A FERRAMENTA USA O FLUXO PUBLICO DE "ESQUECI MINHA SENHA" E DE CADASTRO DE CADA SITE PARA INFERIR SE O E-MAIL ESTA CADASTRADO — **SEM ENVIAR NENHUM E-MAIL AO ALVO** (OPERACAO STEALTH, O DONO DA CONTA NAO E NOTIFICADO).

### NIVEL DE CONFIANCA DOS RESULTADOS

| NIVEL | SIGNIFICADO |
|-------|-------------|
| `[+] CONFIRMADO` | APARECEU E-MAIL/TELEFONE MASCARADO DE RECUPERACAO → PROVA FORTE |
| `[+] REGISTRADO` | ALTA CONFIANCA DE QUE A CONTA EXISTE |
| `[?] PROVAVEL` | SUSPEITO DE RATE-LIMIT → PODE SER FALSO-POSITIVO |
| `[-] INDETERMINADO` | O SITE BLOQUEOU A CONSULTA |
| `[-] NAO ENCONTRADO` | PROVAVELMENTE NAO EXISTE CONTA |

### FUNCIONALIDADES

- ✅ VARREDURA EM 120+ SERVICOS EM PARALELO
- ✅ STEALTH — NAO NOTIFICA O ALVO
- ✅ NIVEL DE CONFIANCA ANTI FALSO-POSITIVO
- ✅ EXIBE E-MAIL E TELEFONE DE RECUPERACAO MASCARADOS
- ✅ RELATORIO SALVO EM ARQUIVO (--save)
- ✅ SUPORTE A LISTA DE MULTIPLOS E-MAILS (-l)
- ✅ BANNER GRANDE + SPINNER DE PROGRESSO
- ✅ FUNCIONA NO TERMUX E LINUX

## 🛠️ INSTALACÃO
## 📱 TERMUX (ANDROID)
---
pkg update && pkg upgrade -y
--
pkg install python git -y
---
git clone https://github.com/user5647382910/EMAIL-TRACE.git
cd EMAIL-TRACE
---
pip install --upgrade pip
---
pip install -r requirements.txt
---

## 🛠 INSTALACÃO
## 💻 LINUX (KALI / DEBIAN / UBUNTU)
---
sudo apt update && sudo apt upgrade -y
---
sudo apt install python3 python3-pip git -y
git clone https://github.com/SEU_USUARIO/EMAIL-TRACE.git
---
cd EMAIL-TRACE
---
pip3 install --upgrade pip
---
pip3 install -r requirements.txt
---

## 🚀 COMO USAR
---
# VARREDURA COMPLETA (MOSTRA TUDO)
python3 mailtrace.py alvo@email.com
---
# SO MOSTRA ONDE TEM CONTA
python3 mailtrace.py alvo@email.com --only-used
---
# MODO ESTRITO (RECOMENDADO) — ESCONDE SUSPEITOS DE FALSO-POSITIVO
python3 mailtrace.py alvo@email.com --strict
---
# SALVA O RELATORIO EM ARQUIVO
python3 mailtrace.py alvo@email.com --strict --save relatorio.txt
---
# VARIOS E-MAILS DE UMA LISTA (UM POR LINHA)
python3 mailtrace.py -l emails.txt --save relatorio.txt
---
# AUMENTA O TIMEOUT POR SITE (REDE LENTA)
python3 mailtrace.py alvo@email.com --timeout 20
---
# PARA RODAR DIRETO COM ./mailtrace.py (SEM "python3")
chmod +x mailtrace.py
./mailtrace.py alvo@email.com --strict
---

## 🔄 COMO ATUALIZAR NO TERMUX
---
cd EMAIL-TRACE
---
git pull origin main
---
pip install -r requirements.txt
---

## 🔄 COMO ATUALIZAR NO LINUX
---
cd EMAIL-TRACE
---
git pull origin main
---
pip3 install -r requirements.txt
---

## 🗑 COMO DESINSTALAR NO TERMUX
---
cd ~
---
rm -rf EMAIL-TRACE
---
pip uninstall holehe -y
---

## 🗑 COMO DESINSTALAR NO LINUX 
---
cd ~
---
rm -rf EMAIL-TRACE
---
pip3 uninstall holehe -y
---

## 🧠 MOTOR
ESTE PROJETO E UM WRAPPER SOBRE O HOLEHE (GPL-3.0). CREDITOS DA ENGINE: MEGADOSE.
---

## ⚠️ AVISO LEGAL
USE APENAS EM E-MAILS QUE VOCE TEM AUTORIZACAO PARA INVESTIGAR (CONTA PROPRIA, PENTEST AUTORIZADO, INVESTIGACAO OSINT LEGAL). O USO INDEVIDO E DE RESPONSABILIDADE EXCLUSIVA DO USUARIO.
---
## MEU DISCORD user7391054826
## MEU TIKTOK user2714950386
