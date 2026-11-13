#!/usr/bin/env bash
# Publishes only this new project. Existing remote repositories are never reused.
set -euo pipefail
task_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
task_target="AIPMAndy/chinese-international-student-business-jobs"
task_pages_url="https://aipmandy.github.io/chinese-international-student-business-jobs/"
cd "$task_root"

for task_command in git gh python3; do
  command -v "$task_command" >/dev/null || { echo "Required command is missing: $task_command" >&2; exit 1; }
done

# Read-only preflight: require the existing, reviewed deliverables before any writes.
for task_file in README.md SOURCES.md LICENSE CONTENT_LICENSE.md THIRD_PARTY_NOTICES.md DEPLOYMENT.md dist/index.html downloads/business-careers-guide.pdf downloads/business-job-workbook.xlsx scripts/package.py scripts/check_pages_links.py .github/workflows/pages.yml; do
  [[ -s "$task_file" ]] || { echo "Required project file is missing or empty: $task_file" >&2; exit 1; }
done
for task_directory in content templates cases research; do
  [[ -d "$task_directory" ]] || { echo "Required project directory is missing: $task_directory" >&2; exit 1; }
done
# The packager writes only these project paths. Do not follow output symlinks.
for task_path in downloads dist dist/downloads audit downloads/business-careers-guide.pdf downloads/business-job-workbook.xlsx downloads/templates-and-cases.zip downloads/repository-source.zip downloads/SHA256SUMS.txt dist/downloads/business-careers-guide.pdf dist/downloads/business-job-workbook.xlsx dist/downloads/templates-and-cases.zip dist/downloads/repository-source.zip dist/downloads/SHA256SUMS.txt audit/downloads-manifest.json; do
  [[ ! -L "$task_path" ]] || { echo "Project output is a symbolic link; stopped: $task_path" >&2; exit 1; }
done

task_git_root=""
if task_git_root="$(git rev-parse --show-toplevel 2>/dev/null)"; then
  [[ "$task_git_root" == "$task_root" ]] || { echo 'Working directory is inside another repository; stopped.' >&2; exit 1; }
  [[ -d .git && ! -L .git ]] || { echo 'A standalone project repository is required; linked worktrees are not changed.' >&2; exit 1; }
  if git remote get-url github >/dev/null 2>&1; then
    echo 'A github remote already exists; inspect it before publishing.' >&2
    exit 1
  fi
elif [[ -e .git || -L .git ]]; then
  echo 'Local Git metadata could not be verified; stopped.' >&2
  exit 1
fi

gh auth status --hostname github.com >/dev/null 2>&1 || { echo 'GitHub CLI is not authenticated for github.com; no repository or package was changed. User authorization is already recorded; an authenticated execution channel is required.' >&2; exit 1; }
task_owner="$(gh api --hostname github.com user --jq .login)"
[[ "$task_owner" == 'AIPMAndy' ]] || { echo 'Authenticated account is not AIPMAndy; stopped.' >&2; exit 1; }
if task_repo_check="$(gh api --hostname github.com "repos/$task_target" 2>&1)"; then
  echo 'Target repository already exists. Inspect it before any continuation; this script will not modify it.' >&2
  exit 1
elif [[ "$task_repo_check" != *"HTTP 404"* ]]; then
  echo 'Could not confirm that the target repository is absent; no repository or package was changed.' >&2
  exit 1
fi

# A source ZIP cannot contain itself. Restore all downloadable packages after extraction.
# This standard-library step preserves the reviewed PDF/XLSX and does not rebuild them.
python3 scripts/package.py
cp downloads/repository-source.zip downloads/SHA256SUMS.txt dist/downloads/
python3 scripts/check_pages_links.py

if [[ -z "$task_git_root" ]]; then
  git init -b main
fi
git add .
if ! git diff --cached --quiet; then
  git commit -m 'Publish complete international student business careers guide'
fi
GH_HOST=github.com gh repo create "$task_target" --public --description '中国留学生商科岗位求职保姆级攻略：六条职能路线、地区路径、专业案例、模板与完整 PDF。作者 AI 酋长 Andy。' --homepage "$task_pages_url"
git remote add github "https://github.com/$task_target.git"
git push --set-upstream github HEAD:main
task_local_commit="$(git rev-parse HEAD)"
task_remote_commit="$(gh api --hostname github.com "repos/$task_target/commits/main" --jq .sha)"
[[ "$task_remote_commit" == "$task_local_commit" ]] || { echo 'Remote main does not match the local commit; publishing is not verified.' >&2; exit 1; }
GH_HOST=github.com gh repo view "$task_target" --json url,visibility,defaultBranchRef
echo "Source push verified at $task_remote_commit. GitHub Pages is the only official website target: $task_pages_url"
echo 'Pages is not yet verified: select GitHub Actions in Settings > Pages, confirm the workflow succeeds, and visit the actual page_url and downloads.'
