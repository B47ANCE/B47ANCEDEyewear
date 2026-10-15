# Validation and release gates

Project Version: 0.8.0-dev.1

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
Lua-only payloads, case-correct requires, JSON/key/placeholder coverage,
recipe-name/instruction localization, canonical
Workshop text and source URL. Package preflight verifies inventory, safe paths,
case collisions, ZIP CRC, source/staging hashes and version provenance. Upload
preparation compares VDF description/change-note text to canonical real paragraphs.
These checks are static/offline integrity, not behavior tests or Linux/runtime evidence.

[VERIFIED: source] The crafting adapter uses installed vanilla OnTest/OnCreate,
IsWorn and keep semantics. Payment stays in the existing server/SP tie transaction;
clients submit the vanilla crafting action. No gameplay test suite was restored.
Recipe labels/instructions use English fallback in the 29 supported language
folders, matching the existing localization policy; key presence is not proof of
native-language translation quality.

[TESTED: offline, 2026-10-14] `python -B scripts/check_versions.py` passed for
0.7.0-dev.1. `python -B scripts/validate_release.py` passed for 128 runtime files,
including compilation of all nine Lua files without execution and translation
key/instruction coverage. A read-only identity audit matched all 47 recipe input
IDs against the installed generated item definitions. `git diff --check` passed.
Package results, source hashes and commit are recorded in generated provenance;
they do not replace the untested gameplay gates below.

[TESTED: offline, 2026-10-14, 0.8.0-dev.1] Run from the project root using the
bundled Python with Lupa 2.6:

```powershell
& 'C:/Users/willi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B scripts/check_versions.py
& 'C:/Users/willi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B scripts/validate_release.py
git diff --check
```

All passed: 165 runtime files; all 12 Lua files compile without execution; JSON,
XML, localization and exact original icon checks pass. A separate read-only
source audit matched all 49 referenced vanilla types and both defined custom
outputs. Native registry and clothing/equipment source paths were inspected, not
executed in PZ. No test suite was restored. No current 0.8 package was generated;
the prior provenance in dist/current remains a historical 0.7.0-dev.1 record.
See RETAINER_ITEMS.md for the exact durability hook blocker and current manual
runtime scenarios. Dedicated G7 and stable G8 remain blocked.

[RUNTIME GATE] SP behavior and dedicated MP have not been validated for this iteration.
G7 BLOCKED / NOT TESTED; G8 BLOCKED. Stable release requires current-commit dedicated evidence and gates. Under the
2026-10-14 Workshop MP testing policy, an explicit publish request may distribute
this labelled test build before G7, after all source/authority/security/package checks.
Preparation does not
launch a game/server, deploy live mods, connect via SFTP or contact SteamCMD.
