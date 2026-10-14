# Validation and release gates

Project Version: 0.6.0-dev.1

The user explicitly requested removal of all testing code. No test suites,
gameplay doubles, item-grant/debug commands or Java harnesses remain in active source.
Production preflight checks are retained to reject malformed or unsafe releases.
Old test reports retain their observed versions; they are not current proof.

Commands from the project root, using a Python interpreter with requirements-tools.txt:

```powershell
python -B scripts/check_versions.py
python -B scripts/validate_release.py
./Build-Workshop.ps1 -PythonExe <python-with-lupa>
python -B scripts/check_versions.py --release
./Publish-Workshop.ps1 -PrepareOnly -PythonExe <python-with-lupa>
```

The syntax parser compiles Lua without executing gameplay. Source preflight checks
Lua-only payloads, case-correct requires, JSON/key/placeholder coverage, canonical
Workshop text and source URL. Package preflight verifies inventory, safe paths,
case collisions, ZIP CRC, source/staging hashes and version provenance. Upload
preparation compares VDF description/change-note text to canonical real paragraphs.
These checks are static/offline integrity, not behavior tests or Linux/runtime evidence.

[RUNTIME GATE] SP behavior and dedicated MP have not been validated for this iteration.
G7 BLOCKED / NOT TESTED; G8 BLOCKED. Stable release requires current-commit dedicated evidence and gates. Under the
2026-10-14 Workshop MP testing policy, an explicit publish request may distribute
this labelled test build before G7, after all source/authority/security/package checks.
Preparation does not
launch a game/server, deploy live mods, connect via SFTP or contact SteamCMD.
