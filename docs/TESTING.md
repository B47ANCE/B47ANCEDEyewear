# Testing



Run `python -m unittest discover -s "B47ANCEDEyewear/tests" -v` with lupa installed.

Host tests do not establish native or multiplayer readiness.



2026-09-12: host tests cover the CraftRecipe callbacks, current vanilla and

Authentic Z recipe identifiers, material and ownership validation, duplicate

completion, persistence restoration, untie/re-tie, metadata, and description

size. Workspace suite tooling uses a fixed

Works-project registry and does not include this standalone project; the command

above runs its full test suite.



Native gates (all UNVERIFIED):

1. Enable this mod alone in Build 42. Wear prescription glasses. With each

   supported material in main inventory, tie them; verify exactly one use lost.

2. Cancel the action, walk/run, remove the glasses or material while queued;

   verify no tie or material loss. Repeat queued ties; only the first succeeds.

3. Take zombie hits including head hits: tied glasses stay on. Untie and confirm

   normal fall behavior returns. Untied eyewear keeps its established item-specific profile; loose hats keep vanilla behavior.

4. Save/reload while wearing tied glasses; remove/re-equip; drop/pick up; transfer

   to another survivor; confirm tie persists and prescription/condition survive.

5. Untie: no refund, original fall chance restored, repeat untie does nothing.

6. Hosted and dedicated server: repeat with two clients, reconnect/late join,

   verify item use, tie replication, ownership, and combat retention on each peer.



No game launch, live deployment, or publication performed by implementation.



Compatibility update: all 11 host tests PASS. Added all six installed Authentic Z

Current glasses identifiers and a synthetic modded eyewear case covering tie,

restore, untie, wrong slot, and non-clothing rejection. Native checks above must

also be repeated with Authentic Z and the user's exact Frockin glasses pack.

Downloaded-edition follow-up: all 12 host tests PASS, including the six shared

original/Faded Authentic Z eyewear identifiers and rejection of Faded's clown

noses and masks. Volume 6 and Backstage are now inspected; their item scripts

contain no eyewear candidates. See API_EVIDENCE.md for the audit. Native runtime

acceptance remains pending for each Authentic Z edition.



Multiplayer audit: all 16 host tests PASS. New regressions cover explicit client

mutation rejection, early server sync during client presentation, strict server

ownership/material validation despite a started flag, separate peer item state

restoration, and missing client item lookup. These are simulated peers, not live

hosted/dedicated-server results. The six native gates above remain UNVERIFIED.



Retention (0.2.0): all 29 host tests PASS. New regressions cover classification

(secured military/crash/riot/hard-hat helmets versus loose caps, the `hat_army`

prefix without matching `PeakedCapArmy`/`BeretArmy`, and unknown-mod fallback),

the fitted eyewear fall chance, loose-item vanilla-chance restoration on untie,

helmet zero-chance refresh, straw-hat tie/untie, and the registration API.

The inventory context-menu tests cover an item-owned Tie submenu, material

filtering, the unavailable-material tooltip, one single-player commit, and the

multiplayer client request/server inventory-ID validation path. Native hosted

and dedicated validation remain required.



Current rename validation is recorded separately in RENAME_VALIDATION.md. Earlier

counts and dated observations above are historical offline evidence. They are not

renamed-version runtime proof. Include legacy ModData migration, updated save mod

selections, TestKit duplicate prevention, mixed-version command rejection, and

Linux dedicated loading in the native acceptance suite.



2026-10-04 native bridge spike validation for current 0.3.0-dev.1 is recorded in

NATIVE_BRIDGE_REPORT.md. Offline native loading/fixtures are separate from the

44 Python tests. No PZ runtime test or dedicated multiplayer PASS is asserted.


Current read-only inventory tooltip implementation and validation: docs/RETAINER_TOOLTIP_INTEGRATION.md (from docs, use RETAINER_TOOLTIP_INTEGRATION.md). Vanilla tooltip remains intact; companion panel displays finite condition and actual reinforcement contributions. Runtime UI and gameplay synchronization remain untested.
