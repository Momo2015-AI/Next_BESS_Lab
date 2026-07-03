$ErrorActionPreference = "Stop"
$base = Split-Path -Parent $PSScriptRoot
$file = Join-Path $base "soh-sim-frontend\src\components\EpcModules.vue"

$content = [System.IO.File]::ReadAllText($file, [System.Text.Encoding]::UTF8)

$rules = @(
  @{old='style="border-color: #e0e0e0"'; new='style="border-color: var(--color-border)"'},
  @{old='style="color: #2f5496"'; new='style="color: var(--color-accent)"'},
  @{old='style="color: #2F5496"'; new='style="color: var(--color-accent)"'},
  @{old='style="color: #999"'; new='style="color: var(--color-text-muted)"'},
  @{old='style="color: #666"'; new='style="color: var(--color-text-secondary)"'},
  @{old='style="background-color: #2f5496"'; new='style="background: var(--color-accent)"'},
  @{old='style="border-color: #bfdbfe"'; new='style="border-color: var(--color-accent-glow)"'},
  @{old="borderColor: '#2F5496'"; new="borderColor: 'var(--color-accent)'"}
)

foreach ($rule in $rules) {
  $old = $rule.old
  $new = $rule.new
  $before = $content
  $content = $content.Replace($old, $new)
  if ($before -ne $content) {
    Write-Host "Replaced: $old"
  } else {
    Write-Host "No match: $old"
  }
}

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($file, $content, $utf8NoBom)
Write-Host "Done: EpcModules.vue"
