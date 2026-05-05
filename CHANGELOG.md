# Changelog

All notable changes to Octo are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.4.0] — 2026-05-05

### Added
- **Pull / Sync** — pull latest remote changes into any local clone directly
  from the main menu. Picks from clone history or accepts a manual path.
  Detects detached HEAD state and refuses gracefully instead of failing silently.
- **Branch Manager** — list all local and remote branches, switch branch,
  create a new branch from any base, delete with optional force flag. Current
  branch shown at every step.
- **View Local Diff** — `git diff` rendered inline with Monokai syntax
  highlighting before committing. Four modes: unstaged, staged, all vs HEAD,
  or between any two commits / branches.
- **Stash Manager** — stash changes (with optional message, includes untracked
  files), pop latest, apply a specific stash, drop, and list — all from a
  single interactive menu.
- **File download** — after previewing any file, a **Download file** option
  appears using the GitHub raw URL. Prompts for save path (pre-filled with the
  filename) and writes bytes to disk.
- **Language filter in repo search** — a second prompt after the search query
  accepts an optional language (e.g. `python`, `go`). Appends
  `language:<lang>` to the GitHub query with no extra API call.

### Fixed
- **Detached HEAD warning in commit & push** — sparse checkout leaves repos in
  detached HEAD. Octo now detects this upfront, explains it, and offers
  commit-only mode rather than letting push fail with a raw git error.
- **Pull-before-push** — a "Pull remote changes first?" prompt is offered
  before every push, preventing the common rejection caused by remote divergence.
- **Issue body input** — replaced the fragile raw `input()` loop with
  `inquirer.text()`, consistent with all other text inputs in the app.

---

## [1.3.0] — 2026-04-05

### Added
- **Clone History** — every sparse checkout recorded to `~/.octo_clones.json`
  (up to 20 entries, deduped by path). New **Clone History** main menu item
  with actions: commit & push, open in editor, open in browser, copy local
  path, remove entry.
- **Repository Search** — global GitHub repo search via `/search/repositories`.
  Sort by stars, recently updated, forks, or best match. Results feed directly
  into the unified repo action loop.
- **Starred Repositories** — browse up to 500 starred repos via `/user/starred`
  with the same filter and selection flow as Browse.
- **Recent Usernames** — last 10 usernames stored in `~/.octo_recent.json` and
  offered as a quick-pick list in the Browse flow.
- **GitHub Actions viewer** — last 30 workflow runs per repo with status icons
  (✓ ✗ ⟳ ⊘), branch, trigger, duration, and job-level drill-down with
  step-level failure details.
- **PR Diff viewer** — inside Issues & PRs, view a changed-files summary table
  (filename, status, additions, deletions) and read individual file patches
  with Monokai diff highlighting.
- **Create Issue** — title, optional body, optional labels fetched from the
  repo, preview before submission, opens the new issue in browser on success.
- **Open in Browser** — available in repo action menus, file preview, issue/PR
  views, and the Actions viewer.
- **Copy URL to Clipboard** — same touch-points as Open in Browser. Fallback
  chain: `pyperclip` → `pbcopy` (macOS) → `xclip`/`xsel` (Linux) → `clip`
  (Windows).
- **Shared repo action loop** — `_repo_action_loop()` used by Browse, Search,
  and Starred so all three behave identically. New features automatically
  propagate to all entry points.
- **Topic filtering** — Browse filter now also matches repository `topics`
  (no extra API call — field already present in repo data).
- **Commit & push quick-pick** — opens with a history picker of known local
  repos instead of requiring a manual path entry.

### Fixed (carried from v1.2.0 audit)
- **Private repos missing** — when browsing your own username while
  authenticated, Octo now calls `/user/repos` (returns private repos) instead
  of `/users/{username}/repos` (public only).
- **Non-JSON error responses crashed `_get_json`** — HTML 5xx pages from
  GitHub caused an uncaught `ValueError`. Now wrapped in `try/except`.
- **File browser wrong error for file paths** — GitHub returns a `dict` not a
  `list` for single-file paths. Error message now says "path points to a file"
  instead of "Empty repo?".
- **`_save_profiles` fd leak on `fdopen` failure** — explicit `os.close()`
  added in the except path.
- **Same fd leak in `_git_env_with_token`** — both temp file descriptors now
  closed on error.
- **`datetime.utcfromtimestamp` deprecated in Python 3.12** — replaced with
  timezone-aware `datetime.datetime.fromtimestamp(..., tz=datetime.timezone.utc)`.
- **Porcelain filename parsing stripped leading spaces** — `line[3:].strip()`
  changed to `line[3:]` to preserve filenames that start with a space.
- **Code search auth requirement** — GitHub made code search
  authentication-mandatory. Octo now checks for a token upfront and shows a
  clear message before attempting the API call.
- **Rate limit tracking** — every API response parsed for
  `X-RateLimit-Remaining`. Warns at ≤5 requests remaining; shows reset time
  when limit is 0.
- **Repo action menu now loops** — after browsing files, searching, or viewing
  stats you return to the same repo's action menu instead of being ejected to
  the username prompt.
- **Profile manager reachable when empty** — previously returned immediately
  with "No profiles" if none were saved. Now shows the full menu including
  "Add / update a token".

---

## [1.1.0] — 2025-03-31

### Security
- Fixed shell injection vulnerability in git credential helper — token written
  to a `0600` temp file, never interpolated into a shell string.
- Token validated against the GitHub API before saving. Invalid tokens are
  rejected at entry and never persisted.
- Atomic profile writes via `mkstemp` + `os.replace()` — a crash can no longer
  leave `~/.octo_profiles.json` corrupt.
- Loose permissions warning on startup and in profile manager with exact
  `chmod` command.
- Explicit `verify=True` on all outbound `requests` calls.

### Fixed
- File browser no longer exits after cloning a path.
- `$EDITOR` with arguments (e.g. `code --wait`) now split correctly before
  being passed to `Popen`.
- Git presence check before clone and push — clear error if `git` not on PATH.
- Empty file selection in interactive staging now aborts cleanly.
- Repo path validated before commit — distinct errors for missing path vs.
  non-repo directory.
- Corrupt profiles file shows a warning instead of silently resetting to `{}`.

---

## [1.0.0] — 2025-01-01

### Added
- Interactive repository browser with real-time filter
- Syntax-highlighted file preview — 40+ types, Monokai theme, line numbers
- Sparse checkout — clone any subdirectory via `git sparse-checkout`
- Commit & push workflow with interactive file staging
- GitHub code search scoped to a repository
- Issues & Pull Requests viewer with comment threads
- Repo stats: contributor bar charts, language breakdown, 26-week activity
- Multi-account token profiles stored in `~/.octo_profiles.json`
- Full pagination — no 100-repo or 100-branch cap
- Secure credential passing via git credential helper
- Cyan / electric-blue terminal theme with block-letter OCTO banner