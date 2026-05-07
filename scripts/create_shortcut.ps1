$WshShell = New-Object -ComObject WScript.Shell
$ShortcutPath = [System.IO.Path]::Combine([Environment]::GetFolderPath("Desktop"), "Moltbot AI.lnk")
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "d:\MERN-FullStack\02_Workouts\Moltbot_ai\moltbot\launch_dev.bat"
$Shortcut.WorkingDirectory = "d:\MERN-FullStack\02_Workouts\Moltbot_ai\moltbot"
$Shortcut.WindowStyle = 7 # Minimized to avoid flash
$Shortcut.Description = "Launch Moltbot AI Assistant"
# Note: IconLocation usually needs an .ico or .exe. 
# We'll point it to our project folder.
$Shortcut.IconLocation = "d:\MERN-FullStack\02_Workouts\Moltbot_ai\moltbot\icon.png" 
$Shortcut.Save()

Write-Host "✅ Shortcut created on Desktop: Moltbot AI"
