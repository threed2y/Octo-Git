"""
octo.py — Interactive GitHub CLI
Eight arms. One terminal. All of GitHub.
"""

from __future__ import annotations

import base64
import datetime
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import requests
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.syntax import Syntax
from rich.table import Table

# ── Console ───────────────────────────────────────────────────────────────────
console = Console()

# ── Theme — cyan / electric blue ─────────────────────────────────────────────
C   = "bold cyan"           # primary accent
CD  = "cyan"                # accent dim
CG  = "bright_cyan"         # accent glow
B   = "bold blue"           # secondary
BD  = "blue"
OK  = "bold green"
ERR = "bold red"
WARN= "bold yellow"
DIM = "grey50"
WHT = "white"

BORDER_MAIN = "cyan"
BORDER_SUB  = "blue"
BORDER_CODE = "bright_cyan"
BORDER_OK   = "green"
BORDER_ERR  = "red"
BORDER_DIM  = "grey30"
BORDER_WARN = "yellow"

GITHUB_API    = "https://api.github.com"
PROFILES_FILE = Path.home() / ".octo_profiles.json"
_active_profile: str = "default"

# ── Banner ────────────────────────────────────────────────────────────────────
BANNER = r"""
   ___   ___ _____ ___
  / _ \ / __|_   _/ _ \
 | (_) | (__  | || (_) |
  \___/ \___| |_| \___/
"""

BANNER_WIDE = r"""
   ██████╗  ██████╗████████╗ ██████╗
  ██╔═══██╗██╔════╝╚══██╔══╝██╔═══██╗
  ██║   ██║██║        ██║   ██║   ██║
  ██║   ██║██║        ██║   ██║   ██║
  ╚██████╔╝╚██████╗   ██║   ╚██████╔╝
   ╚═════╝  ╚═════╝   ╚═╝    ╚═════╝
"""

TAGLINE = "eight arms. one terminal. all of github."
VERSION = "v1.0.0"

# Octo tentacle separator — used in rules
_TENTACLE = "〰"


def _banner() -> None:
    console.print(f"[{CG}]{BANNER_WIDE}[/{CG}]")
    console.print(f"  [{DIM}]{TAGLINE}[/{DIM}]   [{DIM}]{VERSION}[/{DIM}]\n")


# ── UI primitives ─────────────────────────────────────────────────────────────

def _rule(label: str = "") -> None:
    if label:
        console.print(Rule(f"[{C}] {label} [{C}]", style=BORDER_MAIN))
    else:
        console.print(Rule(style=BORDER_DIM))


def _ok(msg: str)   -> None: console.print(f"[{OK}]  {msg}[/{OK}]")
def _err(msg: str)  -> None: console.print(f"[{ERR}]  {msg}[/{ERR}]")
def _warn(msg: str) -> None: console.print(f"[{WARN}]  {msg}[/{WARN}]")
def _info(msg: str) -> None: console.print(f"[{CD}]  {msg}[/{CD}]")


def _panel(content: Any, title: str = "", border: str = BORDER_SUB, **kw) -> None:
    t = f"[{C}]{title}[/{C}]" if title else ""
    console.print(Panel(content, title=t, border_style=border, padding=(0, 1), **kw))


def _kv_table(rows: list[tuple[str, str]]) -> Table:
    t = Table(box=box.SIMPLE, show_header=False, border_style=BORDER_DIM, padding=(0, 1))
    t.add_column(style=f"{CD} bold", no_wrap=True)
    t.add_column(style=WHT)
    for k, v in rows:
        t.add_row(k, v)
    return t


def _status(msg: str):
    return console.status(f"[{CD}]{msg}[/{CD}]")


def _back_prompt() -> None:
    inquirer.select(message="", choices=[Choice("_", "  ↩  back")]).execute()


# ── Profile / auth ────────────────────────────────────────────────────────────

