$ErrorActionPreference = 'Stop'
function Resolve-WorkshopPython([string]$PythonExe) {
    $candidates = @($PythonExe, $env:PZ_TOOL_PYTHON,
        (Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'))
    $command = Get-Command python -ErrorAction SilentlyContinue
    if ($command) { $candidates += $command.Source }
    foreach ($candidate in $candidates) {
        if (-not $candidate -or $candidate -match 'WindowsApps' -or -not (Test-Path -LiteralPath $candidate -PathType Leaf)) { continue }
        $null = & $candidate -c 'from lupa.lua51 import LuaRuntime' 2>&1
        if ($LASTEXITCODE -eq 0) { return [IO.Path]::GetFullPath($candidate) }
    }
    throw 'A Python interpreter with the release-tool dependency lupa is required. Pass -PythonExe and install requirements-tools.txt; no tests are run.'
}
function Invoke-WorkshopPreflight([string]$PythonExe, [string]$Project, [string[]]$Arguments) {
    & $PythonExe -B (Join-Path $Project 'scripts/check_versions.py') --root $Project
    if ($LASTEXITCODE -ne 0) { throw 'Project version consistency failed.' }
    & $PythonExe -B (Join-Path $Project 'scripts/validate_release.py') @Arguments
    if ($LASTEXITCODE -ne 0) { throw 'Production source/package preflight failed.' }
}
function Read-WorkshopInfo([string]$Path) {
    $info = @{}
    foreach ($line in [IO.File]::ReadAllLines($Path)) {
        if ($line -match '^([^=]+)=(.*)$') { $info[$Matches[1]] = $Matches[2].Trim() }
    }
    return $info
}
function Escape-WorkshopVdf([string]$Text) {
    return $Text.Replace('\','\\').Replace('"','\"').Replace("`r`n","`n").Replace("`r","`n")
}
