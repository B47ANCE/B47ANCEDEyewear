# B47ANCE'd Eyewear

Standalone Build 42 mod, ID `B47ANCEDEyewear`, version 0.12.0-dev.1.

Lua-only development build targeting Project Zomboid 42.21. No custom Java/JAR,
test suite or debugger grants are shipped. SP/dedicated gameplay is NOT TESTED.

Wear compatible glasses or a straw/summer hat, keep twine, a rubber band, dental
floss, ordinary thread, sinew thread or aramid thread in your main inventory,
and right-click → Tie. Crafting → Tailoring → Tie worn eyewear uses the same
server transaction. One material use creates/equips a finite improvised tie;
the original eyewear, condition, prescription, model, ID and custom name survive.
Monocles remain incompatible. Untie restores the name and consumes the matching
tie without refunding material. The matching tie slot and a little inventory
space must be free. Transfer the eyewear and its linked tie together; wearing
both activates protection. Taking off either suspends protection. Paid legacy
ties upgrade once when worn, without a second payment; missing newer tie items
never receive free replacements.

Crafting → Tailoring also provides:

- **Make cloth eyewear retainer:** 2 ripped sheets + 2 uses of twine or thread.
- **Make eyewear retainer:** 2 leather strips + 4 thread uses + 2 rubber bands;
  a sewing needle and usable scissors are kept.

Wear these actual items in the separate Eyewear Retainer slot. One unbroken
retainer protects one compatible pair without an active improvised tie, selected
in worn-slot order. Hats keep the direct Tie flow. Take Off preserves the same
retainer and its remaining condition. No learning requirement or workbench applies.

**All improvised ties and both crafted retainers now have durability.** They lose
native condition from eligible head/clothing damage. Defaults give a one-in-1
condition-loss chance for improvised ties, one-in-2 for cloth and one-in-4 for
leather, each on the existing 10-point native condition scale. Server sandbox
settings adjust these wear-resistance values (integer 1–100). Larger values last
longer; these are not guaranteed hit counts. The tooltip shows actual remaining
condition, status and a live bar. Native headwear layering and damage ordering
apply; a breaking blow can also dislodge the eyewear. No hidden knock-off roll is
counted and no Java bridge, second Lua hit roll or post-drop re-equipping is used.
See [durability and migration](docs/DURABILITY.md).

**Unbreakable Eyewear Retainer** is rare, non-craftable loot in school lockers,
optical-store containers and pharmacy cabinets. Its original black-cord artwork
and no-coverage/no-wear definition remain unchanged. RareRetainerLootChance is
0.25% per eligible new fill by default (0–5%; zero disables spawns). Existing
filled containers remain unchanged. Crafted cloth and leather keep distinct icons;
improvised ties reuse the cloth icon. All three retainer items have distinct 3D
ground models: cloth loops, stitched leather and black cord with rubber sleeves.
All three also have head-attached worn models with male/female variants.
In-game fit and clipping are untested. See [worn assets](docs/WORN_MODELS.md) and
[ground assets](docs/GROUND_MODELS.md).

Server sandbox settings also control new tying, untied-eyewear retention,
strapped-headwear fall value, wearable crafting/protection and retained-eyewear
fall value (default 0). Disabling new tying does not erase existing ties. Disabling
wearable protection does not repair or delete actual items; worn finite clothing
can still wear. Historical schema-2 records remain read-only and inactive.

Authoritative source: `src/B47ANCEDEyewear/42/`.
Workshop item: https://steamcommunity.com/sharedfiles/filedetails/?id=3799754736
Public source: https://github.com/B47ANCE/B47ANCEDEyewear

Workshop development / MP test distribution of 0.12.0-dev.1 was explicitly
requested after worn-model implementation. Exact release commit, package/text
hashes, offline checks, upload verification and Steam restart outcome are recorded
in generated publication provenance. Published 0.11.1 files remain preserved.
No game/server was launched; G7 BLOCKED / NOT TESTED and stable G8 BLOCKED
remain unchanged. Publication does not imply local SP deployment.

See [architecture](docs/ARCHITECTURE.md), [retainer items](docs/RETAINER_ITEMS.md),
[validation](docs/VALIDATION.md) and [version policy](docs/VERSION_POLICY.md).
Historical evidence retains its actual version and environment.

## Development tools

Production preflight compiles Lua and checks source/assets without running gameplay:

```powershell
python -B scripts/check_versions.py
python -B scripts/validate_release.py
```

Release tools require requirements-tools.txt; Python is not a runtime dependency.
Build-Workshop.ps1 prepares source/staging/ZIP provenance; Publish-Workshop.ps1
-PrepareOnly checks canonical description/change-note paragraphs and existing ID/
visibility without uploading. Deployment and publication require separate requests.
