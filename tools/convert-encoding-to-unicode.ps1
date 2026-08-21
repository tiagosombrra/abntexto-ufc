param(
  [Parameter(Mandatory = $true)]
  [string]$InputEncoding,

  [Parameter(Mandatory = $true)]
  [string]$OutputEncoding,

  [Parameter(Mandatory = $true)]
  [string]$OutputEncodingName
)

$ErrorActionPreference = 'Stop'

function Resolve-KpseFile([string]$Name) {
  $path = (& kpsewhich $Name).Trim()
  if (-not $path -or -not (Test-Path $path)) {
    throw "Required TeX file not found: $Name"
  }
  return $path
}

function Add-GlyphList([hashtable]$GlyphMap, [string]$Path) {
  foreach ($line in Get-Content $Path) {
    if (-not $line -or $line.StartsWith('#') -or -not $line.Contains(';')) {
      continue
    }

    $parts = $line.Split(';', 2)
    $name = $parts[0].Trim()
    if (-not $name -or $GlyphMap.ContainsKey($name)) {
      continue
    }

    foreach ($candidate in $parts[1].Split(',')) {
      $value = $candidate.Trim()
      if ($value -match '^[0-9A-Fa-f]{4,6}$') {
        $GlyphMap[$name] = $value.ToUpperInvariant()
        break
      }
    }
  }
}

if (-not (Test-Path $InputEncoding)) {
  throw "Input encoding not found: $InputEncoding"
}

$glyphMap = @{}
Add-GlyphList $glyphMap (Resolve-KpseFile 'texglyphlist.txt')
Add-GlyphList $glyphMap (Resolve-KpseFile 'glyphlist.txt')

$lines = @(Get-Content $InputEncoding)
$vectorStart = -1
$vectorEnd = -1

for ($i = 0; $i -lt $lines.Count; $i++) {
  if ($vectorStart -lt 0 -and $lines[$i] -match '^\s*/[^\s]+\s*\[\s*$') {
    $vectorStart = $i
    continue
  }

  if ($vectorStart -ge 0 -and $lines[$i] -match '^\s*\]\s*def\s*$') {
    $vectorEnd = $i
    break
  }
}

if ($vectorStart -lt 0 -or $vectorEnd -le $vectorStart) {
  throw "Encoding vector was not found in: $InputEncoding"
}

$lines[$vectorStart] = "/$OutputEncodingName ["

for ($i = $vectorStart + 1; $i -lt $vectorEnd; $i++) {
  if ($lines[$i] -notmatch '^(\s*)/([^\s%]+)') {
    continue
  }

  $prefix = $Matches[1]
  $glyphName = $Matches[2]
  if ($glyphName -eq '.notdef') {
    continue
  }

  if ($glyphMap.ContainsKey($glyphName)) {
    $replacement = "$prefix/uni$($glyphMap[$glyphName])"
  }
  else {
    $replacement = "$prefix/.notdef"
  }

  $lines[$i] = $lines[$i] -replace '^\s*/[^\s%]+', $replacement
}

$parent = Split-Path -Parent $OutputEncoding
if ($parent) {
  New-Item -ItemType Directory -Force -Path $parent | Out-Null
}

$lines | Set-Content -Path $OutputEncoding -Encoding ascii
Write-Host "Unicode encoding generated: $OutputEncoding"