def _load_profiles() -> dict[str, str]:
    if PROFILES_FILE.exists():
        try:
            return json.loads(PROFILES_FILE.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def _save_profiles(p: dict[str, str]) -> None:
    PROFILES_FILE.write_text(json.dumps(p, indent=2))
    if os.name != "nt":
        os.chmod(PROFILES_FILE, 0o600)


def _safe_token() -> str | None:
    return _load_profiles().get(_active_profile) or None


def get_headers() -> dict:
    h = {"Accept": "application/vnd.github.v3+json"}
    tok = _safe_token()
    if tok:
        h["Authorization"] = f"Bearer {tok}"
    return h


def setup_auth() -> None:
    _rule("Setup Token")
    _info("GitHub → Settings → Developer Settings → Personal Access Tokens (classic)")
    _info("Scopes:  repo  +  read:org\n")

    profile_name = (
        inquirer.text(message="Profile name:", default=_active_profile).execute().strip()
        or "default"
    )
    token = inquirer.secret(message="Personal Access Token:").execute()
    if not token or not token.strip():
        _warn("No token entered — skipping.")
        return

    profiles = _load_profiles()
    profiles[profile_name] = token.strip()
    _save_profiles(profiles)

    with _status("Validating..."):
        resp = requests.get(
            f"{GITHUB_API}/user",
            headers={"Accept": "application/vnd.github.v3+json",
                     "Authorization": f"Bearer {token.strip()}"},
            timeout=10,
        )
    if resp.status_code == 200:
        login = resp.json().get("login", "?")
        _ok(f"Authenticated as  {login}  (profile: {profile_name})")
    else:
        _err(f"Token saved but validation failed (HTTP {resp.status_code}).")


def switch_profile() -> None:
    global _active_profile
    profiles = _load_profiles()
    if not profiles:
        _warn("No profiles yet — run Setup Token first.")
        return
    choices = [
        Choice(k, f"{'▶ ' if k == _active_profile else '  '}{k}")
        for k in profiles
    ]
    _active_profile = inquirer.select(message="Switch to:", choices=choices).execute()
    _ok(f"Active profile → {_active_profile}")


def manage_profiles() -> None:
    _rule("Profile Manager")
    profiles = _load_profiles()
    if not profiles:
        _warn("No profiles saved yet.")
        return

    action = inquirer.select(
        message="Action:",
        choices=[
            Choice("SWITCH", "▶  Switch active profile"),
            Choice("LIST",   "   List all profiles"),
            Choice("DELETE", "✕  Delete a profile"),
            Choice("BACK",   "↩  Back"),
        ],
    ).execute()

    if action == "SWITCH":
        switch_profile()
    elif action == "LIST":
        t = Table(box=box.SIMPLE_HEAD, border_style=BORDER_DIM, header_style=f"{C} bold")
        t.add_column("Profile")
        t.add_column("Status")
        for name in profiles:
            marker = f"[{OK}]● active[/{OK}]" if name == _active_profile else f"[{DIM}]○[/{DIM}]"
            t.add_row(name, marker)
        console.print(t)
    elif action == "DELETE":
        to_del = inquirer.select(
            message="Delete which profile?",
            choices=[Choice(k, k) for k in profiles],
        ).execute()
        if inquirer.confirm(message=f"Delete '{to_del}'?", default=False).execute():
            del profiles[to_del]
            _save_profiles(profiles)
            _ok(f"Deleted '{to_del}'.")


# ── GitHub API helpers ────────────────────────────────────────────────────────

def _get_json(url: str, params: dict | None = None) -> tuple[int, Any]:
    try:
        r = requests.get(url, headers=get_headers(), params=params, timeout=15)
        return r.status_code, (r.json() if r.content else None)
    except requests.RequestException as exc:
        _err(f"Network error: {exc}")
        return 0, None


def _fetch_paginated(url: str, params: dict | None = None, max_pages: int = 20) -> list:
    results: list = []
    p = dict(params or {})
    p.setdefault("per_page", 100)
    for page in range(1, max_pages + 1):
        p["page"] = page
        status, data = _get_json(url, params=p)
        if status != 200 or not data:
            break
        results.extend(data)
        if len(data) < p["per_page"]:
            break
    return results


def fetch_all_repos(username: str) -> list | None:
    repos: list = []
    page = 1
    while True:
        status, data = _get_json(
            f"{GITHUB_API}/users/{username}/repos",
            params={"per_page": 100, "page": page, "sort": "updated"},
        )
        if status == 404:
            _err("User or organization not found.")
            return None
        if status == 403:
            _err("API rate limit hit — add a token via Setup Token.")
            return None
        if status != 200:
            _err(f"Could not fetch repositories (HTTP {status}).")
            return None
        if not data:
            break
        repos.extend(data)
        if len(data) < 100:
            break
        page += 1
    return repos


def get_branches(owner: str, repo: str) -> list[str]:
    data = _fetch_paginated(f"{GITHUB_API}/repos/{owner}/{repo}/branches")
    return [b["name"] for b in data] or ["main"]


# ── Repo browser ──────────────────────────────────────────────────────────────

def browse_repos() -> None:
    _rule("Browse Repositories")
    username = inquirer.text(message="GitHub user / org:").execute().strip()
    if not username:
        return

    with _status(f"Fetching repos for  {username} ..."):
        repos = fetch_all_repos(username)
    if repos is None:
        return
    if not repos:
        _warn("No public repositories found.")
        return

    _ok(f"Found {len(repos)} repositor{'y' if len(repos) == 1 else 'ies'}.")

    q = inquirer.text(message="Filter by name / description  (blank = all):").execute().strip()
    if q:
        ql = q.lower()
        repos = [
            r for r in repos
            if ql in r["name"].lower() or ql in (r.get("description") or "").lower()
        ]
        if not repos:
            _warn("No repositories matched.")
            return

    repo_choices = []
    for r in repos:
        vis   = f"[{DIM}]private [/{DIM}]" if r.get("private") else ""
        lang  = f"[{BD}]{r['language']}[/{BD}]" if r.get("language") else f"[{DIM}]—[/{DIM}]"
        stars = f"[{CD}]★ {r.get('stargazers_count', 0)}[/{CD}]"
        label = f"{vis}[bold white]{r['name']}[/bold white]  {lang}  {stars}"
        repo_choices.append(Choice(r, label))

    repo = inquirer.select(message="Select repository:", choices=repo_choices).execute()

    # ── Repo card ─────────────────────────────────────────────────────────────
    console.print()
    rows = [
        ("Repo",          repo["full_name"]),
        ("Description",   repo.get("description") or "—"),
        ("Language",      repo.get("language") or "—"),
        ("Stars / Forks", f"★ {repo.get('stargazers_count',0)}  /  ⑂ {repo.get('forks_count',0)}"),
        ("Open issues",   str(repo.get("open_issues_count", 0))),
        ("Default branch",repo.get("default_branch", "main")),
        ("License",       (repo.get("license") or {}).get("spdx_id") or "—"),
        ("URL",           repo.get("html_url", "—")),
    ]
    _panel(_kv_table(rows), title=f"  {repo['name']}  ", border=BORDER_MAIN)
    console.print()

    action = inquirer.select(
        message="What to do?",
        choices=[
            Choice("BROWSE",  "  Browse Files"),
            Choice("SEARCH",  "  Search Code"),
            Choice("ISSUES",  "  Issues & Pull Requests"),
            Choice("STATS",   "  Stats & Insights"),
            Choice("BACK",    "↩  Back"),
        ],
    ).execute()

    owner = username
    if action == "BROWSE":
        branches = get_branches(owner, repo["name"])
        default  = repo.get("default_branch", "main")
        branch   = inquirer.select(
            message="Branch:",
            choices=[Choice(b, f"{'▶ ' if b == default else '  '}{b}") for b in branches],
            default=default,
        ).execute()
        browse_files(owner, repo["name"], branch=branch)
    elif action == "SEARCH":
        search_code(owner, repo["name"])
    elif action == "ISSUES":
        browse_issues_prs(owner, repo["name"])
    elif action == "STATS":
        show_repo_stats(owner, repo["name"])


# ── File browser + preview ────────────────────────────────────────────────────

_PREVIEWABLE = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".css", ".scss",
    ".json", ".yaml", ".yml", ".toml", ".md", ".txt", ".sh", ".bash",
    ".rs", ".go", ".java", ".c", ".cpp", ".h", ".rb", ".php",
    ".env", ".gitignore", ".makefile", ".dockerfile", ".xml", ".svg",
    ".ini", ".cfg", ".conf",
}
_MAX_PREVIEW_BYTES = 50_000

