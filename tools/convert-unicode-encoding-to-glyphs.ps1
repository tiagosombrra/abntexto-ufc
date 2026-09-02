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

function Add-ReverseGlyphList(
  [System.Collections.Generic.Dictionary[string,string]]$Reverse,
  [string]$Path
) {
  foreach ($line in Get-Content $Path) {
    if (-not $line -or $line.StartsWith('#') -or -not $line.Contains(';')) {
      continue
    }

    $parts = $line.Split(';', 2)
    $name = $parts[0].Trim()
    $code = $parts[1].Trim()
    if (-not $name -or $code -notmatch '^[0-9A-Fa-f]{4,6}$') {
      continue
    }

    $key = $code.ToUpperInvariant()
    if (-not $Reverse.ContainsKey($key)) {
      $Reverse[$key] = $name
    }
  }
}

if (-not (Test-Path $InputEncoding)) {
  throw "Input encoding not found: $InputEncoding"
}

$reverse = [System.Collections.Generic.Dictionary[string,string]]::new(
  [System.StringComparer]::OrdinalIgnoreCase
)

# Prefer Adobe glyph names, then TeX-specific names as a fallback.
Add-ReverseGlyphList $reverse (Resolve-KpseFile 'glyphlist.txt')
Add-ReverseGlyphList $reverse (Resolve-KpseFile 'texglyphlist.txt')

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
$mapped = 0
$unmapped = 0

for ($i = $vectorStart + 1; $i -lt $vectorEnd; $i++) {
  if ($lines[$i] -notmatch '^(\s*)/([^\s%]+)') {
    continue
  }

  $prefix = $Matches[1]
  $glyphName = $Matches[2]
  if ($glyphName -eq '.notdef') {
    continue
  }

  if ($glyphName -match '^uni([0-9A-Fa-f]{4,6})$') {
    $code = $Matches[1].ToUpperInvariant()
    if ($reverse.ContainsKey($code)) {
      $lines[$i] = $lines[$i] -replace '^\s*/[^\s%]+', "$prefix/$($reverse[$code])"
      $mapped++
    }
    else {
      $lines[$i] = $lines[$i] -replace '^\s*/[^\s%]+', "$prefix/.notdef"
      $unmapped++
    }
  }
  else {
    # Preserve any already-canonical glyph name.
    $mapped++
  }
}

if ($mapped -eq 0) {
  throw "Encoding conversion produced no mapped glyphs: $InputEncoding"
}

$parent = Split-Path -Parent $OutputEncoding
if ($parent) {
  New-Item -ItemType Directory -Force -Path $parent | Out-Null
}

$lines | Set-Content -Path $OutputEncoding -Encoding ascii
Write-Host "Metric encoding generated: $OutputEncoding (mapped=$mapped, unmapped=$unmapped)"
