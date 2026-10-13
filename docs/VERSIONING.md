# Version inventory

Root VERSION is the only canonical project version. docs/VERSION_POLICY.md is
the authoritative inherited policy. The source baseline was mod.info 0.2.0;
README 0.1.0 was stale. No root VERSION, inventory, or checker existed.

Target development version: 0.3.0-dev.1. Classification: MINOR in pre-1.0
development, with explicit breaking identifier changes (Mod ID, Lua API paths,
timed-action class, recipe module and command channel). A stable release version
has not been approved. Gameplay values and persistence schema 1 stay unchanged.

version-inventory.json lists current mod.info, README, Workshop description,
unpublished change note, validation report, and migration document mirrors.
Build-Workshop.ps1 reads VERSION, validates the inventory before building, and
checks generated ZIP metadata with --release. Current output belongs in
dist/current/B47ANCEDEyewear_v<VERSION>.zip. Historical packages never enter that
directory and are never relabeled.

PZ versionMin 42.20.3, Authentic Z version references, item-state schema 1,
test-kit marker version 1, and Workshop metadata format version 1 are independent
versions. Historical roadmap milestones, offline test observations and publication
records retain their original versions and dates. New tests must establish current
evidence; old results are not relabeled.

Commands from the workspace root:

```powershell
$pzPython = & ./tools/Resolve-HostTestPython.ps1
& $pzPython -B ./B47ANCEDEyewear/scripts/check_versions.py --root ./B47ANCEDEyewear
& $pzPython -B ./B47ANCEDEyewear/scripts/check_versions.py --root ./B47ANCEDEyewear --release
```

The release check is expected to fail until authorized current packages exist.
G8 also requires G7 dedicated multiplayer PASS and replacement artwork.
