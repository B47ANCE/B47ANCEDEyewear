# B47ANCE'd Eyewear

Standalone Build 42 mod, ID `B47ANCEDEyewear`, version 0.9.0-dev.1.

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

Crafting → Tailoring now also provides two real wearable items:

- **Make cloth eyewear retainer:** 2 ripped sheets + 2 uses of twine or thread.
- **Make eyewear retainer:** 2 leather strips + 4 thread uses + 2 rubber bands;
  a sewing needle and usable scissors are kept.

Wear either in its dedicated Eyewear Retainer slot alongside compatible glasses.
One retainer protects one untied, unbroken, non-monocle pair in vanilla worn-slot
order. Take Off preserves the same retainer for reuse and restores the glasses'
normal retention. Both materials currently have the same configurable protection;
there is no hidden durability or quality difference. Hats still use Tie/Untie.
No magazine, skill level or workbench is required for either output recipe.

**Unbreakable Eyewear Retainer** is a separate rare, non-craftable item. It keeps
its condition through normal wear and catches and uses the original black-cord
artwork. Look in school lockers, optical-store containers and pharmacy cabinets.
The server's RareRetainerLootChance defaults to 0.25% per eligible new container
fill (range 0–5%; zero disables spawns). Existing filled containers are not changed.
Crafted cloth and leather retainers have distinct new inventory icons.

Tied attachments use the existing zero-fall retention behavior. Untied eyewear
uses item-specific profiles. Strapped protective headwear defaults to zero fall
value, while loose hats retain vanilla behavior. Vanilla impact calculation remains in control.
Server sandbox options control new tying, the untied-eyewear multiplier and the
strapped-headwear fall value, wearable-retainer enable switch and retained-eyewear
fall value (default 0), plus the rare-item loot chance. Disabling wearable retainers stops their crafting/protection
but preserves the actual items. Existing ties remain valid when new tying is disabled.

Hovering tied eyewear shows its material and secured state beside the normal
inventory tooltip, without a fabricated durability bar. Historical finite or
permanent retainer records are preserved for inspection and clearly marked inactive.
Reusable wearable retainer items and their original inventory icon are included.
Their clothing definition is deliberately invisible: no fitted 3D worn model is
claimed. Loot-only acquisition and native unbreakable behavior are described in
[the rare-item record](docs/RARE_RETAINER.md). Exact -1 durability per successful vanilla
knock-off remains blocked by the engine's missing server-safe Lua callback.
Ordinary hits never charge durability; no second fall roll, post-drop re-equipping
or Java dependency is installed. See [retainer behavior and blocker](docs/RETAINER_ITEMS.md).

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
