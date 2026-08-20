param(
  [string]$TexmfRoot = '',
  [string]$FontsDir = "$env:WINDIR\Fonts"
)

$ErrorActionPreference = 'Stop'

function Require-Command([string]$Name) {
  if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
    throw "Required command not found: $Name"
  }
}

function Run-Command([string]$Name, [string[]]$Arguments) {
  & $Name @Arguments | Out-Null
  if ($LASTEXITCODE -ne 0) {
    throw "$Name failed with exit code $LASTEXITCODE"
  }
}

Require-Command 'kpsewhich'
Require-Command 'ttf2tfm'
Require-Command 'vptovf'
Require-Command 'mktexlsr'

if (-not $TexmfRoot) {
  $TexmfRoot = (& kpsewhich '-var-value=TEXMFHOME').Trim()
}
if (-not $TexmfRoot) {
  throw 'TEXMFHOME could not be resolved.'
}

$encT1 = (& kpsewhich 'tex256.enc').Trim()
$encTs1 = (& kpsewhich 'ts1-winfonts.enc').Trim()
if (-not $encT1 -or -not (Test-Path $encT1)) {
  throw 'tex256.enc was not found. Install the winfonts support files first.'
}
if (-not $encTs1 -or -not (Test-Path $encTs1)) {
  throw 'ts1-winfonts.enc was not found. Install the winfonts support files first.'
}

$fonts = @(
  @{ File = 'times.ttf';   T1 = 'mtmr8t';  RawT1 = 'rmtmr8t';  TS1 = 'mtmr8c';  RawTS1 = 'rmtmr8c';  Ps = 'TimesNewRomanPSMT' },
  @{ File = 'timesi.ttf';  T1 = 'mtmri8t'; RawT1 = 'rmtmri8t'; TS1 = 'mtmri8c'; RawTS1 = 'rmtmri8c'; Ps = 'TimesNewRomanPS-ItalicMT' },
  @{ File = 'timesbd.ttf'; T1 = 'mtmb8t';  RawT1 = 'rmtmb8t';  TS1 = 'mtmb8c';  RawTS1 = 'rmtmb8c';  Ps = 'TimesNewRomanPS-BoldMT' },
  @{ File = 'timesbi.ttf'; T1 = 'mtmbi8t'; RawT1 = 'rmtmbi8t'; TS1 = 'mtmbi8c'; RawTS1 = 'rmtmbi8c'; Ps = 'TimesNewRomanPS-BoldItalicMT' },
  @{ File = 'arial.ttf';   T1 = 'malr8t';  RawT1 = 'rmalr8t';  TS1 = 'malr8c';  RawTS1 = 'rmalr8c';  Ps = 'ArialMT' },
  @{ File = 'ariali.ttf';  T1 = 'malri8t'; RawT1 = 'rmalri8t'; TS1 = 'malri8c'; RawTS1 = 'rmalri8c'; Ps = 'Arial-ItalicMT' },
  @{ File = 'arialbd.ttf'; T1 = 'malb8t';  RawT1 = 'rmalb8t';  TS1 = 'malb8c';  RawTS1 = 'rmalb8c';  Ps = 'Arial-BoldMT' },
  @{ File = 'arialbi.ttf'; T1 = 'malbi8t'; RawT1 = 'rmalbi8t'; TS1 = 'malbi8c'; RawTS1 = 'rmalbi8c'; Ps = 'Arial-BoldItalicMT' }
)

foreach ($font in $fonts) {
  $source = Join-Path $FontsDir $font.File
  if (-not (Test-Path $source)) {
    throw "Microsoft font file not found: $source"
  }
}

