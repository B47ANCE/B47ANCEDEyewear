# Retainer expansion preparation validation

Project Version: 0.3.0-dev.1

2026-10-03, Windows offline. Installed vanilla source identifies Build 42.21.
Requested feature is incomplete and BLOCKED; this report covers audits/source assets,
not functioning retainer gameplay. No src/ runtime code, loot table, deployed mod,
game file, launcher, server or Workshop publication was changed by this task.

| Area | Status | Evidence / remaining gate |
| --- | --- | --- |
| Vanilla material audit | PASS | 16 exact FullTypes, fields, tags, use semantics and source hashes. |
| Eyewear metadata audit | PASS | 45 candidates; four monocles excluded; geometric compatibility provisional. |
| Retainer native catch integration | BLOCKED | No adopted/verified post-roll pre-removal loader/hook. |
| Makeshift install/layers/tape | BLOCKED | No runtime implementation; catalog/contract checks are not gameplay tests. |
| Durability/breaking-hit/next fall | BLOCKED | Depends on authoritative native decision interception. |
| Zip-tie cutting | BLOCKED | Candidate vanilla tags verified; custom complete tool predicate/action not implemented. |
| Permanent item definition | BLOCKED | Proposed FullType only; duplication-safe actual-item storage unresolved. |
| Permanent attach/remove/reuse/transfer | BLOCKED | Full-item storage/transactions not implemented or tested. |
| Permanent loot/spawn frequency | BLOCKED | Two tables verified; no injection; proposed weights need native calibration. |
| Inventory sprite source | PASS | Original 64×64 RGBA; alpha/readability inspected; exact case/hashes checked. |
| Inventory sprite in PZ | NOT TESTED | No item definition or runtime asset reference enabled. |
| 3D model source | PASS | Original OBJ/GLB, 354 vertices, 488 triangles, nondegenerate outward geometry. |
| Final FBX export/import | BLOCKED | Blender not found in checked paths/PATH; export script supplied, not executed. |
| Head fit/animation/remote visuals | NOT TESTED | Bip01_Head metadata verified; native scale/origin/fit/lifecycle unverified. |
| Configuration | BLOCKED | Five SandboxVars proposed, not implemented; no new namespace claimed active. |
| Legacy tie migration | BLOCKED | Finite-retainer conversion planned only; current rename compatibility remains intact. |
| Lua and existing regression suite | PASS | Existing 38 regressions plus six preparation tests, 44 total. |
| Development version consistency | PASS | Canonical source remains 0.3.0-dev.1; future feature target separately classified. |
| Asset/internal filename case audit | PASS | Exact-case source references checked offline; not Linux runtime proof. |
| Single-player runtime | NOT TESTED | No game launched. |
| Existing-save/reload | NOT TESTED | No expanded runtime state exists to exercise. |
| Dedicated/two-client/reconnect/restart | NOT TESTED | G7 BLOCKED / NOT TESTED; no multiplayer certification. |
| Linux native loading | NOT TESTED | No Linux game/server used. |
| Release packaging | BLOCKED | G8 BLOCKED, missing feature/FBX/branding/native evidence; no current package. |

Exact commands, from workspace root:

```powershell
$pzPython = & ./tools/Resolve-HostTestPython.ps1
& $pzPython -B ./B47ANCEDEyewear/scripts/audit_retainer_sources.py --game-root 'E:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid'
& $pzPython -B ./B47ANCEDEyewear/scripts/build_retainer_assets.py
& $pzPython -B -m unittest discover -s ./B47ANCEDEyewear/tests -p test_retainer_preparation.py -v
& $pzPython -B -m unittest discover -s ./B47ANCEDEyewear/tests -v
& $pzPython -B ./B47ANCEDEyewear/scripts/check_versions.py --root ./B47ANCEDEyewear --json
& $pzPython -B ./B47ANCEDEyewear/scripts/check_versions.py --root ./B47ANCEDEyewear --release --json
```

Audit: 16 materials, 45 eyewear candidates, 67 source hashes. Focused six tests PASS;
full 44 tests PASS. The first parser fixture exposed an incorrect source line offset
over blank/comment lines; it was corrected and the audit regenerated before PASS.
Geometry cap winding/normals were checked and corrected before the source mesh passed.
Development version checks PASS; --release remains BLOCKED for absent current ZIP.
The planned 0.4.0-dev.1 is not a claim of an implemented or tested feature release.

Vanilla native classes were extracted from the current jar and inspected using:

```powershell
& 'E:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/jre64/bin/java.exe' -jar './.tmp-nightfall-decompile/cfr-0.152.jar' './B47ANCEDEyewear/research/retainers/native/zombie/characters/IsoGameCharacter.class' --outputdir './B47ANCEDEyewear/research/retainers/native' --silent true
```

The same command was used for extracted Core.class, InventoryItem.class and
ItemPickerJava.class. These are static evidence, not game launches. The original
inventory art used built-in imagegen then an edit for 64×64 readability; exact prompts
and final saved paths are in assets/retainers/ART_PROVENANCE.md and README.md.

G6 NOT TESTED; G7 BLOCKED / NOT TESTED; G8 BLOCKED. Safe next implementation
dependency: a supported original native interception/ownership bridge and loader
with build diagnostics, atomic catch/state contracts and actual-item conservation.
Do not bypass the block by re-equipping dropped eyewear or client-owned durability.
