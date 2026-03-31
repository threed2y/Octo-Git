<div align="center">

```
   ██████╗  ██████╗████████╗ ██████╗
  ██╔═══██╗██╔════╝╚══██╔══╝██╔═══██╗
  ██║   ██║██║        ██║   ██║   ██║
  ██║   ██║██║        ██║   ██║   ██║
  ╚██████╔╝╚██████╗   ██║   ╚██████╔╝
   ╚═════╝  ╚═════╝   ╚═╝    ╚═════╝
```

**Eight arms. One terminal. All of GitHub.**

[![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-cyan?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.1.0-brightcyan?style=flat-square)](CHANGELOG.md)

</div>

---

Octo is a fully interactive, terminal-native GitHub companion. Browse repos, preview files with syntax highlighting, clone specific subdirectories, commit and push changes, search code, read issues and pull requests, and inspect contributor stats — all without leaving your shell or opening a browser.

## ✦ Features

| | Feature | Description |
|---|---|---|
| 📂 | **Repo browser** | Browse any public or private repo with live filtering by name or description |
| 📄 | **File preview** | Inline syntax-highlighted preview for 40+ file types (Monokai theme, line numbers) |
| 🔽 | **Sparse checkout** | Clone any subdirectory — not the whole repo — directly from the file browser |
| ⬆️  | **Commit & push** | Stage files, write a commit message, and push from any local clone |
| 🔍 | **Code search** | Search across all files in a repo using GitHub's Search API |
| 🐛 | **Issues & PRs** | Browse open/closed issues and pull requests, read bodies and comment threads |
| 📊 | **Repo stats** | Contributor bar charts, language breakdown, and 26-week commit activity histogram |
| 👤 | **Multi-account** | Named token profiles (`default`, `work`, `personal`) — switch in one keystroke |

---

## ◎ Preview

### Main menu

```
   ██████╗  ██████╗████████╗ ██████╗
  ██╔═══██╗██╔════╝╚══██╔══╝██╔═══██╗
  ██║   ██║██║        ██║   ██║   ██║
  ██║   ██║██║        ██║   ██║   ██║
  ╚██████╔╝╚██████╗   ██║   ╚██████╔╝
   ╚═════╝  ╚═════╝   ╚═╝    ╚═════╝

  eight arms. one terminal. all of github.   v1.1.0

  profile: ● default

❯   Browse Repositories
    Commit & Push
    Setup Token
    Manage Profiles
  ↩  Exit
```

### Repo card

```
╭─────────────────────────────  django-rest-framework  ──────────────────────────────╮
│  Repo           encode/django-rest-framework                                        │
│  Description    Web APIs for Django                                                 │
│  Language       Python                                                              │
│  Stars / Forks  ★ 28,241  /  ⑂ 6,892                                               │
│  Open issues    172                                                                 │
│  Default branch main                                                                │
│  License        BSD-2-Clause                                                        │
│  URL            https://github.com/encode/django-rest-framework                     │
╰─────────────────────────────────────────────────────────────────────────────────────╯
```

### File browser

```
  django-rest-framework/rest_framework  @main
  ────────────────────────────────────────────────

  ▸  authentication/
  ▸  compat/
  ▸  renderers/
     __init__.py            142 B
     authentication.py    8,204 B
     decorators.py        3,018 B
     exceptions.py        5,671 B
     fields.py           62,310 B
     permissions.py       8,903 B
     serializers.py      53,012 B
     views.py            14,445 B

    Clone this path
  ↩  Back
```

### Contributor stats

```
  Top Contributors
 ─────────────────────────────────────────────────────
  #   Login           Commits   Share
  1   tomchristie      2,847    ████████████████████░░
  2   xordoquy           312    ███░░░░░░░░░░░░░░░░░░░
  3   carltongibson      289    ██░░░░░░░░░░░░░░░░░░░░
  4   kevin-brown        201    █░░░░░░░░░░░░░░░░░░░░░
  5   encode-bot         178    █░░░░░░░░░░░░░░░░░░░░░
```

### Language breakdown

```
  Language Breakdown
 ──────────────────────────────────────────────────────────
  Language    Bytes          %      Bar
  Python      1,243,018   91.4%    ████████████████████████░
  HTML           47,201    3.5%    █░░░░░░░░░░░░░░░░░░░░░░░░
  JavaScript     38,904    2.9%    █░░░░░░░░░░░░░░░░░░░░░░░░
  Shell          14,220    1.0%    ░░░░░░░░░░░░░░░░░░░░░░░░░
  Makefile        6,101    0.4%    ░░░░░░░░░░░░░░░░░░░░░░░░░
```

### Commit activity

```
  Commit Activity — Last 26 Weeks
 ──────────────────────────────────────────────────────────────
  Week ending   Commits   Activity
  2024-10-07         31   ██████████░░░░░░░░░░░░░░░░░░░░
  2024-10-14         47   ███████████████░░░░░░░░░░░░░░░
  2024-10-21         58   ██████████████████░░░░░░░░░░░░
  2024-10-28         89   ████████████████████████████░░
  2024-11-04         94   ██████████████████████████████
  2024-11-11         62   ████████████████████░░░░░░░░░░
  2024-11-18         21   ███████░░░░░░░░░░░░░░░░░░░░░░░
```

---

## ⬡ Installation

**Requirements:** Python 3.10 or later · `git` on your PATH

### Step 1 — Get the project

**Option A — from the zip:**
```bash
unzip octo_project.zip
cd octo
```

**Option B — clone from GitHub:**
```bash
git clone https://github.com/your-username/octo.git
cd octo
```

### Step 2 — Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

