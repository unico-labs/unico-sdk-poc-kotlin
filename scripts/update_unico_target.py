import requests
from bs4 import BeautifulSoup
import re
import subprocess
import os
import time

# ===============================
# Settings
# ===============================
URL = "https://devcenter.unico.io/idcloud/integracao/sdk/integracao-sdks/sdk-android/release-notes"
DEPENDENCY_GROUP = "io.unico"
DEPENDENCY_ARTIFACT = "capture"
REPO_PATH = "."  # Path to the local repository

# ===============================
# Step 1: Fetch version, date and release notes from the website
# ===============================
print("🔎 Fetching latest version from Unico's Android release notes...")
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

site_version = None
release_date = None
release_notes = []
header = None

# Procura pelo primeiro cabeçalho <h3> que contém o texto "Versão"
# Isso é mais específico e garante que pegamos o título da release mais recente
for h3 in soup.find_all("h3"):
    if "Versão" in h3.get_text():
        header = h3
        break # Para no primeiro que encontrar, que é o mais recente

if header:
    # CORREÇÃO APLICADA AQUI: Adicionado ".*?" para ignorar caracteres invisíveis
    match = re.search(r"Versão\s*([\d.]+)\s*.*?\s*-\s*(\d{2}/\d{2}/\d{4})", header.get_text())
    if match:
        site_version = match.group(1)
        release_date = match.group(2)

    # A partir do cabeçalho encontrado, busca a próxima lista <ul> com as notas
    notes_block = header.find_next_sibling("ul", class_=lambda x: x and "space-y-2" in x)

    if notes_block:
        # Extrai o texto de cada parágrafo <p> dentro de um item da lista <li>
        for li in notes_block.find_all("li"):
            note_p = li.find("p")
            if note_p:
                text = note_p.get_text(strip=True)
                if text:
                    release_notes.append(text)

# ===============================
# Step 2: Validate extracted data
# ===============================
if not site_version:
    print("❌ Could not capture the version from the website")
    # Se ainda houver notas, vamos exibi-las para depuração
    if release_notes:
        print("\n📝 Release notes were found, but the version header failed to parse:")
        for note in release_notes:
            print(f"- {note}")
    exit(1) # Use exit(1) para sinalizar um erro

print(f"📦 Latest version on the website: {site_version}")
print(f"🗓️ Release date: {release_date}")

if release_notes:
    print("\n📝 Release notes found:")
    for note in release_notes:
        print(f"- {note}")
else:
    print("⚠️ No release notes found on the page.")

# ===============================
# Step 3: Read build.gradle from the target repository
# ===============================
gradle_path = os.path.join(REPO_PATH, "app", "build.gradle")
with open(gradle_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

current_version = None
dependency_pattern = re.compile(rf'implementation\s+"{DEPENDENCY_GROUP}:{DEPENDENCY_ARTIFACT}:(.*?)"')

for line in lines:
    match = dependency_pattern.search(line)
    if match:
        current_version = match.group(1)
        break

print(f"📂 Current version in build.gradle: {current_version}")

# ===============================
# Step 4: Update dependency if necessary
# ===============================
if current_version != site_version:
    new_lines = []
    for line in lines:
        if dependency_pattern.search(line):
            new_lines.append(f'    implementation "{DEPENDENCY_GROUP}:{DEPENDENCY_ARTIFACT}:{site_version}"\n')
        else:
            new_lines.append(line)

    with open(gradle_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"✅ Updated {DEPENDENCY_GROUP}:{DEPENDENCY_ARTIFACT} to version {site_version}")

    branch = f"update-{DEPENDENCY_ARTIFACT}-v{site_version}"
    tag = f"{DEPENDENCY_ARTIFACT}-v{site_version}"
    
    timestamp = int(time.time())
    branch = f"update-{DEPENDENCY_ARTIFACT}-v{site_version}-{timestamp}"
    tag = f"{DEPENDENCY_ARTIFACT}-v{site_version}"

    # Git configuration and push
    subprocess.run(["git", "checkout", "-b", branch], check=True)
    subprocess.run(["git", "config", "user.name", "github-actions"], check=True)
    subprocess.run(["git", "config", "user.email", "github-actions@github.com"], check=True)
    subprocess.run(["git", "add", gradle_path], check=True)
    subprocess.run(["git", "commit", "-m", f"chore: bump {DEPENDENCY_ARTIFACT} to v{site_version}"], check=True)
    subprocess.run(["git", "push", "origin", branch], check=True)

    # Create git tag and push it
    subprocess.run([
        "git", "tag", "-a", tag,
        "-m", f"Release {DEPENDENCY_ARTIFACT} {site_version} ({release_date})"
    ], check=True)
    subprocess.run(["git", "push", "origin", tag], check=True)

    # Build PR body dynamically with notes (if available)
    if release_notes:
        notes_formatted = "\n".join([f"- {note}" for note in release_notes])
    else:
        notes_formatted = "_No release notes available_"

    body = f"""
    Automatic update of `{DEPENDENCY_GROUP}:{DEPENDENCY_ARTIFACT}` to version **{site_version}** 📅  
    **Release date:** {release_date}  
    🔗 [Official Release Notes]({URL})

    **Changelog:**
    {notes_formatted}
    """

    pr_process = subprocess.run([
        "gh", "pr", "create",
        "--title", f"Update {DEPENDENCY_ARTIFACT} to v{site_version}",
        "--body", body,
        "--head", branch
    ], check=True, capture_output=True, text=True)

    pr_url = pr_process.stdout.strip()
    print(f"✅ Pull Request created: {pr_url}")

    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            print(f"updated=true", file=f)
            print(f"new_version={site_version}", file=f)
            print(f"release_date={release_date}", file=f)
            print(f"release_notes={notes_formatted}", file=f)
            print(f"pr_url={pr_url}", file=f)

else:
    print("🔄 Already at the latest version, nothing to do.")
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            print(f"updated=false", file=f)
