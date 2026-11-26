# Interactive last resort for a bug that cannot yet be reproduced automatically.
# Example: powershell -File .\hitl-loop.template.ps1 -Steps 'Open the page and submit the form' -Symptom 'the stated error appears'
param(
    [Parameter(Mandatory = $true)][ValidateNotNullOrEmpty()][string]$Steps,
    [Parameter(Mandatory = $true)][ValidateNotNullOrEmpty()][string]$Symptom
)

Write-Host "Steps: $Steps"
$completed = Read-Host 'Press Enter after completing the steps'
if ($null -eq $completed) {
    Write-Error 'No verdict recorded: input ended.'
    exit 2
}

$answer = Read-Host "Did $Symptom occur? (y/n)"
if ($null -eq $answer) {
    Write-Error 'No verdict recorded: input ended.'
    exit 2
}
$answer = $answer.Trim().ToLowerInvariant()

switch ($answer) {
    'y' { Write-Output 'SYMPTOM_OBSERVED=true (human report)'; exit 1 }
    'n' { Write-Output 'SYMPTOM_OBSERVED=false (human report)'; exit 0 }
    default { Write-Error 'Enter y or n; no verdict recorded.'; exit 2 }
}