_LEXER_MAP = {
    ".py": "python",  ".js": "javascript", ".ts": "typescript",
    ".tsx": "tsx",    ".jsx": "jsx",        ".html": "html",
    ".css": "css",    ".scss": "scss",      ".json": "json",
    ".yaml": "yaml",  ".yml": "yaml",       ".toml": "toml",
    ".md": "markdown",".sh": "bash",        ".bash": "bash",
    ".rs": "rust",    ".go": "go",          ".java": "java",
    ".c": "c",        ".cpp": "cpp",        ".h": "c",
    ".rb": "ruby",    ".php": "php",        ".xml": "xml",
    ".svg": "xml",    ".ini": "ini",        ".cfg": "ini",
}


def _guess_lexer(filename: str) -> str:
    return _LEXER_MAP.get(Path(filename).suffix.lower(), "text")


def _render_preview(content: str, filename: str, size: int) -> None:
    syntax = Syntax(
        content, _guess_lexer(filename),
        theme="monokai", line_numbers=True, word_wrap=False,
    )
    _panel(syntax, title=f"  {filename}  ({size:,} B)  ", border=BORDER_CODE)


def preview_file(item: dict) -> None:
    size = item.get("size", 0)
    ext  = Path(item["name"]).suffix.lower()

    if size > _MAX_PREVIEW_BYTES:
        _warn(f"File is {size:,} bytes — too large to preview.")
        _info(item.get("html_url", ""))
        _back_prompt(); return

    if ext not in _PREVIEWABLE:
        _warn(f"Binary / unsupported type '{ext or '(none)'}' — cannot preview.")
        _info(item.get("html_url", ""))
        _back_prompt(); return

    with _status(f"Loading  {item['name']} ..."):
        status, data = _get_json(item["url"])

    if status != 200 or not isinstance(data, dict):
        _err(f"Could not fetch file (HTTP {status}).")
        _back_prompt(); return

    try:
        content = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
    except Exception as exc:
        _err(f"Decode error: {exc}")
        _back_prompt(); return

    _render_preview(content, item["name"], size)
    _back_prompt()


