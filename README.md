# B47ANCE'd Eyewear

Standalone Build 42 mod, ID `B47ANCEDEyewear`, version 0.7.0-dev.1.

Lua-only development build targeting Project Zomboid 42.21. No Java agent, bridge,
JAR dependency, test suite or debugger item-grant command is part of the project.
Gameplay and dedicated multiplayer acceptance remain unverified.

Wear compatible glasses or a straw/summer hat, keep a supported material in your
main inventory, and right-click the worn item. **Tie** lists available twine,
rubber bands, dental floss, ordinary thread, sinew thread or aramid thread.
Tying consumes one use and preserves the original item, condition, prescription,
model and custom name. **Untie** restores the original name without refunding material.
Crafting → Tailoring also offers **Tie worn eyewear**. Wear compatible vanilla
glasses, a straw hat or a summer hat and keep a supported material in your main
inventory. The recipe consumes one use, modifies the same item and cannot batch
craft. Already tied, broken or unworn items are rejected. No skill, magazine or
workbench is required. Modded eyewear can continue using the inventory context menu.
Monocles remain incompatible with tying.

Tied attachments use the existing zero-fall retention behavior. Untied eyewear
uses item-specific profiles. Strapped protective headwear defaults to zero fall
value, while loose hats retain vanilla behavior. Vanilla impact calculation remains in control.
Server sandbox options control new tying, the untied-eyewear multiplier and the
strapped-headwear fall value. Existing ties remain valid when new tying is disabled.

Hovering tied eyewear shows its material and secured state beside the normal
inventory tooltip, without a fabricated durability bar. Historical finite or
permanent retainer records are preserved for inspection and clearly marked inactive.
Finite-retainer catches, permanent reusable-item gameplay, rare loot and worn
retainer models are not included. Their Lua-only implementation requires a verified
engine capability and authority design; no substitute catch calculation is installed.

Authoritative runtime source: `src/B47ANCEDEyewear/42/`.
Workshop item: https://steamcommunity.com/sharedfiles/filedetails/?id=3799754736
Public source: https://github.com/B47ANCE/B47ANCEDEyewear

See [architecture](docs/ARCHITECTURE.md), [validation and release gates](docs/VALIDATION.md),
[cleanup record](docs/CLEANUP_AND_WORKSHOP_PREPARATION.md) and [version policy](docs/VERSION_POLICY.md).
Old audit/publication documents retain their original tested versions and are historical evidence.

## Development tools

Release tooling uses Python with `requirements-tools.txt` for syntax parsing;
it never runs gameplay fixtures or a unit-test suite. The runtime mod has no Python dependency.

```powershell
python -m pip install -r requirements-tools.txt
python -B scripts/check_versions.py
python -B scripts/validate_release.py
./Build-Workshop.ps1 -PythonExe <python-with-lupa>
./Publish-Workshop.ps1 -PrepareOnly -PythonExe <python-with-lupa>
```

Preparation generates source/staging/ZIP provenance and an upload VDF while
preserving the existing item and visibility. It does not upload. Publication requires a separate explicit request. The labelled MP testing build may
be distributed before dedicated validation; stable release still requires G7/G8.
Published packages, asset masters and superseded experiment evidence are preserved;
retired test/Java code is recoverable in the private cleanup quarantine, outside this repository.
