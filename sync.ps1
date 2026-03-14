$InitPath = "lserp_customization\__init__.py"
$Pattern = "__version__ = '(.*)'"

$Content = Get-Content $InitPath
$NewContent = @()
$CurrentVersion = ""
$NewVersion = ""

foreach ($Line in $Content) {
    if ($Line -match $Pattern) {
        $CurrentVersion = $Matches[1]
        $Parts = $CurrentVersion.Split('.')
        $Patch = [int]$Parts[2] + 1
        $NewVersion = "$($Parts[0]).$($Parts[1]).$Patch"
        $NewContent += "__version__ = '$NewVersion'"
        Write-Host "Bumping version from $CurrentVersion to $NewVersion..." -ForegroundColor Green
    } else {
        $NewContent += $Line
    }
}

Set-Content -Path $InitPath -Value $NewContent

Write-Host "Syncing to git..." -ForegroundColor Cyan
git add .
git commit -m "chore(sync): auto-bump version to $NewVersion"
git push origin master

Write-Host "Sync complete! New version is $NewVersion" -ForegroundColor Green
