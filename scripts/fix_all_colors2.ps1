$ErrorActionPreference = "Continue"
$base = Split-Path -Parent $PSScriptRoot

function Fix-File($filePath, $rules) {
    $path = Join-Path $base $filePath
    if (-not (Test-Path $path)) { Write-Host "SKIP: $filePath"; return }
    $content = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
    $changed = $false
    foreach ($rule in $rules) {
        $before = $content
        $content = $content.Replace($rule[0], $rule[1])
        if ($before -ne $content) { Write-Host "  REPL: $($rule[0])"; $changed = $true }
    }
    if ($changed) {
        $utf8 = New-Object System.Text.UTF8Encoding($false)
        [System.IO.File]::WriteAllText($path, $content, $utf8)
        Write-Host "DONE: $filePath"
    } else { Write-Host "NONE: $filePath" }
}

# ---- HomePage.vue ----
Fix-File "soh-sim-frontend\src\components\HomePage.vue" @(
    ,@('color: #0071e3', 'color: var(--color-accent)'),
    ,@('color: #1d1d1f', 'color: var(--color-text)'),
    ,@('color: #f5f5f7', 'color: var(--color-text)'),
    ,@('color: #86868b', 'color: var(--color-text-secondary)'),
    ,@('color: #d2d2d7', 'color: var(--color-text-muted)'),
    ,@('color: #48484a', 'color: var(--color-text)'),
    ,@('color: #6e6e73', 'color: var(--color-text-secondary)'),
    ,@('color: #40a9ff', 'color: var(--color-accent-secondary)'),
    ,@('color: #30d158', 'color: var(--color-success)')
)

# ---- FormulaLab.vue ----
Fix-File "soh-sim-frontend\src\components\FormulaLab.vue" @(
    ,@('style="color: #f59e0b"', 'style="color: var(--color-warning)"'),
    ,@('style="color: #3b82f6"', 'style="color: var(--color-accent)"'),
    ,@('style="color: #ec4899"', 'style="color: var(--color-info)"'),
    ,@('style="color: #eab308"', 'style="color: var(--color-warning)"'),
    ,@('style="color: #f97316"', 'style="color: var(--color-warning)"'),
    ,@('style="color: #e11d48"', 'style="color: var(--color-danger)"'),
    ,@('style="color: #6366f1"', 'style="color: var(--color-accent)"'),
    ,@('style="color: #84cc16"', 'style="color: var(--color-success)"'),
    ,@('style="color: #8b5cf6"', 'style="color: var(--color-info)"'),
    ,@('color: #f59e0b; border-color: #f59e0b', 'color: var(--color-warning); border-color: var(--color-warning)'),
    ,@('#1e3a5f, #2f5496', 'var(--color-accent-dark), var(--color-accent)')
)

# ---- FinancialDashboard.vue ----
Fix-File "soh-sim-frontend\src\components\FinancialDashboard.vue" @(
    ,@('color: #a855f7', 'color: var(--color-info)'),
    ,@('border-top:1px solid #eee', 'border-top:1px solid var(--color-border)')
)

Write-Host "All done."
