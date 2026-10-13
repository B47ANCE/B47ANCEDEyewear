[CmdletBinding()]
param([string]$WorkshopRoot = 'C:\Users\willi\Zomboid\Workshop',
      [ValidateSet('preserve','public','friends','private')][string]$Visibility = 'preserve')
$ErrorActionPreference = 'Stop'
$project = [IO.Path]::GetFullPath($PSScriptRoot)
$source = Join-Path $project 'src/B47ANCEDEyewear'
$dist = Join-Path $project 'dist/current'
$stage = [IO.Path]::GetFullPath((Join-Path $WorkshopRoot 'B47ANCEDEyewear'))
$stageParent = [IO.Path]::GetFullPath($WorkshopRoot).TrimEnd('\')
if ([IO.Path]::GetDirectoryName($stage) -ne $stageParent) { throw 'Invalid staging path' }
$version = (Get-Content -LiteralPath (Join-Path $project 'VERSION') -Raw).Trim()
$description = [IO.File]::ReadAllText((Join-Path $project 'WORKSHOP_DESCRIPTION.txt')).Trim()
if ([Text.Encoding]::UTF8.GetByteCount($description) -gt 8000) { throw 'Description exceeds Workshop limit' }
$python = & (Join-Path $project '../tools/Resolve-HostTestPython.ps1')
& $python -B (Join-Path $project 'scripts/check_versions.py') --root $project
if ($LASTEXITCODE -ne 0) { throw 'Version validation failed' }
& $python -B -m unittest discover -s (Join-Path $project 'tests') -v
if ($LASTEXITCODE -ne 0) { throw 'Host validation failed' }
# Old artwork is archived, never shipped under the new identity. Fail before
# changing staging or creating an archive until replacement artwork is supplied.
if (-not (Test-Path -LiteralPath (Join-Path $project 'thumbnail.png') -PathType Leaf)) {
    throw "Replacement B47ANCE'd Eyewear thumbnail.png is required; Workshop packaging is blocked."
}
New-Item -ItemType Directory -Force -Path $dist | Out-Null
$workshopId = (Get-Content -LiteralPath (Join-Path $project 'WORKSHOP_ID.txt') -Raw).Trim()
$metadata = @("id=$workshopId", 'visibility=private')
if (Test-Path -LiteralPath $stage) {
    $oldInfo = Join-Path $stage 'workshop.txt'
    if (Test-Path -LiteralPath $oldInfo) {
        $oldMetadata = @(Get-Content -LiteralPath $oldInfo | Where-Object { $_ -match '^(id|visibility)=' })
        $oldId = $oldMetadata | Where-Object { $_ -match '^id=\d{7,20}$' } | Select-Object -First 1
        $oldVisibility = $oldMetadata | Where-Object { $_ -match '^visibility=(public|friends|private)$' } | Select-Object -First 1
        if ($oldId) { $metadata[0] = $oldId }
        if ($oldVisibility) { $metadata[1] = $oldVisibility }
    }
    $backupRoot = [IO.Path]::GetFullPath((Join-Path $project 'historical/artifacts'))
    $backup = [IO.Path]::GetFullPath((Join-Path $backupRoot ('staging-backup-' + [guid]::NewGuid().ToString('N'))))
    if ([IO.Path]::GetDirectoryName($backup) -ne $backupRoot) { throw 'Invalid backup path' }
    Move-Item -LiteralPath $stage -Destination $backup
}
if ($Visibility -ne 'preserve') { $metadata[1] = 'visibility=' + $Visibility }
$content = Join-Path $stage 'Contents/mods/B47ANCEDEyewear'
New-Item -ItemType Directory -Force -Path (Join-Path $content 'common') | Out-Null
Copy-Item -LiteralPath (Join-Path $source '42') -Destination $content -Recurse
# Repository markers and all host tests stay outside Workshop content.
$shipping = @(Get-ChildItem -LiteralPath (Join-Path $source '42') -Recurse -File)
# TestKit.lua is an intentional player-facing runtime command. Host tests and
# repository artifacts live outside 42/, so only reject executable test files
# and debug artifacts that would be accidental Workshop content.
if ($shipping | Where-Object { $_.Extension -in @('.py','.pyc') -or $_.Name -match '(?i)debug|test.*\.(py|pyc)$' }) {
    throw 'Development files found in runtime source'
}
Add-Type -AssemblyName System.Drawing
$original = [Drawing.Image]::FromFile((Join-Path $project 'thumbnail.png'))
$preview = [Drawing.Bitmap]::new(256,256)
$graphics = [Drawing.Graphics]::FromImage($preview)
try {
    $graphics.InterpolationMode = [Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graphics.DrawImage($original,0,0,256,256)
    $preview.Save((Join-Path $stage 'preview.png'),[Drawing.Imaging.ImageFormat]::Png)
} finally { $graphics.Dispose(); $preview.Dispose(); $original.Dispose() }
$lines = @('version=1',"title=B47ANCE'd Eyewear [Development Build]") + $metadata
$lines += @($description -split '\r?\n' | ForEach-Object { 'description=' + $_ })
$lines += 'tags=Build 42;Clothing/Armor;QoL'
[IO.File]::WriteAllLines((Join-Path $stage 'workshop.txt'),$lines,[Text.UTF8Encoding]::new($false))
Add-Type -AssemblyName System.IO.Compression.FileSystem
$archivePath = Join-Path $dist ('B47ANCEDEyewear_v' + $version + '.zip')
if (Test-Path -LiteralPath $archivePath) { throw 'Current archive already exists; preserve or archive it before rebuilding.' }
[IO.Compression.ZipFile]::CreateFromDirectory($stage,$archivePath)
$archive = [IO.Compression.ZipFile]::OpenRead($archivePath)
try {
    foreach ($file in $shipping) {
        $relative = $file.FullName.Substring($source.Length + 1)
        $staged = Join-Path $content $relative
        $expected = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash
        if ((Get-FileHash -LiteralPath $staged -Algorithm SHA256).Hash -ne $expected) { throw "Staging mismatch: $relative" }
            $lookup = 'Contents/mods/B47ANCEDEyewear/' + $relative.Replace('\', '/')
            $entry = $null
            foreach ($candidate in $archive.Entries) {
                if ($candidate.FullName.Replace('\', '/') -eq $lookup) { $entry = $candidate; break }
            }
            if (!$entry) { throw "ZIP missing: $relative" }
        $stream = $entry.Open(); $sha = [Security.Cryptography.SHA256]::Create()
        try { $actual = [BitConverter]::ToString($sha.ComputeHash($stream)).Replace('-','') }
        finally { $stream.Dispose(); $sha.Dispose() }
        if ($actual -ne $expected) { throw "ZIP mismatch: $relative" }
    }
    $packagedFiles = @($archive.Entries | Where-Object { $_.Name -ne '' })
    if ($packagedFiles.Count -ne $shipping.Count + 2) { throw 'Unexpected packaged files' }
} finally { $archive.Dispose() }
$hash = Get-FileHash -LiteralPath $archivePath -Algorithm SHA256
[IO.File]::WriteAllText(($archivePath + '.sha256'),($hash.Hash + '  ' + [IO.Path]::GetFileName($archivePath) + "`n"))
& $python -B (Join-Path $project 'scripts/check_versions.py') --root $project --release
if ($LASTEXITCODE -ne 0) { throw 'Packaged version validation failed' }
Write-Output "Verified $($shipping.Count) runtime files against source, staging, and ZIP."
Write-Output "Workshop staging: $stage"
Write-Output "Archive: $archivePath"
