[CmdletBinding(SupportsShouldProcess, ConfirmImpact='High')]
param(
    [string]$SteamLogin,
    [ValidateSet('preserve','public','friends','private')][string]$Visibility = 'preserve',
    [string]$SteamCmd,
    [string]$WorkshopRoot = (Join-Path $env:USERPROFILE 'Zomboid/Workshop'),
    [string]$PythonExe,
    [switch]$PrepareOnly
)
$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath($PSScriptRoot)
. (Join-Path $root 'scripts/Workshop-Tools.ps1')
$python = Resolve-WorkshopPython $PythonExe
$version = [IO.File]::ReadAllText((Join-Path $root 'VERSION')).Trim()
$id = [IO.File]::ReadAllText((Join-Path $root 'WORKSHOP_ID.txt')).Trim()
if ($id -ne '3799754736') { throw 'Expected existing Workshop item 3799754736; new items are prohibited.' }
$stage = Join-Path ([IO.Path]::GetFullPath($WorkshopRoot)) 'B47ANCEDEyewear'
$archive = Join-Path $root ('dist/current/B47ANCEDEyewear_v' + $version + '.zip')
if (-not (Test-Path -LiteralPath $archive)) { throw 'Run Build-Workshop.ps1 to prepare the current package first.' }
Invoke-WorkshopPreflight $python $root @('--archive',$archive,'--stage',$stage)
& $python -B (Join-Path $root 'scripts/check_versions.py') --root $root --release
if ($LASTEXITCODE -ne 0) { throw 'Prepared artifact versions differ.' }
$metadata = Read-WorkshopInfo (Join-Path $stage 'workshop.txt')
if ($metadata.id -ne $id) { throw 'Staging targets a different Workshop item.' }
$selected = if ($Visibility -eq 'preserve') {$metadata.visibility} else {$Visibility}
if ($selected -notin @('public','friends','private')) { throw 'Workshop visibility is unknown.' }
$info = Read-WorkshopInfo (Join-Path $root 'src/B47ANCEDEyewear/42/mod.info')
$description = [IO.File]::ReadAllText((Join-Path $root 'WORKSHOP_DESCRIPTION.txt')).Replace("`r`n","`n").Replace("`r","`n").Trim()
$note = [IO.File]::ReadAllText((Join-Path $root 'WORKSHOP_CHANGE_NOTE.txt')).Replace("`r`n","`n").Replace("`r","`n").Trim()
$visibilityCode = @{public='0';friends='1';private='2'}[$selected]
$output = Join-Path $root 'dist/workshop-publish'
New-Item -ItemType Directory -Force -Path $output | Out-Null
$vdf = Join-Path $output ('B47ANCEDEyewear-' + $version + '.vdf')
$text = @"
"workshopitem"
{
    "appid" "108600"
    "publishedfileid" "$id"
    "contentfolder" "$(Escape-WorkshopVdf (Join-Path $stage 'Contents'))"
    "previewfile" "$(Escape-WorkshopVdf (Join-Path $stage 'preview.png'))"
    "visibility" "$visibilityCode"
    "title" "$(Escape-WorkshopVdf ($info.name + ' [Development Build]'))"
    "description" "$(Escape-WorkshopVdf $description)"
    "changenote" "$(Escape-WorkshopVdf $note)"
}
"@
[IO.File]::WriteAllText($vdf,$text,[Text.UTF8Encoding]::new($false))
& $python -B (Join-Path $root 'scripts/validate_release.py') --vdf $vdf --stage $stage
if ($LASTEXITCODE -ne 0) { throw 'Workshop VDF canonical-text validation failed.' }
if ($PrepareOnly) { Write-Output "Prepared upload metadata: $vdf. SteamCMD was not invoked."; return }
$status = Get-Content -LiteralPath (Join-Path $root 'docs/RELEASE_STATUS.json') -Raw | ConvertFrom-Json
$commit = (& git -C $root rev-parse HEAD | Out-String).Trim()
if (-not $description.Contains('MP testing build - dedicated multiplayer NOT TESTED') -or
    -not $note.Contains('MP testing build - dedicated multiplayer NOT TESTED')) {
    throw 'This development uploader requires the MP-testing notice in both canonical texts.'
}
& git -C $root fetch origin
if ($LASTEXITCODE -ne 0) { throw 'Cannot verify repository freshness.' }
$counts = (& git -C $root rev-list --left-right --count 'HEAD...@{upstream}' | Out-String).Trim()
if ($LASTEXITCODE -ne 0 -or $counts -notmatch '^0\s+0$') { throw 'Publish source does not match its verified upstream.' }
$defaultRef = (& git -C $root symbolic-ref refs/remotes/origin/HEAD | Out-String).Trim()
if ($LASTEXITCODE -ne 0 -or -not $defaultRef) { throw 'Remote default branch is unknown.' }
& git -C $root merge-base --is-ancestor $defaultRef HEAD
if ($LASTEXITCODE -ne 0) { throw 'Source does not include current remote default branch.' }
$changes = & git -C $root status --porcelain -- src VERSION WORKSHOP_ID.txt WORKSHOP_DESCRIPTION.txt WORKSHOP_CHANGE_NOTE.txt thumbnail.png version-inventory.json Build-Workshop.ps1 Publish-Workshop.ps1 scripts requirements-tools.txt docs/RELEASE_STATUS.json
if ($changes) { throw 'Uncommitted release source blocks upload.' }
$provenance = Get-Content -LiteralPath (Join-Path $root 'dist/current/release-provenance.json') -Raw | ConvertFrom-Json
if ($provenance.commit -ne $commit -or $provenance.package_sha256 -ne (Get-FileHash -LiteralPath $archive).Hash.ToLowerInvariant()) {
    throw 'Package provenance does not match current source commit/hash.'
}
$repo = Invoke-RestMethod -Uri 'https://api.github.com/repos/B47ANCE/B47ANCEDEyewear'
if ($repo.private) { throw 'Source repository must be public.' }
if (-not $SteamLogin -or -not $SteamCmd -or -not (Test-Path -LiteralPath $SteamCmd -PathType Leaf)) {
    throw 'Provide the verified SteamCMD executable and cached-login account. Never put passwords or tokens in files.'
}
if ($PSCmdlet.ShouldProcess("B47ANCE'd Eyewear item $id ($selected)", 'Upload verified content through SteamCMD')) {
    $result = & $SteamCmd +login $SteamLogin +workshop_build_item $vdf +quit 2>&1
    $exitCode = $LASTEXITCODE
    $result | Write-Output
    if ($exitCode -ne 0 -or (($result | Out-String) -notmatch 'Committing update\.\.\.Success')) {
        throw 'SteamCMD did not confirm a successful committed update.'
    }
    $remote = Invoke-RestMethod -Method Post -Uri 'https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/' -Body @{itemcount=1;'publishedfileids[0]'=$id}
    $item = $remote.response.publishedfiledetails[0]
    if ($item.result -ne 1 -or $item.description.Replace("`r`n","`n").Trim() -ne $description) {
        throw 'Steam API could not verify the canonical published description.'
    }
    Write-Output "Verified Workshop update: https://steamcommunity.com/sharedfiles/filedetails/?id=$id"
}
