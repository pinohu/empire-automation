# Execute Day 1 of 90-Day Plan
# PowerShell script to execute all Day 1 tasks

Write-Host "📅 Executing Day 1 of 90-Day Plan" -ForegroundColor Cyan
Write-Host ""

$API_BASE_URL = "http://localhost:8000"

# Step 1: Get Day 1 tasks
Write-Host "[STEP 1] Fetching Day 1 tasks..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$API_BASE_URL/api/90-day-plan/today" -Method Get
    $tasks = $response
    
    if ($tasks.Count -eq 0) {
        Write-Host "  [WARN] No tasks found for Day 1" -ForegroundColor Yellow
        exit 1
    }
    
    Write-Host "  [OK] Found $($tasks.Count) tasks" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Tasks to execute:" -ForegroundColor Cyan
    foreach ($task in $tasks) {
        Write-Host "    - $($task.description)" -ForegroundColor Gray
    }
} catch {
    Write-Host "  [ERROR] Failed to fetch tasks: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 2: Execute each task
Write-Host "[STEP 2] Executing tasks..." -ForegroundColor Yellow
$executed = 0
$failed = 0

foreach ($task in $tasks) {
    $taskId = $task.id
    $description = $task.description
    $agent = $task.agent_assigned
    
    if (-not $agent) {
        $agent = "master-orchestrator"
    }
    
    # Map agent names to API endpoints
    $agentMap = @{
        "entity_manager" = "entity-manager"
        "credential_tracker" = "credential-tracker"
        "professional_services" = "professional-services"
        "directory_manager" = "directory-manager"
        "marketing" = "marketing"
        "financial" = "financial"
        "client_success" = "client-success"
        "master_orchestrator" = "master-orchestrator"
    }
    
    $agentEndpoint = $agentMap[$agent]
    if (-not $agentEndpoint) {
        $agentEndpoint = $agent.Replace("_", "-")
    }
    
    Write-Host "  Executing: $description" -ForegroundColor Gray
    Write-Host "    Agent: $agentEndpoint" -ForegroundColor DarkGray
    
    try {
        $taskPayload = @{
            task_id = $taskId
            description = $description
            parameters = @{
                day_number = 1
                estimated_hours = $task.estimated_hours
                cost = $task.cost
            }
        } | ConvertTo-Json -Depth 10
        
        $executeResponse = Invoke-RestMethod -Uri "$API_BASE_URL/api/agents/$agentEndpoint/execute" -Method Post -Body $taskPayload -ContentType "application/json" -ErrorAction Stop
        
        Write-Host "    [OK] Task executed successfully" -ForegroundColor Green
        $executed++
    } catch {
        Write-Host "    [WARN] Task execution failed: $_" -ForegroundColor Yellow
        $failed++
    }
    
    Write-Host ""
}

# Step 3: Get daily briefing
Write-Host "[STEP 3] Fetching daily briefing..." -ForegroundColor Yellow
try {
    $briefing = Invoke-RestMethod -Uri "$API_BASE_URL/api/daily-briefing" -Method Get
    
    Write-Host "  [OK] Daily briefing retrieved" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Day: $($briefing.day_number)" -ForegroundColor Cyan
    Write-Host "  Total Tasks: $($briefing.total_tasks)" -ForegroundColor Cyan
    Write-Host "  Completed: $($briefing.completed_tasks)" -ForegroundColor Cyan
    Write-Host "  Pending: $($briefing.pending_tasks)" -ForegroundColor Cyan
} catch {
    Write-Host "  [WARN] Could not fetch briefing: $_" -ForegroundColor Yellow
}

Write-Host ""

# Step 4: Summary
Write-Host "[STEP 4] Execution Summary" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Tasks Executed: $executed" -ForegroundColor Green
Write-Host "  Tasks Failed: $failed" -ForegroundColor $(if ($failed -eq 0) { "Green" } else { "Yellow" })
Write-Host "  Success Rate: $([math]::Round(($executed / $tasks.Count) * 100, 1))%" -ForegroundColor Cyan
Write-Host ""

# Step 5: Owner-required tasks reminder
Write-Host "[STEP 5] Owner-Required Tasks Reminder" -ForegroundColor Yellow
Write-Host ""
Write-Host "  The following tasks require your attention:" -ForegroundColor Cyan
Write-Host "    1. File Wyoming annual reports ($1,456)" -ForegroundColor White
Write-Host "    2. Begin SubTo TC certification" -ForegroundColor White
Write-Host "    3. List notary services" -ForegroundColor White
Write-Host ""

Write-Host "✅ Day 1 execution complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Review dashboard: http://localhost:8501" -ForegroundColor White
Write-Host "  2. Complete owner-required tasks" -ForegroundColor White
Write-Host "  3. Review daily briefing in dashboard" -ForegroundColor White
Write-Host "  4. Check financial tracking" -ForegroundColor White
Write-Host ""
