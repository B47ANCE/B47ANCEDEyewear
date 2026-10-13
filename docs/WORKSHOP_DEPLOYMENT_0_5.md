# Workshop development publication

Project Version: 0.5.0-dev.1
Published: 2026-10-10 America/Phoenix, by explicit user request.
Item: https://steamcommunity.com/sharedfiles/filedetails/?id=3799754736
Title: B47ANCE'd Eyewear [Development Build]
Visibility: public (0); same item preserved.

[VERIFIED] SteamCMD exit 0 and Committing update...Success. Steam published-file API result=1 independently confirms current version, title, visibility and bridge exclusion. Response: dist/workshop-publish/published-details-0.5.0-dev.1.json. Logs: native/build/workshop-0.5-build.log and workshop-0.5-publish.log.

[TESTED: offline Windows] 63 tests PASS; all 131 runtime files have source/staging/ZIP SHA-256 parity; declared version/artifact checks --release PASS. Includes Lua finite-retainer candidate and read-only tooltip. Java bridge, permanent-item gameplay, rare loot and worn visuals excluded. Native bridge requires separate exact-build loading; Workshop subscription does not enable finite catches.

No PZ/server launch or live mod deployment. UI/runtime and dedicated MP are NOT TESTED; gameplay G7 and readiness G8 remain BLOCKED. This authorized publication is an unfinished development upload, not stable/MP certification.

Commands:
```powershell
./B47ANCEDEyewear/Build-Workshop.ps1 -Visibility public
./B47ANCEDEyewear/Publish-Workshop.ps1 -SteamLogin <cached-account> -Visibility public -PublishedFileId 3799754736 -SkipStaging -Confirm:$false
```

ZIP SHA-256: B2DE2D8AC3BCFA48122B8E79AD8EE326E9193A30968821E4422072109121EEA8  B47ANCEDEyewear_v0.5.0-dev.1.zip
