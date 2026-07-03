$ErrorActionPreference = "Stop"
$base = Split-Path -Parent $PSScriptRoot

$files = @{
    "soh-sim-frontend\src\components\HomePage.vue" = @(
        @{old='color: #0071e3'; new='color: var(--color-accent)'},
        @{old='color: #1d1d1f'; new='color: var(--color-text)'},
        @{old='color: #f5f5f7'; new='color: var(--color-text)'},
        @{old='color: #86868b'; new='color: var(--color-text-secondary)'},
        @{old='color: #86868B'; new='color: var(--color-text-secondary)'},
        @{old='color: #d2d2d7'; new='color: var(--color-text-muted)'},
        @{old='color: #48484a'; new='color: var(--color-text)'},
        @{old='color: #6e6e73'; new='color: var(--color-text-secondary)'},
        @{old='color: #40a9ff'; new='color: var(--color-accent-secondary)'},
        @{old='color: #30d158'; new='color: var(--color-success)'},
        @{old='background: rgba(0, 113, 227, 0.06)'; new='background: var(--color-accent-glow)'},
        @{old='background: rgba(0, 113, 227, 0.1)'; new='background: var(--color-accent-glow)'},
        @{old='background: rgba(0, 113, 227, 0.2)'; new='background: var(--color-accent-dark)'},
        @{old='background: rgba(0, 113, 227, 0.15)'; new='background: var(--color-accent-dark)'}
    ),
    "soh-sim-frontend\src\components\FormulaLab.vue" = @(
        @{old='style="color: #f59e0b'; new='style="color: var(--color-warning)'},
        @{old='style="color: #3b82f6'; new='style="color: var(--color-accent)'},
        @{old='style="color: #ec4899'; new='style="color: var(--color-info)'},
        @{old='style="color: #eab308'; new='style="color: var(--color-warning)'},
        @{old='style="color: #f97316'; new='style="color: var(--color-warning)'},
        @{old='style="color: #e11d48'; new='style="color: var(--color-danger)'},
        @{old='style="color: #6366f1'; new='style="color: var(--color-accent)'},
        @{old='style="color: #84cc16'; new='style="color: var(--color-success)'},
        @{old='style="color: #8b5cf6'; new='style="color: var(--color-info)'},
        @{old='#1e3a5f, #2f5496'; new='var(--color-accent-dark), var(--color-accent)'}
    ),
    "soh-sim-frontend\src\components\FinancialDashboard.vue" = @(
        @{old='color: #a855f7'; new='color: var(--color-info)'},
        @{old='background-color: rgba(168, 85, 247, 0.2)'; new='background-color: rgba(168, 85, 247, 0.2)'},
        @{old='border-top:1px solid #eee'; new='border-top:1px solid var(--color-border)'}
    ),
    "soh-sim-frontend\src\pages\ToolFinancialPage.vue" = @(),
    "soh-sim-frontend\src\pages\ToolRulesPage.vue" = @(),
    "soh-sim-frontend\src\pages\ToolReportPage.vue" = @(),
    "soh-sim-frontend\src\pages\ToolProjectsPage.vue" = @(),
    "soh-sim-frontend\src\pages\ToolConfigPage.vue" = @(),
    "soh-sim-frontend\src\pages\AuthPage.vue" = @()
}

foreach ($f in $files.Keys) {
    $path = Join-Path $base $f
    if (-not (Test-Path $path)) { Write-Host "SKIP: $f (not found)"; continue }
    $rules = $files[$f]
    if ($rules.Count -eq 0) { Write-Host "SKIP: $f (no rules)"; continue }

    $content = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
    $changed = $false

    foreach ($rule in $rules) {
        $before = $content
        $content = $content.Replace($rule.old, $rule.new)
        if ($before -ne $content) {
            Write-Host "  $($rule.old) => $($rule.new)"
            $changed = $true
        }
    }

    if ($changed) {
        $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
        [System.IO.File]::WriteAllText($path, $content, $utf8NoBom)
        Write-Host "DONE: $f"
    } else {
        Write-Host "NONE: $f"
    }
}
