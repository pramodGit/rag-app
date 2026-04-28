# Stop
taskkill /F /IM ollama.exe 2>$null
taskkill /F /IM node.exe 2>$null
taskkill /F /IM python.exe 2>$null

Write-Host "⏹ Stopped all services" -ForegroundColor Red
Start-Sleep -Seconds 2

# Start
.\start.ps1