[CmdletBinding(SupportsShouldProcess, ConfirmImpact='High')]
param(
    [Parameter(Mandatory)][ValidateNotNullOrEmpty()][string]$SteamLogin,
    [ValidateSet('public','friends','private')][string]$Visibility = 'public',
    [string]$SteamCmd = 'C:\Users\willi\Tools\SteamCMD\steamcmd.exe',
    [string]$PublishedFileId,
    [string]$WorkshopRoot = 'C:\Users\willi\Zomboid\Workshop',
    [switch]$SkipStaging
)

$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath($PSScriptRoot)
if (-not (Test-Path -LiteralPath $SteamCmd -PathType Leaf)) { throw "SteamCMD not found: $SteamCmd" }
if (-not $SkipStaging) {
    & (Join-Path $root 'Build-Workshop.ps1') -WorkshopRoot $WorkshopRoot -Visibility $Visibility
    if ($LASTEXITCODE -ne 0) { throw 'Workshop staging failed.' }
} else {
    $python = & (Join-Path $root '../tools/Resolve-HostTestPython.ps1')
    & $python -B (Join-Path $root 'scripts/check_versions.py') --root $root --release
    if ($LASTEXITCODE -ne 0) { throw 'Staged package version validation failed.' }
    $runtimeSource = Join-Path $root 'src/B47ANCEDEyewear/42'
    $runtimeStage = Join-Path $WorkshopRoot 'B47ANCEDEyewear/Contents/mods/B47ANCEDEyewear/42'
    $expectedFiles = @(Get-ChildItem -LiteralPath $runtimeSource -File -Recurse)
    $stagedFiles = @(Get-ChildItem -LiteralPath $runtimeStage -File -Recurse)
    if ($expectedFiles.Count -ne $stagedFiles.Count) { throw 'Staged source file count mismatch.' }
    foreach ($file in $expectedFiles) {
        $relative = $file.FullName.Substring($runtimeSource.Length).TrimStart('\')
        $stagedFile = Join-Path $runtimeStage $relative
        if ((Get-FileHash -LiteralPath $file.FullName).Hash -ne (Get-FileHash -LiteralPath $stagedFile).Hash) {
            throw "Staged source mismatch: $relative"
        }
    }
}

$info = @{}
Get-Content -LiteralPath (Join-Path $root 'src\B47ANCEDEyewear\42\mod.info') | Where-Object { $_ -match '^[^=]+=' } | ForEach-Object {
    $key, $value = $_ -split '=', 2; $info[$key] = $value.Trim()
}
$idPath = Join-Path $root 'WORKSHOP_ID.txt'
if (-not $PublishedFileId -and (Test-Path -LiteralPath $idPath)) { $PublishedFileId = (Get-Content -Raw -LiteralPath $idPath).Trim() }
if ($PublishedFileId -and $PublishedFileId -notmatch '^\d{7,20}$') { throw 'PublishedFileId must be a Steam Workshop ID.' }

function VdfEscape([string]$text) { return $text.Replace('\','\\').Replace('"','\"').Replace("`r`n","`n").Replace("`r","`n") }
$visibilityCode = @{ public='0'; friends='1'; private='2' }[$Visibility]
$stage = Join-Path ([IO.Path]::GetFullPath($WorkshopRoot)) 'B47ANCEDEyewear'
$vdfRoot = Join-Path $root 'dist\workshop-publish'
New-Item -ItemType Directory -Path $vdfRoot -Force | Out-Null
$vdf = Join-Path $vdfRoot 'B47ANCEDEyewear.vdf'
$idLine = if ($PublishedFileId) { '    "publishedfileid" "' + (VdfEscape $PublishedFileId) + '"' } else { '' }
$description = (Get-Content -Raw -LiteralPath (Join-Path $root 'WORKSHOP_DESCRIPTION.txt')).Trim()
$note = (Get-Content -Raw -LiteralPath (Join-Path $root 'WORKSHOP_CHANGE_NOTE.txt')).Trim()
@"
"workshopitem"
{
    "appid" "108600"
$idLine
    "contentfolder" "$(VdfEscape ([IO.Path]::GetFullPath((Join-Path $stage 'Contents'))))"
    "previewfile" "$(VdfEscape ([IO.Path]::GetFullPath((Join-Path $stage 'preview.png'))))"
    "visibility" "$visibilityCode"
    "title" "$(VdfEscape ($info.name + ' [Development Build]'))"
    "description" "$(VdfEscape $description)"
    "changenote" "$(VdfEscape $note)"
}
"@ | Set-Content -LiteralPath $vdf -Encoding utf8

if ($PSCmdlet.ShouldProcess("B47ANCE'd Eyewear ($Visibility)", 'Upload verified staged content through SteamCMD')) {
    & $SteamCmd +login $SteamLogin +workshop_build_item $vdf +quit
    if ($LASTEXITCODE -ne 0) { throw "SteamCMD failed with exit code $LASTEXITCODE." }
}
