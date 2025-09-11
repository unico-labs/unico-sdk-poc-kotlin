import requests
from bs4 import BeautifulSoup
import re
import subprocess
import os

# ===============================
# Settings
# ===============================
URL = "https://devcenter.unico.io/idcloud/integracao/sdk/integracao-sdks/sdk-android/release-notes"
DEPENDENCY_NAME = "io.unico:capture"
REPO_PATH = "." # Diretório do repositório local
FILE_TO_UPDATE = "app/build.gradle"

# Função para dar pull caso já exista algum repositório criado.
def doPullRequest(branch_name): 
    try:
        print("EXECUTANDO O COMANDO PULL --REBASE ORIGIN !")
        subprocess.run(["git", "pull", "--rebase", "origin", branch_name], check=True)
    except subprocess.CalledProcessError as e:
            # If pull fails, it means the branch is new, so we continue without pulling.
            print(f"Branch does not exist on remote. Proceeding with initial push.")


# ===============================
# 1️⃣ Buscar versão + data no site
# ===============================
print("🔎 Fetching latest version from Unico's release notes...")
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

divs = soup.find_all("div") # Busca todas as divs para encontrar a que tem a versão
site_version = None
release_date = None

# Regex para encontrar o padrão "Versão X.X.X - DD/MM/YYYY"
version_pattern = re.compile(r"Versão\s*([\d.]+)\s*​\s*-\s*\s*(\d{2}/\d{2}/\d{4})")
match = "";
for div in divs:
    text_content = div.get_text(strip=True)
    print(text_content)
    match = version_pattern.search(text_content)
    if match:
        site_version = match.group(1)
        release_date = match.group(2)
        break

if not site_version:
    print("❌ Could not capture the version from the website. Check the HTML structure.")
    exit(1)

print(f"📦 Latest version on the website: {site_version}")
print(f"🗓️ Release date: {release_date}")

print(f"📖 Reading and updating {FILE_TO_UPDATE} file...")

# Cria o caminho completo do arquivo para o projeto Kotlin
# O uso de os.path.join garante que o caminho seja construído corretamente em qualquer OS.
full_file_path = os.path.join(REPO_PATH, FILE_TO_UPDATE)

try:
    with open(full_file_path, "r", encoding="utf-8") as f:
        content = f.read()
except FileNotFoundError:
    raise FileNotFoundError(f"❌ O arquivo '{full_file_path}' não foi encontrado.")

# Regex melhorada para ser mais robusta.
# Procura pela dependência e captura a versão, tratando aspas simples ou duplas.
dependency_pattern = re.compile(rf"compileSdkVersion\s+(['\"]?{DEPENDENCY_NAME}['\"]?):['\"]?([\d\.]+)['\"]?", re.DOTALL)
match = dependency_pattern.search(content)

if not match:
    raise ValueError(f"❌ Dependência '{DEPENDENCY_NAME}' não encontrada no arquivo.")

current_version = match.group(2) # Captura o segundo grupo, que é o número da versão

if current_version != site_version:
    print(f"✅ Atualizando {DEPENDENCY_NAME} de {current_version} para {site_version}...")

    # Substitui a versão antiga pela nova usando re.sub
    new_content = dependency_pattern.sub(f"{DEPENDENCY_NAME}:{site_version}", content)

    try:
        with open(FILE_TO_UPDATE, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"🎉 O arquivo '{FILE_TO_UPDATE}' foi atualizado com sucesso!")
    except IOError as e:
        raise IOError(f"❌ Erro ao escrever no arquivo '{FILE_TO_UPDATE}': {e}")

    try:
    # --- Automação Git e GitHub ---
        branch = f"chore/update-{DEPENDENCY_NAME}-v{site_version}"
        tag = f"v{site_version}"
        commit_message = f"chore: bump {DEPENDENCY_NAME} to v{site_version}"

        print("🤖 Starting Git automation...")
        subprocess.run(["git", "checkout", "-b", branch], check=True)
        subprocess.run(["git", "config", "user.name", "github-actions"], check=True)
        subprocess.run(["git", "config", "user.email", "github-actions@github.com"], check=True)
        subprocess.run(["git", "add", FILE_TO_UPDATE], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push", "origin", branch], check=True)

        tag_message = f"Release {DEPENDENCY_NAME} {site_version} ({release_date})"
            
        subprocess.run(["git", "tag", "-a", tag, "-m", tag_message], check=True)
        subprocess.run(["git", "push", "origin", tag], check=True)

        pr_body = f"""
        ### 🚀 Automatic Update
        Bumps `{DEPENDENCY_NAME}` from `{current_version}` to version **{site_version}**.
        
        - 📅 **Release date**: {release_date}
        - 🔗 **Official Release Notes**: [{URL}]({URL})
        """

        subprocess.run([
            "gh", "pr", "create",
            "--title", commit_message,
            "--body", pr_body,
            "--head", branch,
            "--base", "main" # Altere 'main' para sua branch principal se for outra
        ], check=True)

        print(f"🎉 Successfully created branch, tag, and Pull Request for version {site_version}!")

    except subprocess.CalledProcessError as e:
            raise RuntimeError(f"❌ Erro em um comando Git/GitHub CLI: {e}")
else:
    print("🔄 Already at the latest version, nothing to do.")