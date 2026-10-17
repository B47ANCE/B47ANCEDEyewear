# Retainer tooltip integration

Project Version: 0.5.0-dev.1
Date: 2026-10-10
Change classification: MINOR, additive presentation capability. Gameplay balance, consumption, native interception and schema are unchanged.

## Source evidence and integration

[VERIFIED: source inspection] Installed Build 42.21 client ISUI/ISToolTipInv.lua defines render(), delegates measurement/drawing to item:DoTooltip(), and handles mouse positioning, controller joyfocus and context-menu overlap. SHA-256: 6f36edfb2447f9faa55301c3d150ab0d76a574c9dbb661812eeaa87d736967e6. ISInventoryPane.lua:858 and ISInventoryPaneContextMenu.lua:3762 instantiate this class. These are inspected installed files, not edited upstream files.

RetainerTooltip.lua chains the existing ISToolTipInv.render implementation once and returns its result. An independently positioned companion ISPanel extends the inspection surface; the original item tooltip, measurements and other mods' chained render content remain intact. Mouse/controller anchor positions come from the already rendered tooltip. An invisible owner removes the companion. Existing context-menu suppression also hides it. The panel adds no input actions or inventory scans.

The companion wraps UTF-8 text using the current Small-font measurements and derives row height from the active text manager. Placement tries below, right, left and above without overlapping the original. [RUNTIME GATE] If no non-overlapping space exists, the companion is omitted to preserve vanilla. Actual supported resolutions/UI scales and extreme large-tooltip cases need visual validation; offline geometry is not a screenshot.

## Read-only presentation contract

RetainerPresentation.lua reads only the current inspected InventoryItem ModData. No owner/worn requirement is imposed for presentation, so container and transferred-item inspection can use the same replicated values. No writes, migrations, network requests, transaction callbacks, RNG, or sandbox changes occur.

Finite schema-2 state displays material, condition, current/stored maximum, proportional colored bar and percentage. Persisted contribution explains base and additional strands; the tape contribution is the stored maximum minus the installed strand subtotal. Changing sandbox values cannot rewrite the historical contribution. One strand and absent tape generate no zero/unused modifier rows.

Conditions use the requested threshold table: Secure >75%, Worn >50%, Fraying/Stretched/Damaged >25%, About to Break >0%, Broken at zero. The handoff's example calls 50% Worn but its table assigns 50% to the damaged tier; this implementation follows the table and uses Fraying for floss. Rubber bands use Stretched; wire and zip ties use Damaged.

A presentation-only permanent fixture requires schema 2, kind permanent, permanent=true, the reserved original custom FullType and revision, with no finite current/maximum, layers, tape or contribution. It renders Permanent/Infinite and no bar or modifiers. This does not create or authorize a permanent gameplay item; ownership/persistence remains blocked.

Absent metadata leaves vanilla unchanged. Invalid, unknown or contradictory state displays localized information-unavailable text and one diagnostic per tooltip instance. No synthetic durability is invented.

## State refresh and known schema limitation

Each visible render reads only its own item's authoritative metadata. New replicated values update the open companion on its next render. Existing server syncItemModData / syncItemFields calls and vanilla item transfer/save serialization are dependencies; this UI does not provide replacement networking or prove those operations in multiplayer.

[UNKNOWN / schema limitation] Manual destructive makeshift removal and the final breaking catch both persist current=0 without a removal discriminator. UI cannot distinguish them without a gameplay/schema change. Both display Broken, while an absent record displays no section. The handoff authorizes presentation only, so no gameplay tombstone has been rewritten. Gameplay-produced permanent replacement is also unavailable.

## Modified files

- New client/B47ANCEDEyewear/RetainerPresentation.lua and RetainerTooltip.lua.
- All 29 shared/Translate/*/UI.json files: 21 additional English-fallback keys.
- New tests/test_retainer_tooltip.py; test_glasses.py's verified vanilla require allowlist.
- VERSION, mod.info, version-inventory.json, CHANGELOG.md, README.md, native/README.md, Workshop description/change note, ROADMAP.md, TESTING.md, ARCHITECTURE.md and this report.
- The 0.4.0 implementation report remains historical evidence; no old runtime/native checks were relabeled as tooltip proof. Old native/build outputs remain historical development outputs; no new native binary or Workshop package was produced.

## Validation

| Check | Status | Evidence |
| --- | --- | --- |
| Installed tooltip integration point | PASS | Source inspection above |
| Percentage, material contributions, tape, snapshot maximum, no repair | PASS | Offline Lupa tests |
| Permanent/no-retainer/malformed states | PASS | Deterministic fixtures, not live gameplay |
| Read-only state and open-tooltip refresh | PASS | Offline tests |
| Vanilla delegation and UTF-8 wrapping/placement | PASS | Mock UI and geometry tests |
| 29-language key/placeholder parity and all Lua syntax | PASS | Full project suite |
| Actual UI, controller, container, scaling and clipping | NOT TESTED | No PZ launch authorized for this work |
| Actual catch-driven durability replication, transfers, reconnect/restart | BLOCKED / NOT TESTED | Existing gameplay/native and dedicated MP gates |

Commands (workspace root):

```powershell
$pzPython = & ./tools/Resolve-HostTestPython.ps1
& $pzPython -B -m unittest discover -s B47ANCEDEyewear/tests -v
& $pzPython B47ANCEDEyewear/scripts/check_versions.py
```

[TESTED: offline Windows Python 3.12 / Lupa 2.6] 63 tests PASS, including 9 new tooltip tests. Log: native/build/tooltip-tests.log. Pinned host-test dependency was restored with bundled Python -m pip install -r tools/host-test-requirements.txt because the refreshed bundled runtime lacked Lupa.

The new feature is proven read-only local presentation: G7 N/A for this bounded UI change. The enclosing gameplay candidate still has G7 BLOCKED / NOT TESTED and G8 BLOCKED. No live durability, release, Linux UI or MP readiness is claimed. No game/server launch, live deployment, publication or mockup-as-runtime evidence.
