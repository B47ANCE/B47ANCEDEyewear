# Identity migration

Project Version: 0.3.0-dev.1

Display name: B47ANCE'd Eyewear
Mod ID: B47ANCEDEyewear
Workshop ID: 3799754736 (preserved from WORKSHOP_ID.txt)

Formerly Glasses Stay Put, Mod ID GlassesStayPut, Lua API StayPutGlasses.
This document deliberately records deprecated identifiers for migration.

## Installation and administrators

Replace `Mods=GlassesStayPut` with `Mods=B47ANCEDEyewear` in dedicated-server
configuration; retain Workshop item `3799754736` in WorkshopItems. Update existing
save mod selections using the game's mod-management flow. Do not enable an old
copy alongside the new mod. Remove deprecated deployed copies manually after
backing them up; this task does not modify live mods or Workshop staging.

Workshop identity and technical Mod ID are separate. No new Workshop item was
created and no upload was performed. External compatibility mods/dependencies
must update require= references and calls to the renamed public API. No old Mod ID,
Lua global, require-path, recipe or network-channel alias is registered. Clients
and server must run the same new version; mixed-version commands are rejected.

## Persistence compatibility

[VERIFIED source] Core.state reads B47ANCEDEyewear item ModData first. Only if
that key is absent does it read valid schema-1 StayPutGlasses data. Core.migrateState
copies that table to an independent canonical table on authoritative refresh or
untie, then calls the existing syncItemModData/syncItemFields path. The old record
is preserved unchanged. Copying does not consume material, change item identity,
or restore a stale legacy record over a canonical value. Invalid legacy records
are not migrated. Clients can read the fallback but cannot write the migration.

Legacy tied monocles retain their original record for recovery; the new key gets
a retirement marker, the name is restored, and the established 70 fall chance
applies. The marker prevents resurrecting an obsolete tie on later refresh.
Dropped/unworn items migrate lazily on authoritative wear/refresh or untie.

The single-player test kit carries forward GlassesStayPut.TestKitVersion to
B47ANCEDEyewear.TestKitVersion when the latter is absent. It retains the old marker
and refuses a duplicate grant. Multiplayer refuses the kit before any marker write.

[INFERRED] Retention save data can remain compatible once the new Mod ID is
enabled. [RUNTIME GATE] Actual existing-save activation, field replication,
save/reload, transfer, late join and reconnect require native tests. Serialized
queued timed actions/recipe selections across the ID change are [UNKNOWN]; finish
or cancel pending actions before upgrading and retain a save backup.

## Authority and configuration audit

[VERIFIED source] Both ISB47ANCEDEyewear.perform and Server.onClientCommand use
the B47ANCEDEyewear/Tie route. The server resolves inventory IDs from the sender,
then revalidates ownership, equipped state, item eligibility, tie state and material
uses. Core.tie/untie reject clients. The existing native timed-action complete
path for untie and existing CraftRecipe flow are preserved, not certified anew.
Vanilla synchronization is reused; no custom server-command protocol is introduced.
Core's existing client retention refresh remains presentation derived from state;
authoritative persistence migration is forbidden on clients.

There are no existing SandboxVars or sandbox-options definitions in the baseline,
so no namespace/config migration is necessary. Existing-save or server sandbox
files have no project-owned keys to replace. Item retention values, category
defaults, material rules and action duration are configuration candidates but
remain unchanged for this identity-only task. Their absence from sandbox settings
is a pre-existing global-invariant gap, not a completed configuration feature;
designing those options requires a separate gameplay slice. Data schema/marker
versions, command names and canonical keys are implementation/protocol identifiers
and are not meaningful sandbox options.

## Files and packaging

Project folder Glasses Stay Put -> B47ANCEDEyewear; src/GlassesStayPut ->
src/B47ANCEDEyewear; client/server/shared StayPutGlasses folders -> B47ANCEDEyewear;
TimedActions/ISStayPutGlasses.lua -> ISB47ANCEDEyewear.lua;
GlassesStayPut_Crafting.txt -> B47ANCEDEyewear_Crafting.txt. All requires and
translation call sites use exact new case. Vanilla and third-party item IDs remain.

Historical dist output is moved intact to historical/artifacts. Source baseline
and SHA-256 inventory, old artwork and publication/preparation records are preserved
under historical/. They are excluded from runtime source and current packaging.
Other projects' console/API evidence and .tmp-stayput-api research are historical
observations and were not rewritten. Generic GSP occurrences are not renamed.

Obsolete thumbnails are removed from active source and mod.info poster/icon
references. Replacement artwork was not generated. Supply a new project-root
thumbnail.png, inspect its branding, then add an approved runtime thumbnail and
poster/icon metadata if desired. Build-Workshop.ps1 fails before staging when the
new root artwork is missing; it cannot accidentally reuse archived branding.