def browse_files(username: str, selected_repo: str, branch: str = "main") -> None:
    current_path = ""

    while True:
        with _status("Loading directory..."):
            url    = f"{GITHUB_API}/repos/{username}/{selected_repo}/contents/{current_path}"
            status, contents = _get_json(url, params={"ref": branch})

        if status != 200 or not isinstance(contents, list):
            _err("Could not load directory. (Empty repo?)")
            break

        contents.sort(key=lambda x: (0 if x["type"] == "dir" else 1, x["name"].lower()))

        # breadcrumb header
        crumb = (
            f"[{CG}]{selected_repo}[/{CG}]"
            f"[{DIM}]/{current_path}[/{DIM}]"
            f"  [bold {BD}]@{branch}[/bold {BD}]"
        )
        console.print(f"\n  {crumb}")
        console.print(f"  [{DIM}]{'─' * 48}[/{DIM}]")

        choices: list = []
        if current_path:
            choices.append(Choice("..", f"[{CD}]↑  ..[/{CD}]"))

        for item in contents:
            if item["type"] == "dir":
                label = f"[{CG}]▸  {item['name']}/[/{CG}]"
            else:
                sz    = f"[{DIM}]  {item['size']:,} B[/{DIM}]"
                label = f"[{WHT}]   {item['name']}[/{WHT}]{sz}"
            choices.append(Choice(item, label))

        choices.append(Choice("CLONE", f"[{OK}]  Clone this path[/{OK}]"))
        choices.append(Choice("BACK",  f"[{DIM}]↩  Back[/{DIM}]"))

        sel = inquirer.select(message="", choices=choices).execute()

        if sel == "BACK":
            break
        elif sel == "CLONE":
            clone_and_edit(username, selected_repo, current_path, branch)
            break
        elif sel == "..":
            current_path = "/".join(current_path.split("/")[:-1])
        elif isinstance(sel, dict):
            if sel["type"] == "dir":
                current_path = sel["path"]
            else:
                preview_file(sel)


# ── Clone, commit & push ──────────────────────────────────────────────────────

