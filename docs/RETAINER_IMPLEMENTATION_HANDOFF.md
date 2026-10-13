# Retainer implementation contract

Audited Source Version: 0.3.0-dev.1

Status: BLOCKED at native runtime proof and reusable-object storage.
Original native spike now builds and loads offline; see NATIVE_BRIDGE_REPORT.md
for REVISE decision. Historical preparation observations below are unchanged.
Planned feature version: 0.4.0-dev.1 (pre-1.0 MINOR, new gameplay capability with
explicit legacy-tie migration). Canonical VERSION remains 0.3.0-dev.1 because
no retainer feature has entered runtime source. Bump VERSION and all current
mirrors before the first gameplay implementation slice. Preserve historical
0.3.0-dev.1 test records rather than relabeling them as new-version evidence.

Read RETAINER_SOURCE_AUDIT.md for the exact blocked engine seam. Both makeshift
and permanent branches depend on it. Inventory sprite and mesh source preparation
are complete separately; they do not demonstrate a functioning wearable item.

## Proposed runtime model

Reserved proposed item: B47ANCEDEyewear.EyewearRetainer, display name Eyewear Retainer.
No item definition currently advertises or creates this FullType.
Wearable visual must be cosmetic derived state; it cannot create a second valuable
inventory item. New makeshift models can use the same optional visual adapter later.

Versioned persistent item ModData under B47ANCEDEyewear should contain a retainer
record with material FullType, kind, strand count, installed contribution snapshot,
current/maximum DUR, one optional tape type/contribution, permanent flag,
monotonic revision and schema version. Actual reusable-item payload/ownership must
use a verified attachment or full-item escrow mechanism, never a raw Lua userdata
or a FullType-only reconstruction. No unstable runtime object pointer is persisted.

Keep schema/command IDs and payload bounds internal. Material balance comes from
the central audited catalog (14 makeshift materials plus two tape reinforcements).
Same-material reinforcement adds its contribution to BOTH current and maximum;
the durability deficit is unchanged. Reject mixed strands, fourth strands,
rubber-band/bulk stacking, second tape, tape as base material and tape on zip ties
or permanent retainers. No repair-through-reinforcement. Removal destroys makeshift
material with no refund; permanent removal returns exactly the same valuable item.

Only native qualifying catches damage durability. Baseline severity=1, with a
trusted severity argument for future reliable event types. No retainer damage on
a non-fall roll. Permanent catches never degrade. If current reaches zero, that
event still saves the item; retire/remove the makeshift state only after committing
that successful catch. The next qualifying event falls normally. Monocles reject
all actions regardless of material, permanent item, compatibility API or client request.

## Authority and transaction contract

Clients request InstallMakeshift, ReinforceStrand, ApplyTape, RemoveMakeshift,
CutMakeshift, AttachPermanent and RemovePermanent with inventory IDs and expected
revision only. Do not expose a Catch/Damage command. Server derives the sender,
resolves items/tools, revalidates ownership/equipped/compatibility/config/material
uses/tape/layers/revision, then performs one atomic mutation and vanilla inventory
consumption/synchronization. Duplicate/replayed requests must refuse without extra
consumption or output. Menus and timed actions recheck current state at completion.
Do not combine native timed-action completion with a second command commit.

Native catch bridge calls the same authoritative state service, not the client
command router. Persist synchronized results via vanilla item ModData/field paths.
No Lua gameplay handler may manufacture a native fall decision. Fail closed when
capability is absent: disable expanded installs/loot/protection, report diagnostics,
preserve saved retainer data and allow safe recovery/removal when its storage path
is available. Never silently grant permanent protection as a substitute.

Permanent transfer must conserve the actual item across attach/remove/drop/
container/character transfer, disconnect and restart. Establish crash recovery,
mutually exclusive ownership and duplicate-ID detection for escrow before enabling it.
State revision checks alone do not provide crash-atomic inventory conservation.

## Sandbox proposal (not implemented)

Canonical server namespace: SandboxVars.B47ANCEDEyewear. Stable proposed identifiers:

| Option | Type / default | Bounds / interpretation |
| --- | --- | --- |
| MakeshiftRetainersEnabled | boolean / true | Disable new makeshift actions and catches; preserve data; allow removal. |
| PermanentRetainerEnabled | boolean / true | Disable new permanent attachment, loot and catches; retain recovery/removal. |
| RetainerDurabilityMultiplier | double / 1 | 0.25–10, step 0.25; snapshot contributions on installation. |
| RetainerImpactDamageMultiplier | double / 1 | 0.25–10, step 0.25; apply to future trusted catches. |
| PermanentRetainerRarity | enum / Very Rare | Extremely Rare (0.25), Very Rare (1), Rare (4), scaling proposed table weights; vanilla scarcity still applies. |

Validate finite values/type/bounds on the server, use default on malformed input,
and ship names/tooltips/grouping in all 29 locale JSON tables. Existing retainer
contribution snapshots stay stable when durability multiplier changes; future
same-material reinforcement uses that installed contribution. Damage settings apply
to future events. No per-material sliders, bone IDs or protocol safety-limit settings.

Legacy version-1 eyewear ties cannot remain an unlimited parallel solution. Once
the native capability is enabled, migrate known material ties to one finite strand
once on the server, preserving the item/name/condition/prescription and refunding
nothing. Legacy hats remain in their existing separate mechanic. Unknown/corrupt
records require explicit safe recovery; do not invent a commercial permanent item.
This conversion and flag-change behavior need existing-save/dedicated tests.

## Context and condition UI

Show Make Makeshift Retainer only for compatible worn eyewear with at least one
available valid material. List only those materials. Show reinforcement only for
the same material below its layer cap; rubber band/bulk reinforcement never appears.
Show available tape only when no tape is installed and the base accepts tape.
Permanent items show only valid attach/remove options, no repair/reinforcement.
Zip-tie cutting appears only after reliable server-side tag/condition/sharpness
validation is implemented and a valid tool is available. No redundant opposite-state
or unavailable-material menu entries. Player-visible text must be fully localized.

Tooltip/inspection must show current/maximum DUR, material, strands and tape; for
permanent show Permanent rather than a misleading numeric durability. Display
condition descriptions only as supplementary information. Comfort penalties and
event-specific impact types remain deferred until supported hooks are verified.

## Native proof required before enablement

Verify exact post-roll/pre-removal injection on the supported build, normal false
roll behavior, final breaking catch, next-event fall, authoritative item sync,
single consumption under queued/replayed requests, forged IDs/revisions, two-client
durability/breakage, permanent attach/remove/transfer duplicate attempts, full-item
escrow crash recovery, save/reload/restart, late join/reconnect and client visuals.
G6 NOT TESTED; G7 BLOCKED / NOT TESTED; G8 BLOCKED. No deployment/publication is authorized.
