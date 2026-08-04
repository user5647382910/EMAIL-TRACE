#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
  EMAIL TRACE v2 — varredura OSINT de e-mail com níveis de confiança
  Motor: holehe | Termux
  Uso:  python3 mailtrace.py alvo@email.com [--only-used] [--strict]
        python3 mailtrace.py alvo@email.com --no-password-recovery
"""

import sys
import re
import time
import argparse
import threading
from datetime import datetime

# ─────────────────────────── cores ANSI ───────────────────────────
G  = "\033[92m"
R  = "\033[91m"
Y  = "\033[93m"
C  = "\033[96m"
B  = "\033[1m"
D  = "\033[0m"
GR = "\033[90m"

# ─────────────────── banner grande (fonte ANSI Shadow) ───────────────────
FONT = {
 'E': ["███████╗","██╔════╝","█████╗  ","██╔══╝  ","███████╗","╚══════╝"],
 'M': ["███╗   ███╗","████╗ ████║","██╔████╔██║","██║╚██╔╝██║","██║ ╚═╝ ██║","╚═╝     ╚═╝"],
 'A': [" █████╗ ","██╔══██╗","███████║","██╔══██║","██║  ██║","╚═╝  ╚═╝"],
 'I': ["██╗","██║","██║","██║","██║","╚═╝"],
 'L': ["██╗     ","██║     ","██║     ","██║     ","███████╗","╚══════╝"],
 'T': ["████████╗","╚══██╔══╝","   ██║   ","   ██║   ","   ██║   ","   ╚═╝   "],
 'R': ["██████╗ ","██╔══██╗","██████╔╝","██╔══██╗","██║  ██║","╚═╝  ╚═╝"],
 'C': [" ██████╗","██╔════╝","██║     ","██║     ","╚██████╗"," ╚═════╝"],
 ' ': ["      "] * 6,
}

def banner(texto):
    linhas = [""] * 6
    for ch in texto.upper():
        for i, linha in enumerate(FONT.get(ch, FONT[' '])):
            linhas[i] += linha + "  "
    return "\n".join(linhas)

# ─────────────────────────── detecção do motor ───────────────────────────
ENGINE = None
try:
    from holehe.core import import_submodules, get_functions, launch_module
    ENGINE = "trio"
except Exception:
    try:
        from holehe import check_email
        ENGINE = "async"
    except Exception:
        ENGINE = None

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")


def scan_com_holehe(email, timeout, no_password_recovery=False):
    """Motor oficial holehe — varredura paralela com trio + httpx."""
    import trio
    import httpx

    async def _run():
        modules = import_submodules("holehe.modules")
        args = argparse.Namespace(nopasswordrecovery=no_password_recovery)
        websites = get_functions(modules, args)
        client = httpx.AsyncClient(timeout=timeout)
        out = []
        async with trio.open_nursery() as nursery:
            for site in websites:
                nursery.start_soon(launch_module, site, email, client, out)
        await client.aclose()
        return out

    return trio.run(_run)


def scan_com_check_email(email, timeout):
    """Motor alternativo (forks com API check_email)."""
    import asyncio
    async def _run():
        return await check_email(email)
    return asyncio.run(_run)


def iniciar_spinner():
    parar = threading.Event()
    chars = "|/-\\"
    def animar():
        i = 0
        while not parar.is_set():
            sys.stdout.write(f"\r{C}[*]{D} {B}Escaneando serviços...{D} {C}{chars[i % 4]}{D}")
            sys.stdout.flush()
            time.sleep(0.12)
            i += 1
    t = threading.Thread(target=animar, daemon=True)
    t.start()
    return parar, t


# ─────────── classificação de confiança (anti falso-positivo) ───────────
def classificar(d):
    if d.get("error") or d.get("rateLimit"):
        return "erro"          # bloqueado/indeterminado
    if not d.get("exists"):
        return "nao"           # não encontrado
    if d.get("emailrecovery") or d.get("phoneNumber"):
        return "confirmado"    # prova forte: recuperação mascarada
    if d.get("frequent_rate_limit"):
        return "baixa"         # site campeão de rate-limit → suspeito
    return "alta"              # alta confiança


def mostrar_resultados(email, dados, so_encontrados, estrito=False):
    if so_encontrados:
        print(f"\n{B}{C}═══ RESULTADOS ({email}) — apenas contas ═══{D}")
    else:
        print(f"\n{B}{C}═══ RESULTADOS ({email}) ═══{D}")
    if estrito:
        print(f"{GR}  Modo estrito: exibe apenas confirmações e alta confiança{D}")

    for d in dados:
        d["_conf"] = classificar(d)

    confirmados = [d for d in dados if d["_conf"] == "confirmado"]
    altos       = [d for d in dados if d["_conf"] == "alta"]
    baixos      = [d for d in dados if d["_conf"] == "baixa"]
    erros       = [d for d in dados if d["_conf"] == "erro"]
    nao         = [d for d in dados if d["_conf"] == "nao"]

    visiveis = confirmados + altos
    if not estrito:
        visiveis += baixos

    if so_encontrados and not visiveis:
        print(f"  {Y}Nenhuma conta de alta confiança encontrada.{D}")

    for d in visiveis:
        if d["_conf"] == "confirmado":
            marca = f"{G}[+] CONFIRMADO{D}"
        elif d["_conf"] == "alta":
            marca = f"{G}[+] REGISTRADO{D}"
        else:
            marca = f"{Y}[?] PROVÁVEL{D}"
        extra = ""
        if d.get("emailrecovery"):
            extra += f" {GR}[rec: {C}{d['emailrecovery']}{GR}]{D}"
        if d.get("phoneNumber"):
            extra += f" {GR}[tel: {C}{d['phoneNumber']}{GR}]{D}"
        if d["_conf"] == "baixa":
            extra += f" {GR}[rate-limit frequente — pode ser falso-positivo]{D}"
        print(f"  {marca}  {B}{d.get('domain','?')}{D} {GR}({d.get('name','?')}){D}{extra}")

    for d in erros:
        print(f"  {GR}[-] INDETERMINADO{D} {d.get('domain','?')} {GR}(bloqueado pelo site){D}")

    if not so_encontrados:
        for d in nao:
            print(f"  {R}[-] NÃO ENCONTRADO{D} {d.get('domain','?')} {GR}({d.get('name','?')}){D}")

    print(f"\n  {C}═{D} Total: {B}{len(dados)}{D} | {G}Contas: {B}{len(visiveis)}{D} "
          f"| {Y}Suspeitas: {B}{len(baixos)}{D} | {GR}Indeterminadas: {B}{len(erros)}{D} "
          f"| {R}Não encontradas: {B}{len(nao)}{D}")


def salvar(email, dados, caminho):
    rotulo = {"confirmado": "CONFIRMADO", "alta": "REGISTRADO",
              "baixa": "PROVÁVEL", "erro": "INDETERMINADO", "nao": "NÃO ENCONTRADO"}
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(f"EMAIL TRACE — relatório gerado em {datetime.now().isoformat()}\n")
        f.write(f"Alvo: {email}\n")
        f.write("=" * 62 + "\n")
        for d in sorted(dados, key=lambda x: ("confirmado","alta","baixa","erro","nao").index(x.get("_conf","nao"))):
            linha = f"[{rotulo.get(d.get('_conf'),'?')}] {d.get('domain','?')} ({d.get('name','?')})"
            if d.get("emailrecovery"):
                linha += f" | recuperação: {d['emailrecovery']}"
            if d.get("phoneNumber"):
                linha += f" | telefone: {d['phoneNumber']}"
            f.write(linha + "\n")
    print(f"  {G}[+]{D} Relatório salvo em: {B}{caminho}{D}")


def main():
    parser = argparse.ArgumentParser(
        description="EMAIL TRACE v2 — descobre em quais sites um e-mail tem conta (motor: holehe)")
    parser.add_argument("emails", nargs="*", help="E-mail(s) alvo")
    parser.add_argument("-l", "--list", help="Arquivo com lista de e-mails (um por linha)")
    parser.add_argument("--only-used", action="store_true",
                        help="Mostrar apenas contas encontradas")
    parser.add_argument("--strict", action="store_true",
                        help="Ocultar resultados suspeitos (PROVÁVEL) — menos falsos positivos")
    parser.add_argument("--no-password-recovery", action="store_true",
                        help="Pular sites que usam recuperação de senha (Adobe, Mail.ru, Samsung...)")
    parser.add_argument("--timeout", type=int, default=10,
                        help="Timeout por requisição em segundos (padrão: 10)")
    parser.add_argument("--save", metavar="ARQUIVO", help="Salvar relatório em arquivo")
    parser.add_argument("--no-banner", action="store_true", help="Não exibir o banner")
    args = parser.parse_args()

    alvos = list(args.emails or [])
    if args.list:
        try:
            with open(args.list, encoding="utf-8") as f:
                alvos += [l.strip() for l in f if l.strip()]
        except FileNotFoundError:
            print(f"{R}[-]{D} Arquivo de lista não encontrado: {args.list}")
            sys.exit(1)

    if not alvos:
        alvo = input(f"{C}[?]{D} Digite o e-mail alvo: ").strip()
        if alvo:
            alvos = [alvo]

    if not alvos:
        print(f"{R}[-]{D} Nenhum e-mail informado.")
        sys.exit(1)

    if not args.no_banner:
        print(f"{C}{B}{banner('EMAIL TRACE')}{D}")
        print(f"{GR}{'═' * 64}{D}")
        print(f"{GR}  OSINT · motor: holehe · {len(alvos)} alvo(s) · stealth · Termux{D}")
        print(f"{GR}{'═' * 64}{D}\n")

    if ENGINE is None:
        print(f"{R}[-]{D} Motor 'holehe' não encontrado. Instale com:")
        print(f"{Y}   Termux:{D}  pkg install python && pip install holehe")
        sys.exit(1)

    for i, email in enumerate(alvos, 1):
        email = email.strip()
        if not EMAIL_RE.match(email):
            print(f"{R}[-]{D} E-mail inválido, pulando: {email}")
            continue

        print(f"\n{C}[*]{D} Alvo {i}/{len(alvos)}: {B}{email}{D}")

        parar, t = iniciar_spinner()
        try:
            if ENGINE == "trio":
                dados = scan_com_holehe(email, args.timeout, args.no_password_recovery)
            else:
                dados = scan_com_check_email(email, args.timeout)
        except KeyboardInterrupt:
            parar.set(); t.join()
            print(f"\n{R}[!]{D} Interrompido pelo usuário.")
            sys.exit(130)
        except Exception as e:
            parar.set(); t.join()
            sys.stdout.write("\r" + " " * 60 + "\r")
            print(f"{R}[-]{D} Erro na varredura: {e}")
            continue
        parar.set(); t.join()
        sys.stdout.write("\r" + " " * 60 + "\r")
        sys.stdout.flush()

        mostrar_resultados(email, dados, args.only_used, args.strict)

        if args.save:
            caminho = (args.save if len(alvos) == 1
                       else f"{args.save}_{re.sub(r'[^a-zA-Z0-9]', '_', email)}.txt")
            salvar(email, dados, caminho)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}[!]{D} Interrompido.")
        sys.exit(130)