def _credential_args(token: str | None) -> list[str]:
    if not token:
        return []
    helper = f"!f() {{ echo username=token; echo password={token}; }}; f"
    return ["-c", f"credential.helper={helper}"]


def _run_git(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    result = subprocess.run(list(args), capture_output=True, cwd=cwd)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, args, result.stdout, result.stderr)
    return result


def clone_and_edit(owner: str, repo: str, path: str, branch: str) -> None:
    _rule("Clone")
    token     = _safe_token()
    cred_args = _credential_args(token)
    repo_url  = f"https://github.com/{owner}/{repo}.git"

    folder_name = path.split("/")[-1] if path else repo
    target_dir  = Path(f"./{repo}_{folder_name}_clone").resolve()

    if target_dir.exists():
        if not inquirer.confirm(
            message=f"'{target_dir.name}' exists. Overwrite?", default=False
        ).execute():
            _warn("Clone cancelled.")
            return
        shutil.rmtree(target_dir)

    _info(f"Source   {owner}/{repo}  /{path or '(root)'}  @  {branch}")
    _info(f"Target   {target_dir}\n")

    try:
        with _status("Cloning..."):
            _run_git(
                "git", *cred_args,
                "clone", "--no-checkout", "--depth", "1", "--branch", branch,
                repo_url, str(target_dir),
            )
        with _status("Configuring sparse-checkout..."):
            _run_git("git", "sparse-checkout", "init", "--cone", cwd=target_dir)
            _run_git("git", "sparse-checkout", "set", path or ".", cwd=target_dir)
        with _status(f"Checking out  {branch} ..."):
            _run_git("git", "checkout", branch, cwd=target_dir)

        rows = [
            ("Path",   path or "/"),
            ("Repo",   f"{owner}/{repo}"),
            ("Branch", branch),
            ("Saved",  str(target_dir)),
        ]
        _panel(_kv_table(rows), title="  Cloned  ", border=BORDER_OK)

    except subprocess.CalledProcessError as exc:
        err = exc.stderr.decode(errors="replace").strip() if exc.stderr else str(exc)
        _err(f"Git error: {err}")
        return

    if inquirer.confirm(message="Open in editor now?", default=True).execute():
        editor = os.environ.get("EDITOR", "code")
        try:
            subprocess.Popen([editor, str(target_dir)])
            _ok(f"Launched  {editor}")
        except FileNotFoundError:
            _err(f"Editor '{editor}' not found. Set $EDITOR.")

    if inquirer.confirm(message="Queue a commit & push?", default=False).execute():
        commit_and_push(target_dir)


def commit_and_push(target_dir: Path | None = None) -> None:
    _rule("Commit & Push")

    if target_dir is None:
        path_str   = inquirer.text(message="Path to local repo:").execute().strip()
        target_dir = Path(path_str).expanduser().resolve()

    if not (target_dir / ".git").exists():
        _err("Not a git repository.")
        return

    result = subprocess.run(
        ["git", "status", "--short"], capture_output=True, text=True, cwd=target_dir
    )
    if not result.stdout.strip():
        _ok("Nothing to commit — working tree is clean.")
        return

    _panel(
        f"[{CD}]{result.stdout.strip()}[/{CD}]",
        title="  Changed Files  ",
        border=BORDER_WARN,
    )

    stage = inquirer.select(
        message="Stage:",
        choices=[
            Choice("ALL",  "  Stage everything  (git add -A)"),
            Choice("PICK", "  Choose files interactively"),
        ],
    ).execute()

    if stage == "ALL":
        subprocess.run(["git", "add", "-A"], cwd=target_dir, check=True)
    else:
        files_raw = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True, cwd=target_dir
        ).stdout.strip().splitlines()
        file_choices = [Choice(line[3:].strip(), line) for line in files_raw if line.strip()]
        selected = inquirer.checkbox(message="Select files:", choices=file_choices).execute()
        for f in selected:
            subprocess.run(["git", "add", "--", f], cwd=target_dir, check=True)

    msg = inquirer.text(message="Commit message:").execute().strip()
    if not msg:
        _warn("Empty message — aborted.")
        return

    try:
        _run_git("git", "commit", "-m", msg, cwd=target_dir)
        _ok(f"Committed: {msg}")
    except subprocess.CalledProcessError as exc:
        err = exc.stderr.decode(errors="replace").strip() if exc.stderr else str(exc)
        _err(f"Commit failed: {err}")
        return

    if inquirer.confirm(message="Push to remote?", default=True).execute():
        cred_args = _credential_args(_safe_token())
        try:
            with _status("Pushing..."):
                _run_git("git", *cred_args, "push", cwd=target_dir)
            _ok("Pushed successfully.")
        except subprocess.CalledProcessError as exc:
            err = exc.stderr.decode(errors="replace").strip() if exc.stderr else str(exc)
            _err(f"Push failed: {err}")


