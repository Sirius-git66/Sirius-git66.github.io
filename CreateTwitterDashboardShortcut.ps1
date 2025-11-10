# Create desktop shortcut for Twitter Dashboard Setup
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = "$DesktopPath\Twitter Dashboard Setup.lnk"
$TargetPath = "c:\Users\being\OneDrive\Documents\AI Courses\Personal Website\setup_twitter_dashboard.bat"
$WorkingDirectory = "c:\Users\being\OneDrive\Documents\AI Courses\Personal Website"
$IconLocation = "shell32.dll,14"

# Create the shortcut
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetPath
$Shortcut.WorkingDirectory = $WorkingDirectory
$Shortcut.IconLocation = $IconLocation
$Shortcut.Save()

Write-Host "Desktop shortcut 'Twitter Dashboard Setup' created successfully!" -ForegroundColor Green
Write-Host "You can now double-click this shortcut to set up your Twitter accounts." -ForegroundColor Yellow