$work = Join-Path $env:TEMP "ufctex-winfonts-$PID"
$tfmDir = Join-Path $TexmfRoot 'fonts\tfm\ufctex\windows'
$vfDir = Join-Path $TexmfRoot 'fonts\vf\ufctex\windows'
$ttfDir = Join-Path $TexmfRoot 'fonts\truetype\ufctex\windows'
$encDir = Join-Path $TexmfRoot 'fonts\enc\dvips\ufctex'
$mapDir = Join-Path $TexmfRoot 'fonts\map\pdftex\ufctex'
$texDir = Join-Path $TexmfRoot 'tex\latex\ufctex-winfonts'

New-Item -ItemType Directory -Force -Path $work, $tfmDir, $vfDir, $ttfDir, $encDir, $mapDir, $texDir | Out-Null
Copy-Item $encT1 (Join-Path $encDir 'tex256.enc') -Force
Copy-Item $encTs1 (Join-Path $encDir 'ts1-winfonts.enc') -Force

Push-Location $work
try {
  foreach ($font in $fonts) {
    $source = Join-Path $FontsDir $font.File
    Copy-Item $source (Join-Path $ttfDir $font.File) -Force

    Run-Command 'ttf2tfm' @($source, '-q', '-T', $encT1, '-v', "$($font.T1).vpl", "$($font.RawT1).tfm")
    Run-Command 'vptovf' @("$($font.T1).vpl", "$($font.T1).vf", "$($font.T1).tfm")
    Run-Command 'ttf2tfm' @($source, '-q', '-T', $encTs1, '-v', "$($font.TS1).vpl", "$($font.RawTS1).tfm")
    Run-Command 'vptovf' @("$($font.TS1).vpl", "$($font.TS1).vf", "$($font.TS1).tfm")

    Copy-Item "$($font.RawT1).tfm", "$($font.T1).tfm", "$($font.RawTS1).tfm", "$($font.TS1).tfm" -Destination $tfmDir -Force
    Copy-Item "$($font.T1).vf", "$($font.TS1).vf" -Destination $vfDir -Force
  }
}
finally {
  Pop-Location
}