| Platform | Command |
|---|---|
| macOS / Linux | `source .venv/bin/activate` |
| Windows (CMD) | `.venv\Scripts\activate.bat` |
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |

Your prompt will show `(.venv)` when it's active.

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Run

```bash
python -m octo
```

> **Optional — install as a shell command**
>
> If you want to type `octo` from any directory instead of `python -m octo`, run:
> ```bash
> pip install -e .
> ```
> This installs Octo into your virtual environment as a command. You only need to do this once.

---

## ◈ Authentication

Octo works without a token, but GitHub limits unauthenticated requests to **60 per hour**. Adding a Personal Access Token raises this to **5,000 per hour** and unlocks private repositories.

### Generate a token

1. Go to **GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)**
2. Click **Generate new token (classic)**
3. Give it a name — e.g. `octo-cli`
4. Check the **`repo`** scope. Add **`read:org`** if you want to browse organisation repos
5. Click **Generate token** and copy it — you won't be shown it again

### Add the token to Octo

```
Main menu  →  Setup Token
```

Enter a profile name (e.g. `default`) and paste your token when prompted. Octo validates it immediately against the GitHub API and shows your authenticated username on success.

Tokens are stored in `~/.octo_profiles.json` with `0600` permissions on Unix (owner read/write only). The token is never embedded in process arguments and will not appear in `ps aux` or shell history.

### Multiple accounts

Save multiple tokens under different profile names and switch between them at any time:

```
Main menu  →  Setup Token           # repeat with a different profile name
Main menu  →  Manage Profiles  →  Switch active profile
```

Profile names are arbitrary — `default`, `work`, `oss`, anything you like.

---

## ◈ Usage

### Keyboard controls

| Key | Action |
|-----|--------|
| `↑` / `↓` | Move through options |
| `Enter` | Select / confirm |
| `Space` | Toggle a checkbox (used in file staging) |
| `Ctrl-C` | Cancel / exit at any point |

### Browse repositories

1. Select **Browse Repositories** from the main menu
2. Enter a GitHub username or organisation name (e.g. `django`, `microsoft`)
3. Optionally type a keyword to filter repos by name or description — press Enter with a blank input to show all
4. Select a repo — a summary card appears showing stars, forks, language, and license
5. Choose what to do: **Browse Files**, **Search Code**, **Issues & PRs**, or **Stats & Insights**

### Browse files & preview

Navigate the directory tree with the arrow keys. Folders are prefixed with `▸`. Selecting a file opens an inline syntax-highlighted preview (up to 50 KB, with line numbers).

Supported preview types include `.py` `.js` `.ts` `.go` `.rs` `.java` `.c` `.cpp` `.rb` `.php` `.html` `.css` `.json` `.yaml` `.toml` `.md` `.sh` `.xml` `.svg` `.ini` and more.

### Sparse checkout — clone a specific folder

Navigate to any folder in the file browser and select **Clone this path**. Octo uses `git sparse-checkout` to download only that subdirectory — not the entire repository. This is much faster for large repos.

```
Browse Files  →  navigate into any folder  →  Clone this path
```

The clone is saved as `./<repo>_<folder>_clone/` in your current working directory. Octo will ask if you want to open it in your `$EDITOR` immediately after.

### Commit & push

Available from the main menu, or automatically offered after a sparse checkout.

1. Select **Commit & Push** from the main menu
2. Enter the path to your local git repository
3. Octo shows all changed files — choose to stage everything or pick files individually
4. Enter a commit message
5. Octo commits and asks if you want to push to the remote

### Search code

```
Browse  →  select repo  →  Search Code
```

Type a keyword and Octo searches all files in that repository using GitHub's Search API. Results list matching file paths. Select any file to load its full content with syntax highlighting.

### Issues & Pull Requests

```
Browse  →  select repo  →  Issues & Pull Requests
```

Choose between Issues and Pull Requests, filter by state (open / closed / all) and optionally by label. Select any item to read its full body and optionally load up to 10 comment threads inline.

### Repo stats

```
Browse  →  select repo  →  Stats & Insights
```

Choose one view or all three at once:

- **Top Contributors** — ranked list with proportional fill bars
- **Language Breakdown** — bytes, percentage, and colour-coded bar per language
- **Commit Activity** — 26-week histogram, bars heat-coded by activity level

---

## ◈ Project structure

```
octo/
├── octo/
│   ├── __init__.py        # Package metadata
│   ├── __main__.py        # Enables python -m octo
│   └── core.py            # All application logic
├── docs/
│   └── preview_main.txt   # ASCII preview reference
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── pyproject.toml         # Package config and optional entry point
└── requirements.txt       # Runtime dependencies
```

---

## ◈ Dependencies

| Package | Version | Purpose |
|---|---|---|
| [requests](https://github.com/psf/requests) | ≥ 2.31 | GitHub API HTTP calls |
| [rich](https://github.com/Textualize/rich) | ≥ 13.7 | Terminal UI — panels, tables, syntax highlighting |
| [InquirerPy](https://github.com/kazhala/InquirerPy) | ≥ 0.3.4 | Interactive menus and prompts |

All three are pure-Python and install without any system-level dependencies.

---

## ◈ Security

- **Token storage** — `~/.octo_profiles.json` is written with `0600` permissions on Unix (owner read/write only). Tokens are never logged or printed to the terminal.
- **Process safety** — Git authentication uses a transient credential helper passed via `-c credential.helper=...`. The token does not appear in `ps`, `top`, or shell history.
- **No telemetry** — Octo makes no network requests beyond the GitHub API calls you explicitly trigger.

---

## ◈ Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the development setup and code style guidelines.

---

## ◈ License

[MIT](LICENSE) © 2025 Octo contributors
