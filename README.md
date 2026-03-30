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
[![Version](https://img.shields.io/badge/version-1.0.0-brightcyan?style=flat-square)](CHANGELOG.md)
[![Code style: rich](https://img.shields.io/badge/UI-rich%20%2B%20InquirerPy-blueviolet?style=flat-square)](https://github.com/Textualize/rich)

</div>

---

Octo is a fully interactive, terminal-native GitHub companion. Browse repos, preview files with syntax highlighting, clone subdirectories, commit and push changes, search code, read issues and pull requests, and inspect contributor stats — all without leaving your shell or opening a browser.

## ✦ Features

| | Feature | Description |
|---|---|---|
| 📂 | **Repo browser** | Browse any public or private repo with live filtering by name or description |
| 📄 | **File preview** | Inline syntax-highlighted preview for 40+ file types (Monokai theme, line numbers) |
| 🔽 | **Sparse checkout** | Clone any subdirectory — not the whole repo — directly from the file browser |
| ⬆️ | **Commit & push** | Stage files, write a commit message, and push from any local clone |
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

  eight arms. one terminal. all of github.   v1.0.0

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
     mixins.py            4,229 B
     pagination.py       22,884 B
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
  Language    Bytes        %      Bar
  Python      1,243,018   91.4%  ████████████████████████░
  HTML           47,201    3.5%  █░░░░░░░░░░░░░░░░░░░░░░░░
  JavaScript     38,904    2.9%  █░░░░░░░░░░░░░░░░░░░░░░░░
  Shell          14,220    1.0%  ░░░░░░░░░░░░░░░░░░░░░░░░░
  Makefile        6,101    0.4%  ░░░░░░░░░░░░░░░░░░░░░░░░░
```

### Commit activity

```
  Commit Activity — Last 26 Weeks
 ──────────────────────────────────────────────────────────────
  Week ending   Commits   Activity
  2024-09-30         12   ████░░░░░░░░░░░░░░░░░░░░░░░░░░
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

### From PyPI *(coming soon)*

```bash
pip install octo-cli
```

### From source

```bash
# 1. Clone
git clone https://github.com/your-username/octo.git
cd octo

# 2. Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install
pip install -e .

# 4. Run
octo
```

**Requirements:** Python 3.10 or later, `git` on your PATH.

---

## ◈ Authentication

Octo works unauthenticated (60 requests/hour via GitHub's public rate limit), but a Personal Access Token unlocks higher limits and private repository access.

**Generate a token:**

1. Go to **GitHub → Settings → Developer Settings → Personal Access Tokens (classic)**
2. Click **Generate new token**
3. Enable the `repo` scope (add `read:org` for organisation repos)
4. Copy the token

**Add it to Octo:**

```
octo  →  Setup Token
```

Tokens are stored in `~/.octo_profiles.json` with `600` permissions (owner read/write only). The token is **never** embedded in process arguments — Octo uses a transient Git credential helper so it doesn't appear in `ps aux` output.

### Multiple accounts

Octo supports named profiles so you can switch between personal and work tokens instantly:

```
octo  →  Manage Profiles  →  Switch active profile
```

Profile names are arbitrary strings: `default`, `work`, `oss`, etc.

---

## ◈ Usage

Run with:

```bash
octo
# or
python -m octo
```

### Navigation

Octo is fully keyboard-driven using arrow keys and Enter.

| Key | Action |
|-----|--------|
| `↑` / `↓` | Move selection |
| `Enter` | Confirm |
| `Space` | Toggle (checkboxes) |
| `Ctrl-C` | Exit at any point |

### Browse repositories

1. Select **Browse Repositories**
2. Enter a GitHub username or organisation name
3. Optionally type a filter string (matches name and description)
4. Select a repository — a summary card is shown
5. Choose an action: **Browse Files**, **Search Code**, **Issues & PRs**, or **Stats**

### Browse files & preview

Navigate the directory tree with arrow keys. Selecting a file opens an inline syntax-highlighted preview (up to 50 KB). Selecting **Clone this path** runs a sparse checkout of the current directory.

Supported preview types include: `.py` `.js` `.ts` `.go` `.rs` `.java` `.c` `.cpp` `.rb` `.php` `.html` `.css` `.json` `.yaml` `.toml` `.md` `.sh` `.xml` `.svg` `.ini` and more.

### Sparse checkout

Octo clones only the subdirectory you're browsing — not the full repository — using `git sparse-checkout`. This is significantly faster for large monorepos.

```
Browse Files  →  navigate to any folder  →  Clone this path
```

The clone is saved as `./<repo>_<folder>_clone/` in the current working directory. You're offered the option to open it in your `$EDITOR` immediately.

### Commit & push

After cloning (or from the main menu with any local git repo):

1. Select **Commit & Push**
2. Enter the path to your local repository
3. View changed files, choose to stage all or pick individually
4. Enter a commit message
5. Confirm push

### Search code

```
Browse  →  select repo  →  Search Code
```

Uses GitHub's `/search/code` API scoped to the selected repository. Results show matching file paths; selecting a file loads the full content with syntax highlighting.

### Issues & Pull Requests

```
Browse  →  select repo  →  Issues & Pull Requests
```

Filter by state (open / closed / all) and label. Select any item to read its full description and optionally load comment threads (up to 10 comments shown inline).

### Repo stats

```
Browse  →  select repo  →  Stats & Insights
```

Three views available individually or all at once:

- **Top Contributors** — ranked list with proportional bar chart
- **Language Breakdown** — bytes, percentage, and colour-coded bars
- **Commit Activity** — 26-week histogram with heat-coded bars

---

## ◈ Project structure

```
octo/
├── octo/
│   ├── __init__.py          # Package metadata
│   ├── __main__.py          # python -m octo entry point
│   └── core.py              # All application logic
├── docs/
│   └── preview_main.txt     # ASCII preview art
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── pyproject.toml           # Build config + package metadata
└── requirements.txt         # Pinned runtime + dev deps
```

---

## ◈ Dependencies

| Package | Version | Purpose |
|---|---|---|
| [requests](https://github.com/psf/requests) | ≥ 2.31 | GitHub API HTTP calls |
| [rich](https://github.com/Textualize/rich) | ≥ 13.7 | Terminal rendering (panels, tables, syntax) |
| [InquirerPy](https://github.com/kazhala/InquirerPy) | ≥ 0.3.4 | Interactive menus and prompts |

All three are pure-Python and install without system dependencies.

---

## ◈ Security

- **Token storage** — `~/.octo_profiles.json` is created with `0600` permissions (Unix). Tokens are never logged or printed.
- **Process safety** — Git operations authenticate via a transient in-process credential helper (`-c credential.helper=...`). The token does not appear in `ps`, `top`, or shell history.
- **No telemetry** — Octo makes no network requests other than the GitHub API calls you trigger explicitly.

---

## ◈ Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the development setup and code style guidelines.

---

## ◈ License

[MIT](LICENSE) © 2025 Octo contributors