$map = @()
foreach ($font in $fonts) {
  $map += "$($font.RawT1) $($font.Ps) `"T1Encoding ReEncodeFont`" <[tex256.enc <$($font.File)"
  $map += "$($font.RawTS1) $($font.Ps) `"ts1-winfonts ReEncodeFont`" <[ts1-winfonts.enc <$($font.File)"
}
$map | Set-Content -Path (Join-Path $mapDir 'ufctex-windows.map') -Encoding ascii

@'
\ProvidesFile{t1times-ttf.fd}[2026/08/20 ufctex generated Times New Roman support]
\DeclareFontFamily{T1}{times-ttf}{}
\DeclareFontShape{T1}{times-ttf}{m}{n}{<-> mtmr8t}{}
\DeclareFontShape{T1}{times-ttf}{m}{it}{<-> mtmri8t}{}
\DeclareFontShape{T1}{times-ttf}{m}{sl}{<->ssub * times-ttf/m/it}{}
\DeclareFontShape{T1}{times-ttf}{b}{n}{<-> mtmb8t}{}
\DeclareFontShape{T1}{times-ttf}{b}{it}{<-> mtmbi8t}{}
\DeclareFontShape{T1}{times-ttf}{b}{sl}{<->ssub * times-ttf/b/it}{}
\DeclareFontShape{T1}{times-ttf}{bx}{n}{<->ssub * times-ttf/b/n}{}
\DeclareFontShape{T1}{times-ttf}{bx}{it}{<->ssub * times-ttf/b/it}{}
\DeclareFontShape{T1}{times-ttf}{bx}{sl}{<->ssub * times-ttf/b/it}{}
\endinput
'@ | Set-Content -Path (Join-Path $texDir 't1times-ttf.fd') -Encoding ascii

@'
\ProvidesFile{ts1times-ttf.fd}[2026/08/20 ufctex generated Times New Roman support]
\DeclareFontFamily{TS1}{times-ttf}{}
\DeclareFontShape{TS1}{times-ttf}{m}{n}{<-> mtmr8c}{}
\DeclareFontShape{TS1}{times-ttf}{m}{it}{<-> mtmri8c}{}
\DeclareFontShape{TS1}{times-ttf}{m}{sl}{<->ssub * times-ttf/m/it}{}
\DeclareFontShape{TS1}{times-ttf}{b}{n}{<-> mtmb8c}{}
\DeclareFontShape{TS1}{times-ttf}{b}{it}{<-> mtmbi8c}{}
\DeclareFontShape{TS1}{times-ttf}{b}{sl}{<->ssub * times-ttf/b/it}{}
\DeclareFontShape{TS1}{times-ttf}{bx}{n}{<->ssub * times-ttf/b/n}{}
\DeclareFontShape{TS1}{times-ttf}{bx}{it}{<->ssub * times-ttf/b/it}{}
\DeclareFontShape{TS1}{times-ttf}{bx}{sl}{<->ssub * times-ttf/b/it}{}
\endinput
'@ | Set-Content -Path (Join-Path $texDir 'ts1times-ttf.fd') -Encoding ascii

@'
\ProvidesFile{t1arial.fd}[2026/08/20 ufctex generated Arial support]
\DeclareFontFamily{T1}{arial}{}
\DeclareFontShape{T1}{arial}{m}{n}{<-> malr8t}{}
\DeclareFontShape{T1}{arial}{m}{it}{<-> malri8t}{}
\DeclareFontShape{T1}{arial}{m}{sl}{<->ssub * arial/m/it}{}
\DeclareFontShape{T1}{arial}{b}{n}{<-> malb8t}{}
\DeclareFontShape{T1}{arial}{b}{it}{<-> malbi8t}{}
\DeclareFontShape{T1}{arial}{b}{sl}{<->ssub * arial/b/it}{}
\DeclareFontShape{T1}{arial}{bx}{n}{<->ssub * arial/b/n}{}
\DeclareFontShape{T1}{arial}{bx}{it}{<->ssub * arial/b/it}{}
\DeclareFontShape{T1}{arial}{bx}{sl}{<->ssub * arial/b/it}{}
\endinput
'@ | Set-Content -Path (Join-Path $texDir 't1arial.fd') -Encoding ascii

@'
\ProvidesFile{ts1arial.fd}[2026/08/20 ufctex generated Arial support]
\DeclareFontFamily{TS1}{arial}{}
\DeclareFontShape{TS1}{arial}{m}{n}{<-> malr8c}{}
\DeclareFontShape{TS1}{arial}{m}{it}{<-> malri8c}{}
\DeclareFontShape{TS1}{arial}{m}{sl}{<->ssub * arial/m/it}{}
\DeclareFontShape{TS1}{arial}{b}{n}{<-> malb8c}{}
\DeclareFontShape{TS1}{arial}{b}{it}{<-> malbi8c}{}
\DeclareFontShape{TS1}{arial}{b}{sl}{<->ssub * arial/b/it}{}
\DeclareFontShape{TS1}{arial}{bx}{n}{<->ssub * arial/b/n}{}
\DeclareFontShape{TS1}{arial}{bx}{it}{<->ssub * arial/b/it}{}
\DeclareFontShape{TS1}{arial}{bx}{sl}{<->ssub * arial/b/it}{}
\endinput
'@ | Set-Content -Path (Join-Path $texDir 'ts1arial.fd') -Encoding ascii

@'
\ProvidesFile{ufctex-winfonts-ready.tex}[2026/08/20 ufctex generated Windows font support]
\def\ufctexWindowsFontSupportVersion{2026-08-20}
\endinput
'@ | Set-Content -Path (Join-Path $texDir 'ufctex-winfonts-ready.tex') -Encoding ascii

Run-Command 'mktexlsr' @($TexmfRoot)
Remove-Item $work -Recurse -Force
Write-Host "ufctex Windows font support prepared in $TexmfRoot"
