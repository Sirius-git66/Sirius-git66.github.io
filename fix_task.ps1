# PowerShell script to fix the Task Scheduler task
# Delete the existing task
try {
    Unregister-ScheduledTask -TaskName "Refresh Commods Dashboard" -Confirm:$false
    Write-Host "Successfully deleted the existing task"
} catch {
    Write-Host "Failed to delete the existing task: $($_.Exception.Message)"
}

# Create the new task with correct settings
try {
    $action = New-ScheduledTaskAction -Execute "C:\Users\being\OneDrive\Documents\AI Courses\Personal Website\update_dashboard.bat" -WorkingDirectory "C:\Users\being\OneDrive\Documents\AI Courses\Personal Website"
    $trigger = New-ScheduledTaskTrigger -Daily -At 9:09AM
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable
    $principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount
    
    Register-ScheduledTask -TaskName "Refresh Commods Dashboard" -Action $action -Trigger $trigger -Settings $settings -Principal $principal
    Write-Host "Successfully created the new task"
} catch {
    Write-Host "Failed to create the new task: $($_.Exception.Message)"
}