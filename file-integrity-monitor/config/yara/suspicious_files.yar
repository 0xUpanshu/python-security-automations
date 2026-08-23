rule Suspicious_Powershell
{
    meta:
        description = "Detect Powershell command patterns"
        author = "FIM Project"
        severity = "medium"

    strings:
    $powershell = "powershell" nocase
    $encoded = "-enc" nocase
    $execution = "Invoke-Expression" nocase

    condition:
    2 of them

}