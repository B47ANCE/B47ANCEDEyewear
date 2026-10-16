# Clothing visual registration and synchronization

Project Version: 0.14.0-dev.1
Audit: 2026-10-15; installed Project Zomboid 42.21 / Steam build 25485521.

## Cause and evidence

[VERIFIED: dedicated log observation, earlier deployed build] The native
SyncClothing packet failed while TieDurability.install called setWornItem.
ItemDescription dereferenced a null InventoryItem.getVisual() result for tint.
A later compatibility diagnostic identified ImprovisedTieEyes without a visual
and removed it from worn equipment. This observation proves the original failure;
it is not acceptance evidence for this source patch. Private logs stay outside Git.

[VERIFIED: source] The published 0.12 package and the 0.13 source contain custom
clothing XMLs but no media/fileGuidTable.xml. The installed native lookup requires
the table: ZomboidFileSystem.loadFileGuidTable reads both common and versioned mod
media/fileGuidTable.xml files, namespaces their GUIDs and merges their entries.
OutfitManager.loadAllClothingItems looks up media/clothing/clothingItems/<name>.xml
through getGuidFromFilePath. Without a GUID it skips assigning clothingItemAsset.
InventoryItem.getVisual returns null if that asset is absent or not ready.
SyncClothingPacket.ItemDescription has guards for texture indices, but its tint
read dereferences getVisual without a null check. The existing pcall cannot repair
a failed native packet: native sending logs/catches its own failure after equip.

Read-only inspection of original installed JAR entries yielded these SHA-256s:

| Entry | SHA-256 |
| --- | --- |
| zombie/ZomboidFileSystem.class | c4e5a5123bc43d03f2585c40f37544c50c1e702eebceb78bec94069e410b6750 |
| zombie/core/skinnedmodel/population/OutfitManager.class | 8e93b6618f61a9c28017661826374fec8594a6013c0ef1c1fc1834db550da4c7 |
| zombie/inventory/InventoryItem.class | 48f01be16d1ef1b76e37638fac6e25ca4eb285ad38ab2f462caa5597318c7f9d |
| zombie/network/packets/SyncClothingPacket$ItemDescription.class | 050b0eca12e211c4d7c514dd9b82a6104381d7591820a0c65ca47ee24c5d9328 |

Installed shared/TimedActions/ISClothingExtraAction.lua:67,69 also calls
item:getVisual() during authoritative clothing conversion. No copied engine code,
custom Java, JAR, third-party assets or third-party implementation was added.

## Change and invariants

The new GUID table registers all seven existing XMLs using their existing
m_GUID values and exact path case. It includes the older invisible definition
for compatibility and all six current retainer/tie definitions. No GUID, FullType,
slot, mesh, texture, item condition, schema or material rule changes.

Tie installation checks the actual new native item's visual before assigning
reciprocal links, sending AddItem, equipping or consuming a material use. An
unready visual causes removal of only that not-yet-published transaction item.
New Tie rolls back target metadata/name/chance without payment. Paid legacy
migration retains its pending record and may retry on the existing refresh path;
it does not publish/remove a network item or leave a committed link on rejection.
No new scan, event, packet, client-owned gameplay state or retry timer is added.
Asset validity is a technical invariant, not a configurable gameplay preference;
existing server sandbox settings remain authoritative and unchanged.

Existing actual ties retain identity and condition. Native getClothingItem uses
the current script asset, so registration also addresses saved items without
reconstructing them. [RUNTIME GATE] That old-save/rejoin behavior still requires
actual dedicated testing. Missing newer tie items remain unreplaced by design.

## Validation

[TESTED: offline, 2026-10-15] Before adding the table, the new production check
failed with `Missing native clothing file GUID table`. The completed source
preflight passes for 195 runtime files and compiles all 14 Lua files; native table
shape, unique GUIDs, XML identity, exact path case and script bindings are checked.
The pre-existing artwork/import/hash, localization and Lua-only checks also pass.

A disposable audit outside the repository runs actual gameplay modules through
Lupa Lua 5.1 with doubles, preserving the project's no-test-suite/runtime-debug
policy. Its simulated native sender records failure without throwing to Lua.
With HEAD's old TieDurability module, the new scenario fails with `unresolved
visual accepted and charged`. With this patch, all 126 assertions pass, including
Eyes/Face/Hat rejection, zero publication/payment, readiness retry, repeated paid
legacy migration, original record preservation, condition/identity, payment and
notification failures, native-break simulation, ownership/transfer and client
rejection. It is not PZ execution or network acceptance evidence.

Commands from the project root:

```powershell
python -B scripts/check_versions.py
python -B scripts/validate_release.py
python -B "$env:TEMP/B47ANCEDEyewear-lua-durability-audit/clothing_sync_regression.py"
git diff --check
```

Production-check mutation probes additionally reject a missing table, removed
registration, duplicate path/GUID, incorrect case, XML GUID mismatch and unresolved
script binding. Fixtures and raw native inspection output remain outside source.

## Native acceptance remaining

[RUNTIME GATE] G6 native/SP NOT TESTED; G7 dedicated NOT TESTED / BLOCKED; stable
G8 BLOCKED. With matching updated server and two remote clients, verify existing
saved ties, new Eyes/Face/Hat ties, all retainers, Untie/Take Off, native damage,
join/rejoin and server restart. Confirm remote appearance and preserved item
condition/IDs, one-use payment, no duplicate migration and no new SyncClothing or
missing-visual removal messages. A Lua guard cannot fix unrelated mods' invalid
worn entries. No deployment, publication, game/server launch or remote write was
performed for this request.

The 0.13.2 thumbnail-only iteration preserves this implementation. All evidence
above retains its original version/package; no clothing behavior changed.

The 0.14.0-dev.1 material/reinforcement iteration reuses these same seven registered
clothing assets for three new LayeredTie script types. No XML/GUID/mesh changes.
Historical 0.13.1 acceptance does not establish the new gameplay's MP behavior.
