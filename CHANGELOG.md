# Changelog

## [0.8.0-dev.1] — 2026-10-14

- MINOR: add craftable reusable cloth and leather eyewear retainers with a dedicated vanilla equipment slot.
- Keep actual inventory items through Wear/Take Off, vanilla crafting, transfers and saves; protect one compatible worn pair through server-owned derived fall values.
- Add server sandbox settings, item/recipe instructions, original inventory artwork and production asset/localization checks.
- Exact minus-one durability on successful native knock-off remains blocked: the installed engine exposes no server-safe Lua callback at that decision. No substitute damage or Java code is installed.
- Static/offline checks only; SP/dedicated validation NOT TESTED and G7/G8 blocked. No packaging, deployment or publication in this iteration.

## [0.7.0-dev.2]
- Add user-supplied fallback icon/thumbnail; preserve manually supplied artwork. Asset-only iteration; gameplay unchanged.
- Offline branding/version checks only; earlier validation remains historical at 0.7.0-dev.1. No new SP/dedicated MP evidence.

## [0.7.0-dev.1] — 2026-10-14

- MINOR: add Tie worn eyewear to Crafting → Tailoring using verified Build42 recipe hooks and the existing server-owned tie transaction.
- Keep both selected inputs in vanilla processing; consume exactly one material use in successful authoritative completion without replacing the eyewear.
- Reject worn-state, ownership, broken/tied-state or sandbox failures; disable batch crafting and preserve context-menu support for optional modded eyewear.
- Add recipe labels/instructions and production localization checks. Preserve the prepared0.6 candidate with hashes; no testing/debug or Java code is restored.
- Source inspection and offline syntax/integrity checks only. Actual SP/dedicated crafting remains NOT TESTED; G7/G8 stay blocked.

## [0.6.0-dev.1] — 2026-10-14

- Lua-only cleanup: remove testing/debug code and retire Java-dependent finite-retainer actions and the unsafe crafting recipe.
- Keep server-validated item context-menu tying/untying and read-only historical retainer inspection; preserve existing item data and released artifacts.
- Fix tie transaction failures, tighten inventory commands, localize item labels and bound tooltip placement.
- Prepare Workshop content using production-only version/content checks. No game/server or dedicated MP validation; G7/G8 remain blocked.
- Pre-1.0 MINOR compatibility decision: withdraw experimental retainer action APIs, debugger grants and TieGlasses recipe. Existing legacy tie data remains supported; finite records are retained read-only and do not provide protection.

## [0.5.0-dev.1] — 2026-10-10

- Add read-only inventory retainer inspection, condition bar and reinforcement breakdown.
- MINOR: additive UI capability; gameplay/schema and native bridge design unchanged.
- Native gameplay and dedicated multiplayer runtime gates remain unresolved.

## [0.4.0-dev.1] — 2026-10-05

- Retainer expansion development: compatible feature additions and finite
  retainer schema; legacy conversion is capability-gated.
- Fixed eager game-type loading on native incompatibility paths; production
  authority and conservation requirements remain enforced.
- Historical 0.3.0-dev.1 publication and validation records are retained.
- No in-game testing or automatic Workshop upload in this implementation task.




## [0.3.0-dev.1] — 2026-10-03



- Renamed Glasses Stay Put (`GlassesStayPut`) to B47ANCE'd Eyewear

  (`B47ANCEDEyewear`), including project/source folders, Lua modules, recipe

  module, timed action, localization keys, network channel, and build paths.

- Added authoritative, non-destructive migration of legacy item retention data

  and compatibility for the single-player test-kit grant marker.

- Adopted root VERSION and synchronized current metadata and documentation.

- Archived old distribution output and obsolete artwork. Workshop packaging

  requires replacement branding; native and dedicated multiplayer gates remain open.

- Preserved item-specific probabilities, tied zero chance, monocle exclusion,

  materials, recipes, and context-menu behavior. Public identifier compatibility

  changes are documented in docs/IDENTITY_MIGRATION.md.

- 2026-10-03 retainer expansion preparation: audited current installed Build 42.21

  materials/eyewear/native seams and created original inventory/3D source assets.

  No gameplay or loot implementation was enabled; native interception and reusable

  permanent-item storage remain blocked. Planned feature version is 0.4.0-dev.1.



- 2026-10-04 authorized isolated runtime attempt failed during startup with
  an incompatible loose class and duplicate-class LinkageError. Preserved logs;
  user stopped in-game testing. No gameplay result, deployment or promotion.

- 2026-10-04 user-authorized Workshop development publication: replacement
  preview, explicit development title/status and current renamed Lua source.
  Native bridge/fixtures and retainer expansion excluded; runtime gates remain open.

## [0.2.0] — source baseline



Historical Glasses Stay Put retention framework and item-specific profiles.

The exact pre-rename source, unpublished Workshop note, distribution artifacts,

and their original versions are preserved in historical/. The 0.2.0 source was

tested with 31 offline tests before this migration; it is not runtime evidence.