# ── Code search ───────────────────────────────────────────────────────────────

def search_code(owner: str, repo: str) -> None:
    _rule(f"Search Code  ·  {owner}/{repo}")
    query = inquirer.text(message="Query:").execute().strip()
    if not query:
        return

    with _status("Searching..."):
        status, data = _get_json(
            f"{GITHUB_API}/search/code",
            params={"q": f"{query} repo:{owner}/{repo}", "per_page": 30},
        )

    if status == 422:
        _err("Too vague — try a more specific keyword.")
        return
    if status == 403:
        _err("Search rate-limit hit. Wait a moment or add a token.")
        return
    if status != 200 or not isinstance(data, dict):
        _err(f"Search error (HTTP {status}).")
        return

    items = data.get("items", [])
    total = data.get("total_count", 0)
    _ok(f"{total:,} result(s) — showing top {len(items)}.")
    if not items:
        return

    result_choices = [Choice(item, f"[{WHT}]{item['path']}[/{WHT}]") for item in items]
    result_choices.append(Choice("BACK", f"[{DIM}]↩  Back[/{DIM}]"))

    while True:
        sel = inquirer.select(message="File:", choices=result_choices).execute()
        if sel == "BACK":
            break

        with _status(f"Loading  {sel['path']} ..."):
            s2, d2 = _get_json(sel["url"])

        if s2 == 200 and isinstance(d2, dict):
            try:
                content = base64.b64decode(d2["content"]).decode("utf-8", errors="replace")
                _render_preview(content, sel["path"], d2.get("size", 0))
            except Exception as exc:
                _err(f"Could not decode: {exc}")
        else:
            _err(f"Could not fetch file (HTTP {s2}).")

        _back_prompt()


# ── Issues & Pull Requests ────────────────────────────────────────────────────

