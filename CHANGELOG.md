# Changelog

All notable changes to Octo are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.1.0] — 2025-03-31

### Security
- **Fixed shell injection via credential helper** — token is now written to a
  `0600` temp file and passed to git via a helper script. The raw token string
  no longer appears in any shell evaluation context, closing a potential
  injection vector for tokens containing `$`, backticks, or `!`.
- **Token validated before saving** — PAT is now checked against the GitHub API
  before being written to disk. Invalid or expired tokens are rejected and never
  persisted.
- **Atomic profile writes** — `~/.octo_profiles.json` is now written via a temp
  file + `os.replace()` (atomic on POSIX and Win32). A crash or interrupt during
  save can no longer produce a corrupt/truncated profiles file.
- **Loose permissions warning** — startup and the profile manager now check
  `~/.octo_profiles.json` permissions on Unix and warn if group/other read bits
  are set, with the exact `chmod` command to fix it.
- **Explicit TLS verification** — all `requests` calls now pass `verify=True`
  explicitly rather than relying on the library default.

### Fixed
- **File browser no longer exits after cloning** — previously selecting "Clone
  this path" broke out of the browse loop entirely. Now the loop continues so
  you can keep navigating or clone another folder.
- **`$EDITOR` with arguments now works** — values like `"code --wait"` or
  `"vim -p"` are split on spaces before being passed to `Popen`, so the editor
  launches correctly instead of failing with `FileNotFoundError`.
- **git presence check** — `clone_and_edit()` and `commit_and_push()` now verify
  `git` is on `$PATH` before doing anything and show a clear error if not.
- **Empty file selection in interactive staging** — selecting no files in the
  checkbox picker now aborts with a message instead of running a silent no-op
  commit.
- **Repo path validation** — `commit_and_push()` checks that the path exists
  and is a git repository before proceeding, with a distinct error for each case.
- **Corrupt profile file** — a malformed `~/.octo_profiles.json` now shows a
  warning instead of silently returning an empty dict and potentially
  overwriting good data.

---

## [1.0.0] — 2025-01-01

### Added
- Interactive repository browser with real-time filter
- Syntax-highlighted file preview (50+ languages via Monokai theme)
- Sparse checkout — clone any subdirectory, not just full repos
- Commit & push workflow with interactive file staging
- GitHub code search scoped to a single repository
- Issues & Pull Requests viewer with comment threads
- Repo stats: contributor bar charts, language breakdown, 26-week commit activity
- Multi-account token profiles stored in `~/.octo_profiles.json`
- Full pagination — fetches all repos / branches, no 100-item cap
- Secure credential passing via Git credential helper
- Cyan / electric-blue terminal theme with `bright_cyan` OCTO banner
