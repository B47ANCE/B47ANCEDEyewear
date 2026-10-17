# Workshop development deployment

Project Version: 0.3.0-dev.1

Published 2026-10-04 America/Phoenix, by explicit user request.
Workshop item: https://steamcommunity.com/sharedfiles/filedetails/?id=3799754736
Title: B47ANCE'd Eyewear [Development Build]. Existing public visibility preserved.
SteamCMD cached login/upload completed with Committing update...Success.
Steam published-file API independently confirmed title, visibility0, development
notice and native/retainer exclusion. API response is preserved in
`dist/workshop-publish/published-details.json`.

Uploaded current Lua source only:66 runtime files, new procedural development
preview, identity migration and current change notes. No Java agent, fixtures,
research/decompiler output, assets-in-preparation or retainer expansion gameplay.
No live mod deployment or game/server launch in this publishing task.

Validation:44 offline tests PASS; source/staging/ZIP SHA-256 parity PASS;
`scripts/check_versions.py --root B47ANCEDEyewear --release` PASS for declared
version mirrors/artifacts. This version check does not satisfy native/MP gates.
G7 remains BLOCKED / NOT TESTED; G8 release-readiness remains BLOCKED. User
explicitly authorized publishing this unfinished development build; this is not
stable or multiplayer-certified release evidence.

Package metadata was regenerated with public visibility to match the successful
upload. Content/preview stayed unchanged. Current ZIP SHA-256:
2c7a19b3ba3778805c349a4b6dffee7595147b2d7b9389081497da434fa1b8e6

The successful upload's initial local private-metadata ZIP snapshot is preserved
under historical/artifacts/development-upload-20261004. The earlier CRLF metadata
version-check failure snapshot is retained separately. Active mod.info uses LF
line endings so ZIP version selection agrees with source version selection.

Preview:original procedural typography/glasses artwork created for this
publication, using installed Bahnschrift for rendered text; no font binary or
third-party mod art is included. Replacement historical artwork remains archived.

Commands:
```powershell
./B47ANCEDEyewear/Build-Workshop.ps1 -Visibility public
./B47ANCEDEyewear/Publish-Workshop.ps1 -SteamLogin <cached-account> -Visibility public -PublishedFileId 3799754736 -SkipStaging -Confirm:$false
```
The publish command used the verified initial staging; the final build above
synchronized local visibility metadata afterward. No second upload was needed.