def browse_issues_prs(owner: str, repo: str) -> None:
    kind = inquirer.select(
        message="Browse:",
        choices=[Choice("issues", "  Issues"), Choice("pulls", "  Pull Requests")],
    ).execute()

    state = inquirer.select(
        message="State:",
        choices=[
            Choice("open",   f"[{OK}]Open[/{OK}]"),
            Choice("closed", f"[{ERR}]Closed[/{ERR}]"),
            Choice("all",    "All"),
        ],
    ).execute()

    label_filter = inquirer.text(message="Label filter (blank = all):").execute().strip()
    params: dict = {"state": state, "per_page": 50}
    if label_filter:
        params["labels"] = label_filter

    endpoint = "issues" if kind == "issues" else "pulls"
    _rule(f"{kind.title()}  ·  {owner}/{repo}")

    with _status(f"Fetching {endpoint}..."):
        items = _fetch_paginated(
            f"{GITHUB_API}/repos/{owner}/{repo}/{endpoint}",
            params=params, max_pages=3,
        )

    if not items:
        _warn(f"No {endpoint} found.")
        return

    _STATE_COLOR = {"open": OK, "closed": ERR}

    item_choices = []
    for item in items:
        sc     = _STATE_COLOR.get(item["state"], DIM)
        dot    = f"[{sc}]●[/{sc}]"
        num    = f"[{DIM}]#{item['number']}[/{DIM}]"
        title  = f"[{WHT}]{item['title']}[/{WHT}]"
        author = f"[{DIM}]{item.get('user', {}).get('login','?')}[/{DIM}]"
        cmt    = f"[{DIM}]💬 {item.get('comments',0)}[/{DIM}]"
        item_choices.append(Choice(item, f"{dot}  {num}  {title}  {author}  {cmt}"))
    item_choices.append(Choice("BACK", f"[{DIM}]↩  Back[/{DIM}]"))

    while True:
        sel = inquirer.select(message=f"Select {kind[:-1]}:", choices=item_choices).execute()
        if sel == "BACK":
            break

        sc   = _STATE_COLOR.get(sel["state"], DIM)
        rows = [
            ("Number",    f"#{sel['number']}"),
            ("Title",     sel["title"]),
            ("State",     f"[{sc}]{sel['state']}[/{sc}]"),
            ("Author",    sel.get("user", {}).get("login", "?")),
            ("Created",   sel.get("created_at", "?")[:10]),
            ("Updated",   sel.get("updated_at", "?")[:10]),
            ("Labels",    ", ".join(lb["name"] for lb in sel.get("labels", [])) or "—"),
            ("Assignees", ", ".join(a["login"] for a in sel.get("assignees", [])) or "—"),
            ("URL",       sel.get("html_url", "?")),
        ]
        if sel.get("merged_at"):
            rows.append(("Merged", sel["merged_at"][:10]))

        _panel(_kv_table(rows), title=f"  #{sel['number']}  ", border=BORDER_MAIN)
        _panel(sel.get("body") or "_No description._", title="  Body  ", border=BORDER_DIM)

        if sel.get("comments", 0) > 0 and inquirer.confirm(
            message=f"Load {sel['comments']} comment(s)?", default=False
        ).execute():
            with _status("Fetching comments..."):
                c_st, cdata = _get_json(sel["comments_url"])
            if c_st == 200 and isinstance(cdata, list):
                for c in cdata[:10]:
                    author  = c.get("user", {}).get("login", "?")
                    created = c.get("created_at", "")[:10]
                    _panel(
                        (c.get("body") or "")[:1000],
                        title=f"  {author}  ·  {created}  ",
                        border=BORDER_DIM,
                    )

        _back_prompt()


# ── Repo stats ────────────────────────────────────────────────────────────────

def show_repo_stats(owner: str, repo: str) -> None:
    _rule(f"Stats & Insights  ·  {owner}/{repo}")
    choice = inquirer.select(
        message="View:",
        choices=[
            Choice("CONTRIBUTORS", "  Top Contributors"),
            Choice("LANGUAGES",    "  Language Breakdown"),
            Choice("ACTIVITY",     "  Commit Activity  (last 26 weeks)"),
            Choice("ALL",          "  All of the above"),
            Choice("BACK",         "↩  Back"),
        ],
    ).execute()

    if choice == "BACK":
        return
    if choice in ("CONTRIBUTORS", "ALL"):
        _show_contributors(owner, repo)
    if choice in ("LANGUAGES", "ALL"):
        _show_languages(owner, repo)
    if choice in ("ACTIVITY", "ALL"):
        _show_commit_activity(owner, repo)


def _show_contributors(owner: str, repo: str) -> None:
    with _status("Fetching contributors..."):
        data = _fetch_paginated(f"{GITHUB_API}/repos/{owner}/{repo}/contributors", max_pages=1)
    if not data:
        _warn("No contributor data available.")
        return

    data = data[:20]
    top  = data[0]["contributions"] if data else 1

    t = Table(
        title=f"[{C}]  Top Contributors[/{C}]",
        box=box.SIMPLE_HEAD, border_style=BORDER_DIM, header_style=f"{CD} bold",
    )
    t.add_column("#",       style=DIM, width=4)
    t.add_column("Login",   style=f"bold {WHT}")
    t.add_column("Commits", justify="right", style=CD)
    t.add_column("Share",   min_width=24)

    for i, c in enumerate(data, 1):
        commits = c["contributions"]
        bar_w   = max(1, int(commits / top * 22))
        bar     = f"[{CG}]{'█' * bar_w}[/{CG}][{DIM}]{'░' * (22 - bar_w)}[/{DIM}]"
        t.add_row(str(i), c["login"], f"{commits:,}", bar)
    console.print(t)


# Vivid but distinct per-language colours
_LANG_COLORS = [CG, "bright_blue", "green", "magenta", "yellow", "red", "white", "bright_cyan"]


