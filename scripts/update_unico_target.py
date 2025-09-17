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
FILE_TO_UPDATE = "app/build.gradle"

script_dir = os.path.dirname(os.path.abspath(__file__))
REPO_PATH = os.path.abspath(os.path.join(script_dir, '..'))

# ===============================
# Step 1: Fetch version and release date from the website
# ===============================
print("🔎 Fetching latest version from Unico's release notes...")
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

site_version = None
release_date = None

version_pattern = re.compile(r"Versão\s*([\d.]+)\s*-\s*(\d{2}/\d{2}/\d{4})")

divs = soup.find_all("div")
for div in divs:
    text_content = div.get_text(strip=True)
    match = version_pattern.search(text_content)
    if match:
        site_version = match.group(1)
        release_date = match.group(2)
        break

if not site_version:
    print("❌ Could not capture the version from the website. Check the HTML structure or regex.")
    exit(1)

print(f"📦 Latest version on the website: {site_version}")
print(f"🗓️ Release date: {release_date}")

# ===============================
# Step 2: Read and update the gradle file
# ===============================
full_file_path = os.path.join(REPO_PATH, FILE_TO_UPDATE)

try:
    with open(full_file_path, "r", encoding="utf-8") as f:
        content = f.read()
except FileNotFoundError:
    print(f"❌ O arquivo '{full_file_path}' não foi encontrado.")
    exit(1)

dependency_pattern = re.compile(rf'(implementation\s+["\']{DEPENDENCY_NAME}:)([\d.]+)["\']', re.MULTILINE)
match = dependency_pattern.search(content)

if not match:
    print(f"❌ Dependência '{DEPENDENCY_NAME}' não encontrada no arquivo.")
    exit(1)

current_version = match.group(2)
print(f"✅ Current version in {FILE_TO_UPDATE}: {current_version}")

if current_version != site_version:
    print(f"⬆️ New version found! Updating from {current_version} to {site_version}.")

    new_content = dependency_pattern.sub(rf"\g<1>{site_version}'", content, count=1)

    with open(full_file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"🎉 File '{FILE_TO_UPDATE}' was successfully updated!")

    # ===============================
    # Step 3: Create branch, commit, and Pull Request
    # ===============================
 
    branch = f"update-{DEPENDENCY_NAME.replace(':', '-')}-v{site_version}"
    tag = f"v{site_version}" 

    print(f"🌿 Creating branch '{branch}'...")
    subprocess.run(["git", "checkout", "-b", branch], check=True)
    subprocess.run(["git", "config", "user.name", "github-actions"], check=True)
    subprocess.run(["git", "config", "user.email", "github-actions@github.com"], check=True)
    
    subprocess.run(["git", "add", full_file_path], check=True)
    
    commit_message = f"chore: bump {DEPENDENCY_NAME} to v{site_version}"
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    subprocess.run(["git", "push", "--set-upstream", "origin", branch], check=True)

    print(f"🔖 Creating tag '{tag}'...")
    subprocess.run(["git", "tag", "-a", tag, "-m", f"Release {DEPENDENCY_NAME} {site_version} ({release_date})"], check=True)
    subprocess.run(["git", "push", "origin", tag], check=True)

    print("🚀 Creating Pull Request...")
    body = f"Automatic update of `{DEPENDENCY_NAME}` to version **{site_version}**.\n\n📅 Release date: **{release_date}**\n🔗 [Official Release Notes]({URL})"

    pr_process = subprocess.run([
        "gh", "pr", "create",
        "--title", f"Update {DEPENDENCY_NAME} to v{site_version}",
        "--body", body,
        "--head", branch
    ], check=True, capture_output=True, text=True)

    pr_url = pr_process.stdout.strip()
    print(f"✅ Pull Request created: {pr_url}")

    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            print(f"updated=true", file=f, flush=True)
            print(f"new_version={site_version}", file=f, flush=True)
            print(f"pr_url={pr_url}", file=f, flush=True)
else:
    print("🔄 Already at the latest version, nothing to do.")
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            print(f"updated=false", file=f, flush=True)