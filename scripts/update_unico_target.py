import requests
from bs4 import BeautifulSoup
import re
import subprocess
import os
import time

# ===============================
# Settings
# ===============================
URL = "https://developer.unico.io/pt-BR/developers/sdks-and-tools/android/resources/release-notes"
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

content = soup.select_one("div.theme-doc-markdown")
header = content.find("h2") if content else None

if header:
    site_version = header.get_text(strip=True)

    # A data no site vem no formato MM/DD/YYYY; convertemos para DD/MM/YYYY
    date_tag = header.find_next_sibling("p")
    if date_tag:
        date_match = re.search(r"(\d{2})/(\d{2})/(\d{4})", date_tag.get_text())
        if date_match:
            month, day, year = date_match.groups()
            release_date = f"{day}/{month}/{year}"

    notes_block = header.find_next_sibling("ul")
    if notes_block:
        for li in notes_block.find_all("li"):
            text = li.get_text(strip=True)
            if text:
                release_notes.append(text)

# ===============================
# Step 2: Validate extracted data
# ===============================
if not site_version:
    print("❌ Could not capture the version from the website")
    if release_notes:
        print("\n📝 Release notes were found, but the version header failed to parse:")
        for note in release_notes:
            print(f"- {note}")
    exit(1)

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

    # O nome da tag de versão deve ser limpo, sem timestamp.
    tag = f"{DEPENDENCY_ARTIFACT}-v{site_version}"
    
    # Usar um timestamp para o branch é uma boa prática para garantir que ele seja único.
    timestamp = int(time.time())
    branch = f"update-{DEPENDENCY_ARTIFACT}-v{site_version}-{timestamp}"

    # Git configuration and push
    subprocess.run(["git", "checkout", "-b", branch], check=True)
    subprocess.run(["git", "config", "user.name", "github-actions"], check=True)
    subprocess.run(["git", "config", "user.email", "github-actions@github.com"], check=True)
    subprocess.run(["git", "add", gradle_path], check=True)
    subprocess.run(["git", "commit", "-m", f"chore: bump {DEPENDENCY_ARTIFACT} to v{site_version}"], check=True)
    subprocess.run(["git", "push", "origin", branch], check=True)

    ### AJUSTE AQUI: LÓGICA PARA GERENCIAR A TAG ###
    # 1. Tenta deletar a tag no repositório remoto, caso ela já exista de uma execução anterior.
    # Usamos 'check=False' para que o script NÃO pare se a tag não existir (o que é esperado na primeira vez).
    print(f"ℹ️  Attempting to delete remote tag '{tag}' if it exists...")
    subprocess.run(["git", "push", "origin", "--delete", tag], check=False)
    
    # 2. Cria a tag localmente.
    print(f"✅ Creating local tag: {tag}")
    subprocess.run([
        "git", "tag", "-a", tag,
        "-m", f"Release {DEPENDENCY_ARTIFACT} {site_version} ({release_date})"
    ], check=True)
    
    # 3. Envia a nova tag para o repositório. Agora este comando não vai mais falhar.
    print(f"🚀 Pushing new tag to remote...")
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
    print(f"🎉 Pull Request created: {pr_url}")
    github_output = os.getenv("GITHUB_OUTPUT")

    if github_output:
        with open(github_output, "a") as f:
            f.write(f"updated=true\n")
            f.write(f"new_version={site_version}\n")
            f.write(f"release_date={release_date}\n")
            f.write(f"pr_url={pr_url}\n")
            f.write("release_notes<<EOF\n")
            f.write(f"{notes_formatted}\n")
            f.write("EOF\n")

else:
    print("🔄 Already at the latest version, nothing to do.")
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            print(f"updated=false", file=f)