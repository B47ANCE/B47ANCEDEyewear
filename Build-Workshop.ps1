[CmdletBinding()]
param(
    [string]$WorkshopRoot = (Join-Path $env:USERPROFILE 'Zomboid/Workshop'),
    [ValidateSet('preserve','public','friends','private')][string]$Visibility = 'preserve',
    [string]$PythonExe,
    [string]$ArchiveRoot = (Join-Path $env:USERPROFILE '.codex/artifact-archives/B47ANCEDEyewear')
)
$ErrorActionPreference = 'Stop'
$project = [IO.Path]::GetFullPath($PSScriptRoot)
. (Join-Path $project 'scripts/Workshop-Tools.ps1')
$python = Resolve-WorkshopPython $PythonExe
$version = [IO.File]::ReadAllText((Join-Path $project 'VERSION')).Trim()
$workshopId = [IO.File]::ReadAllText((Join-Path $project 'WORKSHOP_ID.txt')).Trim()
if ($workshopId -ne '3799754736') { throw 'Expected existing Workshop item 3799754736.' }
$source = Join-Path $project 'src/B47ANCEDEyewear/42'
$dist = Join-Path $project 'dist/current'
$archivePath = Join-Path $dist ('B47ANCEDEyewear_v' + $version + '.zip')
if (Test-Path -LiteralPath $archivePath) { throw 'Current package exists; preserve it before rebuilding. Staging was not changed.' }
$stageParent = [IO.Path]::GetFullPath($WorkshopRoot).TrimEnd('\')
$stage = [IO.Path]::GetFullPath((Join-Path $stageParent 'B47ANCEDEyewear'))
if ([IO.Path]::GetDirectoryName($stage) -ne $stageParent) { throw 'Invalid staging path.' }
foreach ($path in @($stageParent,$stage)) {
    if ((Test-Path -LiteralPath $path) -and ((Get-Item -LiteralPath $path).Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Reparse-point Workshop staging is not supported.' }
}
$selectedVisibility = 'private'
if (Test-Path -LiteralPath (Join-Path $stage 'workshop.txt')) {
    $old = Read-WorkshopInfo (Join-Path $stage 'workshop.txt')
    if ($old.id -ne $workshopId) { throw 'Existing staging belongs to another Workshop item.' }
    if ($old.visibility -in @('public','friends','private')) { $selectedVisibility = $old.visibility }
}
if ($Visibility -ne 'preserve') { $selectedVisibility = $Visibility }
Invoke-WorkshopPreflight $python $project @()
if (-not (Test-Path -LiteralPath (Join-Path $project 'thumbnail.png'))) { throw 'Workshop thumbnail is missing.' }
$commit = (& git -C $project rev-parse HEAD | Out-String).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Git source commit is unavailable.' }
$payloadChanges = & git -C $project status --porcelain -- src VERSION WORKSHOP_ID.txt WORKSHOP_DESCRIPTION.txt WORKSHOP_CHANGE_NOTE.txt thumbnail.png version-inventory.json Build-Workshop.ps1 Publish-Workshop.ps1 scripts requirements-tools.txt docs/RELEASE_STATUS.json
if ($payloadChanges) { throw 'Commit the intended release source before generating provenance.' }
$token = [guid]::NewGuid().ToString('N')
$temporary = [IO.Path]::GetFullPath((Join-Path $stageParent ('B47ANCEDEyewear-preparation-' + $token)))
if ([IO.Path]::GetDirectoryName($temporary) -ne $stageParent) { throw 'Invalid preparation path.' }
$temporaryArchiveRoot = Join-Path $project 'dist/preparation'
New-Item -ItemType Directory -Force -Path $temporaryArchiveRoot | Out-Null
$temporaryArchive = Join-Path $temporaryArchiveRoot ('package-' + $token + '.zip')
$content = Join-Path $temporary 'Contents/mods/B47ANCEDEyewear'
New-Item -ItemType Directory -Force -Path (Join-Path $content 'common') | Out-Null
Copy-Item -LiteralPath $source -Destination $content -Recurse
Add-Type -AssemblyName System.Drawing
$original = [Drawing.Image]::FromFile((Join-Path $project 'thumbnail.png'))
$preview = [Drawing.Bitmap]::new(256,256)
$graphics = [Drawing.Graphics]::FromImage($preview)
try {
    $graphics.DrawImage($original,0,0,256,256)
    $preview.Save((Join-Path $temporary 'preview.png'),[Drawing.Imaging.ImageFormat]::Png)
} finally { $graphics.Dispose(); $preview.Dispose(); $original.Dispose() }
$description = [IO.File]::ReadAllText((Join-Path $project 'WORKSHOP_DESCRIPTION.txt')).Trim()
$lines = @('version=1',"title=B47ANCE'd Eyewear [Development Build]","id=$workshopId","visibility=$selectedVisibility")
$lines += @($description -split '\r?\n' | ForEach-Object { 'description=' + $_ })
$lines += 'tags=Build 42;Clothing/Armor;QoL'
[IO.File]::WriteAllLines((Join-Path $temporary 'workshop.txt'),$lines,[Text.UTF8Encoding]::new($false))
$runtime = @(Get-ChildItem -LiteralPath $source -File -Recurse | ForEach-Object {
    @{path=$_.FullName.Substring($source.Length + 1).Replace('\','/');sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
})
$manifest = @{version=$version;commit=$commit;workshop_id=$workshopId;mod_id='B47ANCEDEyewear';app_id=108600;
    target_game='42.21';steam_build='25485521';source_root='src/B47ANCEDEyewear/42';files=$runtime;source_validation='STATIC PASS';
    sp='NOT TESTED';g7='BLOCKED / NOT TESTED';g8='BLOCKED';publication='PREPARED ONLY';
    preview_sha256=(Get-FileHash -LiteralPath (Join-Path $temporary 'preview.png')).Hash.ToLowerInvariant();
    workshop_metadata_sha256=(Get-FileHash -LiteralPath (Join-Path $temporary 'workshop.txt')).Hash.ToLowerInvariant();
    description_sha256=(Get-FileHash -LiteralPath (Join-Path $project 'WORKSHOP_DESCRIPTION.txt')).Hash.ToLowerInvariant();
    changenote_sha256=(Get-FileHash -LiteralPath (Join-Path $project 'WORKSHOP_CHANGE_NOTE.txt')).Hash.ToLowerInvariant()}
[IO.File]::WriteAllText((Join-Path $temporary 'release-manifest.json'),($manifest | ConvertTo-Json -Depth 8),[Text.UTF8Encoding]::new($false))
Add-Type -AssemblyName System.IO.Compression.FileSystem
[IO.Compression.ZipFile]::CreateFromDirectory($temporary,$temporaryArchive)
Invoke-WorkshopPreflight $python $project @('--archive',$temporaryArchive,'--stage',$temporary)
$backupRoot = [IO.Path]::GetFullPath($ArchiveRoot)
$backup = [IO.Path]::GetFullPath((Join-Path $backupRoot ('staging-backup-' + $token)))
if ([IO.Path]::GetDirectoryName($backup) -ne $backupRoot) { throw 'Invalid staging backup path.' }
New-Item -ItemType Directory -Force -Path $backupRoot,$dist | Out-Null
$replaced = $false
try {
    if (Test-Path -LiteralPath $stage) { Move-Item -LiteralPath $stage -Destination $backup; $replaced = $true }
    Move-Item -LiteralPath $temporary -Destination $stage
    Move-Item -LiteralPath $temporaryArchive -Destination $archivePath
$hash = (Get-FileHash -LiteralPath $archivePath -Algorithm SHA256).Hash.ToLowerInvariant()
[IO.File]::WriteAllText(($archivePath + '.sha256'),($hash + '  ' + [IO.Path]::GetFileName($archivePath) + "`n"),[Text.UTF8Encoding]::new($false))
$manifest.package_sha256 = $hash
[IO.File]::WriteAllText((Join-Path $dist 'release-provenance.json'),($manifest | ConvertTo-Json -Depth 8),[Text.UTF8Encoding]::new($false))
& $python -B (Join-Path $project 'scripts/check_versions.py') --root $project --release
if ($LASTEXITCODE -ne 0) { throw 'Prepared artifact version consistency failed.' }
} catch {
    if (Test-Path -LiteralPath $archivePath) { Move-Item -LiteralPath $archivePath -Destination $temporaryArchive }
    if (Test-Path -LiteralPath ($archivePath+'.sha256')) { Move-Item -LiteralPath ($archivePath+'.sha256') -Destination ($temporaryArchive+'.sha256') }
    $provenancePath=Join-Path $dist 'release-provenance.json'
    if (Test-Path -LiteralPath $provenancePath) { Move-Item -LiteralPath $provenancePath -Destination (Join-Path $temporaryArchiveRoot ('failed-provenance-'+$token+'.json')) }
    if ($replaced -and (Test-Path -LiteralPath $backup)) {
        if (Test-Path -LiteralPath $stage) { Move-Item -LiteralPath $stage -Destination $temporary }
        Move-Item -LiteralPath $backup -Destination $stage
    }
    throw
}
Write-Output "Prepared $($runtime.Count) Lua-only runtime files. No test suite or debugger grant code is included."
Write-Output "Workshop staging: $stage"
Write-Output "Archive: $archivePath"
Write-Output 'MP testing distribution needs an explicit publish request; stable G7/G8 remain blocked. SteamCMD was not invoked.'
