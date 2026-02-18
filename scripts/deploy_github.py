"""
🚀 Jelly V6 - GitHub Deploy Automator
Este script automatiza o processo de deploy para o GitHub,
garantindo limpeza de arquivos antigos e segurança.

Uso:
    python scripts/deploy_github.py
"""
import os
import subprocess
import sys

# Arquivos obsoletos para remover
FILES_TO_REMOVE = [
    "brain.py",
    "app.py",
    "app_top.py",
    "app_backup.py",
    "package-lock.json"
]

REPO_URL = "https://github.com/codeZ-coder/JellyV6.git"

def run_cmd(cmd):
    """Executa um comando shell e para se der erro"""
    print(f"🔄 Executando: {cmd}")
    try:
        subprocess.check_call(cmd, shell=True)
        print("✅ Sucesso\n")
    except subprocess.CalledProcessError:
        print(f"❌ Erro ao executar: {cmd}")
        sys.exit(1)

def main():
    print("="*50)
    print("🚀 JELLY V6 - DEPLOY AUTOMÁTICO")
    print("="*50)

    # 1. Limpeza
    print("🧹 [1/4] Removendo arquivos obsoletos...")
    for f in FILES_TO_REMOVE:
        if os.path.exists(f):
            os.remove(f)
            print(f"   - Removido: {f}")
        else:
            print(f"   - Já inexistente: {f}")
    print("✅ Limpeza concluída.\n")

    # 2. Configurar Git
    print("⚙️ [2/4] Configurando Remote Git...")
    try:
        # Tenta adicionar, se falhar tenta set-url
        subprocess.check_call(f"git remote add origin {REPO_URL}", shell=True, stderr=subprocess.DEVNULL)
    except:
        subprocess.check_call(f"git remote set-url origin {REPO_URL}", shell=True)
    print(f"   - Remote configurado: {REPO_URL}\n")

    # 3. Commit
    print("📦 [3/4] Criando Commit de Release...")
    run_cmd("git add .")
    try:
        subprocess.check_call('git commit -m "feat: JellyV6 NerveNet Architecture Release 🪼"', shell=True)
    except:
        print("   (Nada para commitar ou commit já existe)")

    # 4. Push
    print("🚀 [4/4] Enviando para GitHub...")
    print("   Isso pode pedir sua senha/token do GitHub.")
    run_cmd("git branch -M main")
    run_cmd("git push -u origin main")

    print("\n" + "="*50)
    print("🏆 DEPLOY CONCLUÍDO COM SUCESSO!")
    print(f"🌐 Verifique em: {REPO_URL}")
    print("="*50)

if __name__ == "__main__":
    main()
