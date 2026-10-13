> **Lua-only policy (2026-10-12):** Custom Java code, agents, bridges and JAR mod dependencies are prohibited. Older bridge documentation is historical and superseded. The current snapshot has disabled bridge-dependent retainer paths awaiting Lua-only redesign; it does not supply functioning finite-retainer catches. Offline tests do not prove in-game or dedicated multiplayer behavior. Workshop publication remains a separate operation.
# B47ANCE'd Eyewear



Standalone Build 42 mod, ID `B47ANCEDEyewear`, version 0.5.0-dev.1.

Current source adds a finite makeshift-retainer development candidate: 14 materials,
same-material layering, tape reinforcement, durability display and server-validated
installation/removal. It requires the separately loaded, exact-build native bridge
to intercept the original post-roll fall. The bridge is not automatically installed
by subscribing to the Workshop item. Permanent reusable retainers, loot and worn
visuals remain blocked on safe actual-item ownership/persistence.

See [current implementation and validation](docs/RETAINER_EXPANSION_IMPLEMENTATION.md).
Workshop remains on 0.3.0-dev.1. The legacy behavior described below remains the
fallback when the bridge is unavailable. No in-game or dedicated MP readiness is claimed.


Wear glasses, carry twine, a rubber band, dental floss, or thread in your main

inventory, then use the **Tie glasses** crafting recipe and select the worn pair

and a material. One use is consumed (one whole rubber band). The attached tie

stays with the original glasses until it is untied from that item's right-click

menu; untying does not refund material.



You can also right-click a worn supported pair or hat. An untied item submenu

contains **Tie**, followed by only the tying materials currently in your

inventory. A tied item submenu contains **Untie** only. If no materials are

available, Tie is disabled with an explanation. Multiplayer requests are

validated and applied by the server.

No skills, tools, dependencies, new loot, or prescription changes.



Supports vanilla glasses, including Face-slot Reading Glasses, original

Authentic Z and Faded's Authentic Z 42.20.2.1 glasses. The recipes enumerate

all tieable current vanilla glasses definitions and the six shared Authentic Z

definitions, so only actual eyewear is selectable. Eyepatches, masks, clown

noses, monocles, and non-clothing props remain excluded. Vanilla eyewear uses

item-specific untied knock-off profiles; see `docs/RETENTION_PROFILES.md`.

Monocles use a 70 ChanceToFall profile and cannot be tied. Frockin uses vanilla eyewear and

has no distinct eyewear item definition requiring an adapter. Compatibility is

host-tested; native validation is pending.



Source: `src/B47ANCEDEyewear/42/`. Development candidate; native and multiplayer

validation remain UNVERIFIED. See `docs/TESTING.md`.



For single-player testing, enter `B47ANCEDEyewearTestKit()` in the Lua debugger.

It gives every supported vanilla and Authentic Z pair, both supported hats, and

two of every supported material. Compatibility items that are unavailable are

listed in the console. The kit is granted once per character; use

`B47ANCEDEyewearTestKit(true)` to grant another.



Workshop staging is generated with `./Build-Workshop.ps1`. It runs host checks,

packages only runtime content, creates a 256x256 Workshop preview, preserves

existing Workshop identity/visibility on rebuild, and verifies source/staging/ZIP

hashes. Tests, documentation, build scripts, and caches stay outside the upload.

Default staging: `C:/Users/willi/Zomboid/Workshop/B47ANCEDEyewear`.



Identity migration: see `docs/IDENTITY_MIGRATION.md`. Existing servers must use

`Mods=B47ANCEDEyewear`; Workshop ID `3799754736` is preserved. Legacy item state

is read compatibly and migrated by authority; existing-save runtime acceptance

is pending. No SandboxVars existed in the baseline.



Canonical version: root `VERSION`; policy and inventory: `docs/VERSION_POLICY.md`,

`version-inventory.json`. Current validation: `docs/RENAME_VALIDATION.md`.

Workshop development build was published on 2026-10-04 with replacement preview
artwork; see docs/WORKSHOP_DEVELOPMENT_DEPLOYMENT.md. Native and dedicated gates
remain open.

Historical packages and artwork are preserved under `historical/`, excluded from

active distribution. Earlier preparation records describe their original
no-publication state; the later development upload is documented separately.



Retainer expansion is currently BLOCKED at the native post-knock-off-roll hook

and reusable permanent-item storage. Source audits, original inventory art and

3D model sources are prepared outside runtime source; no retainer gameplay or

loot is enabled. See `docs/RETAINER_SOURCE_AUDIT.md`,

`docs/RETAINER_IMPLEMENTATION_HANDOFF.md`, and `assets/retainers/README.md`.



Native catch bridge development spike: build and offline loading are verified

separately in `docs/NATIVE_BRIDGE_REPORT.md`. Recommendation REVISE; real PZ

combat, dedicated multiplayer and Linux loading remain untested. The bridge and

fixture stay outside runtime source and are not automatically deployed.


Current read-only inventory tooltip implementation and validation: docs/RETAINER_TOOLTIP_INTEGRATION.md (from docs, use RETAINER_TOOLTIP_INTEGRATION.md). Vanilla tooltip remains intact; companion panel displays finite condition and actual reinforcement contributions. Runtime UI and gameplay synchronization remain untested.