def _show_languages(owner: str, repo: str) -> None:
    with _status("Fetching language stats..."):
        status, data = _get_json(f"{GITHUB_API}/repos/{owner}/{repo}/languages")
    if status != 200 or not data:
        _warn("No language data available.")
        return

    total = sum(data.values()) or 1
    t = Table(
        title=f"[{C}]  Language Breakdown[/{C}]",
        box=box.SIMPLE_HEAD, border_style=BORDER_DIM, header_style=f"{CD} bold",
    )
    t.add_column("Language", style=f"bold {WHT}")
    t.add_column("Bytes",    justify="right", style=DIM)
    t.add_column("%",        justify="right", style=CD)
    t.add_column("Bar",      min_width=28)

    for idx, (lang, bytes_) in enumerate(sorted(data.items(), key=lambda x: -x[1])):
        pct   = bytes_ / total * 100
        color = _LANG_COLORS[idx % len(_LANG_COLORS)]
        bar_w = max(1, int(pct / 4))
        bar   = f"[{color}]{'█' * bar_w}[/{color}][{DIM}]{'░' * max(0, 25 - bar_w)}[/{DIM}]"
        t.add_row(lang, f"{bytes_:,}", f"{pct:.1f}%", bar)
    console.print(t)


def _show_commit_activity(owner: str, repo: str) -> None:
    with _status("Fetching commit activity..."):
        status, data = _get_json(f"{GITHUB_API}/repos/{owner}/{repo}/stats/commit_activity")

    if status == 202:
        time.sleep(3)
        with _status("Still computing — retrying..."):
            status, data = _get_json(f"{GITHUB_API}/repos/{owner}/{repo}/stats/commit_activity")

    if status != 200 or not data:
        _warn("Not ready yet — try again in a moment.")
        return

    weeks     = data[-26:]
    max_total = max((w["total"] for w in weeks), default=1) or 1

    t = Table(
        title=f"[{C}]  Commit Activity — Last 26 Weeks[/{C}]",
        box=box.SIMPLE_HEAD, border_style=BORDER_DIM, header_style=f"{CD} bold",
    )
    t.add_column("Week ending", style=DIM)
    t.add_column("Commits",     justify="right", style=CD)
    t.add_column("Activity",    min_width=34)

    for w in weeks:
        dt    = datetime.datetime.utcfromtimestamp(w["week"]).strftime("%Y-%m-%d")
        total = w["total"]
        bar_w = int(total / max_total * 30)
        ratio = total / max_total if max_total else 0
        color = CG if ratio >= 0.7 else (CD if ratio >= 0.3 else DIM)
        bar   = f"[{color}]{'█' * bar_w}[/{color}]" if bar_w else f"[{DIM}]·[/{DIM}]"
        t.add_row(dt, str(total), bar)
    console.print(t)


# ── Main menu ─────────────────────────────────────────────────────────────────

def main() -> None:
    _banner()

    while True:
        token     = _safe_token()
        auth_pill = (
            f"[{OK}]● {_active_profile}[/{OK}]"
            if token
            else f"[{ERR}]● unauthenticated  [{DIM}](60 req/hr)[/{DIM}][/{ERR}]"
        )
        console.print(f"  [{DIM}]profile:[/{DIM}] {auth_pill}\n")

        action = inquirer.select(
            message="",
            choices=[
                Choice("BROWSE",   "  Browse Repositories"),
                Choice("PUSH",     "  Commit & Push"),
                Choice("AUTH",     "  Setup Token"),
                Choice("PROFILES", "  Manage Profiles"),
                Choice("EXIT",     "↩  Exit"),
            ],
        ).execute()

        console.print()

        if action == "EXIT":
            _rule()
            console.print(f"\n  [{CD}]Goodbye from Octo. 🐙[/{CD}]\n")
            sys.exit(0)
        elif action == "AUTH":
            setup_auth()
        elif action == "PROFILES":
            manage_profiles()
        elif action == "BROWSE":
            browse_repos()
        elif action == "PUSH":
            commit_and_push()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print(f"\n\n  [{CD}]Interrupted — see you next time. 🐙[/{CD}]\n")
        sys.exit(0)
