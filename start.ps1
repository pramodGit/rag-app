# Start Ollama
Start-Process "ollama" -ArgumentList "serve" -WindowStyle Minimized

Start-Sleep -Seconds 2

# Start Python RAG service (using venv Python directly)
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\rag'; .\venv\Scripts\python.exe -m uvicorn rag_service:app --port 8000" -WindowStyle Normal

Start-Sleep -Seconds 2

# Start Node backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; node server.js" -WindowStyle Normal

Start-Sleep -Seconds 2

# Start Frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm run dev" -WindowStyle Normal

Write-Host "✅ All services started!" -ForegroundColor Green
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host "Node:     http://localhost:5000" -ForegroundColor Cyan
Write-Host "Python:   http://localhost:8000" -ForegroundColor Cyan
Write-Host "Ollama:   http://localhost:11434" -ForegroundColor Cyan