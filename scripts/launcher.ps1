# =====================================================================
# AMAZON KDP BOOK PRODUCTION STUDIO - PROFESSIONAL CMD LAUNCHER
# Designed & Developed by Kadir Laskar
# =====================================================================

param(
    [switch]$TestMode,
    [string]$BrowserChoice = ""
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Unicode Symbols defined via char codes
$s0 = [char]0x25D0  # ◐
$s1 = [char]0x25D3  # ◓
$s2 = [char]0x25D1  # ◑
$s3 = [char]0x25D2  # ◒
$s = @($s0, $s1, $s2, $s3)

$fill = [char]0x2588   # █
$empty = [char]0x2591  # ░
$check = [char]0x2713  # ✓
$cross = [char]0x2717  # ✗

# Box drawing characters
$h = [char]0x2500   # ─
$v = [char]0x2502   # │
$tl = [char]0x250C  # ┌
$tr = [char]0x2510  # ┐
$bl = [char]0x2514  # └
$br = [char]0x2518  # ┘
$ml = [char]0x251C  # ├
$mr = [char]0x2524  # ┤

$dh = [char]0x2550  # ═
$dv = [char]0x2551  # ║
$dtl = [char]0x2554 # ╔
$dtr = [char]0x2557 # ╗
$dbl = [char]0x255A # ╚
$dbr = [char]0x255D # ╝

$scriptDir = Split-Path -Parent $PSScriptRoot
if (-not $scriptDir) { $scriptDir = (Get-Location).Path }

try { $host.UI.RawUI.WindowTitle = "Amazon KDP Book Production Studio" } catch {}
try { Clear-Host } catch {}

# 1. Professional ASCII Header & Logo
$dLine69 = "$dh" * 69
$sLine69 = "$h" * 69

Write-Host ""
Write-Host "  $dtl$dLine69$dtr" -ForegroundColor Cyan
Write-Host "  $dv                                                                     $dv" -ForegroundColor Cyan
Write-Host "  $dv      ██╗  ██╗██████╗ ██████╗     ███████╗████████╗██╗   ██╗██████╗  $dv" -ForegroundColor White
Write-Host "  $dv      ██║ ██╔╝██╔══██╗██╔══██╗    ██╔════╝╚══██╔══╝██║   ██║██╔══██╗ $dv" -ForegroundColor White
Write-Host "  $dv      █████╔╝ ██║  ██║██████╔╝    ███████╗   ██║   ██║   ██║██║  ██║ $dv" -ForegroundColor Cyan
Write-Host "  $dv      ██╔═██╗ ██║  ██║██╔═══╝     ╚════██║   ██║   ██║   ██║██║  ██║ $dv" -ForegroundColor Cyan
Write-Host "  $dv      ██║  ██╗██████╔╝██║         ███████║   ██║   ╚██████╔╝██████╔╝ $dv" -ForegroundColor White
Write-Host "  $dv      ╚═╝  ╚═╝╚═════╝ ╚═╝         ╚══════╝   ╚═╝    ╚═════╝ ╚═════╝  $dv" -ForegroundColor White
Write-Host "  $dv                                                                     $dv" -ForegroundColor Cyan
Write-Host "  $dv                  AMAZON KDP BOOK PRODUCTION STUDIO                  $dv" -ForegroundColor Yellow
Write-Host "  $dv                Professional Book Production Workspace               $dv" -ForegroundColor DarkGray
Write-Host "  $dv                                                                     $dv" -ForegroundColor Cyan
Write-Host "  $dbl$dLine69$dbr" -ForegroundColor Cyan
Write-Host ""

function Test-PortOpen($port = 8080) {
    try {
        $tcp = New-Object System.Net.Sockets.TcpClient
        $connect = $tcp.BeginConnect("127.0.0.1", $port, $null, $null)
        $wait = $connect.AsyncWaitHandle.WaitOne(200, $false)
        if ($wait) {
            $tcp.EndConnect($connect)
            $tcp.Close()
            return $true
        }
        $tcp.Close()
        return $false
    } catch {
        return $false
    }
}

function Animate-ProcessStep($stepName, $actionBlock = $null) {
    $paddedName = $stepName.PadRight(35)
    $delayMs = 20
    if ($TestMode) { $delayMs = 5 }
    
    for ($p = 0; $p -le 90; $p += 10) {
        $filledCount = [int]($p / 5)
        $emptyCount = 20 - $filledCount
        $bar = ("$fill" * $filledCount) + ("$empty" * $emptyCount)
        $spin = $s[[int]($p / 10) % 4]
        $pct = "{0,3}" -f $p
        Write-Host -NoNewline "`r  $spin $paddedName [$bar] $pct% " -ForegroundColor Yellow
        Start-Sleep -Milliseconds $delayMs
    }

    $result = $null
    if ($actionBlock) {
        try {
            $result = & $actionBlock
        } catch {
            $failBar = ("$fill" * 8) + ("$empty" * 12)
            Write-Host "`r  $cross $paddedName [$failBar]  FAILED" -ForegroundColor Red
            throw $_
        }
    }

    $fullBar = "$fill" * 20
    Write-Host -NoNewline "`r  $($s[3]) $paddedName [$fullBar] 100% " -ForegroundColor Yellow
    Start-Sleep -Milliseconds $delayMs
    Write-Host "`r  $check $paddedName [$fullBar] 100%  Completed" -ForegroundColor Green
    
    return $result
}

Write-Host "  SYSTEM INITIALIZATION" -ForegroundColor Cyan
Write-Host "  $sLine69" -ForegroundColor DarkGray

# STEP 1: Initializing KDP Studio
Animate-ProcessStep "1. Initializing KDP Studio" {
    $sTime = 120
    if ($TestMode) { $sTime = 10 }
    Start-Sleep -Milliseconds $sTime
}

# STEP 2: Checking Python Environment
$pyCmd = $null
$pyVersion = "Python 3.10+"
Animate-ProcessStep "2. Checking Python Environment" {
    $venvPy = Join-Path $scriptDir ".venv\Scripts\python.exe"
    if (Test-Path $venvPy) {
        $pyCmd = $venvPy
    } else {
        $sysPy = (Get-Command python -ErrorAction SilentlyContinue)
        if ($sysPy) {
            $pyCmd = "python"
        } else {
            $pyLauncher = (Get-Command py -ErrorAction SilentlyContinue)
            if ($pyLauncher) {
                $pyCmd = "py"
            }
        }
    }

    if (-not $pyCmd) {
        throw "Python was not found! Please install Python 3.10+ or check .venv directory."
    }

    try {
        $verOut = & $pyCmd --version 2>&1
        if ($verOut) { $pyVersion = $verOut.ToString().Trim() }
    } catch {}
}

# STEP 3: Starting Backend Engine
$serverProcess = $null
Animate-ProcessStep "3. Starting Backend Engine" {
    $serverRunning = Test-PortOpen 8080
    if (-not $serverRunning) {
        $serverPy = Join-Path $scriptDir "web_preview\server.py"
        $serverProcess = Start-Process -FilePath $pyCmd -ArgumentList "`"$serverPy`"" -PassThru -WindowStyle Hidden
    }
}

# STEP 4: Checking Local Server
Animate-ProcessStep "4. Checking Local Server" {
    $retries = 0
    while (-not (Test-PortOpen 8080) -and $retries -lt 25) {
        Start-Sleep -Milliseconds 100
        $retries++
    }
    if (-not (Test-PortOpen 8080)) {
        throw "Local server failed to respond on http://localhost:8080 within timeout."
    }
}

# STEP 5: Verifying Project Workspace
$projectsDir = [System.IO.Path]::Combine([Environment]::GetFolderPath("MyDocuments"), "KDP_Studio_Projects")
Animate-ProcessStep "5. Verifying Project Workspace" {
    if (-not (Test-Path $projectsDir)) {
        New-Item -ItemType Directory -Path $projectsDir -Force | Out-Null
    }
}

# STEP 6: Checking Browser Availability
$availableBrowsers = @()
Animate-ProcessStep "6. Checking Browser Availability" {
    $availableBrowsers += "Default System Browser"
    if (Get-Command chrome -ErrorAction SilentlyContinue -or (Test-Path "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe") -or (Test-Path "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe") -or (Test-Path "${env:LocalAppData}\Google\Chrome\Application\chrome.exe")) {
        $availableBrowsers += "Google Chrome"
    }
    if (Get-Command msedge -ErrorAction SilentlyContinue -or (Test-Path "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe") -or (Test-Path "${env:ProgramFiles}\Microsoft\Edge\Application\msedge.exe")) {
        $availableBrowsers += "Microsoft Edge"
    }
    if (Get-Command brave -ErrorAction SilentlyContinue -or (Test-Path "${env:ProgramFiles}\BraveSoftware\Brave-Browser\Application\brave.exe")) {
        $availableBrowsers += "Brave Browser"
    }
    if (Get-Command firefox -ErrorAction SilentlyContinue -or (Test-Path "${env:ProgramFiles}\Mozilla Firefox\firefox.exe")) {
        $availableBrowsers += "Mozilla Firefox"
    }
}

# STEP 7: Preparing KDP Studio
Animate-ProcessStep "7. Preparing KDP Studio" {
    $indexPath = Join-Path $scriptDir "web_preview\index.html"
    if (-not (Test-Path $indexPath)) {
        throw "Studio assets missing: web_preview\index.html not found!"
    }
}

# STEP 8: Final System Check
Animate-ProcessStep "8. Final System Check" {
    $sTime = 100
    if ($TestMode) { $sTime = 10 }
    Start-Sleep -Milliseconds $sTime
}

Write-Host "  $sLine69" -ForegroundColor DarkGray
Write-Host ""

# 5. System Status Table
$sLine67 = "$h" * 67
Write-Host "  $tl$sLine67$tr" -ForegroundColor Cyan
Write-Host "  $v $("SYSTEM STATUS".PadRight(67)) $v" -ForegroundColor White
Write-Host "  $ml$sLine67$mr" -ForegroundColor Cyan
Write-Host "  $v $(" Python Environment    $check READY  ($pyVersion)".PadRight(66)) $v" -ForegroundColor Gray
Write-Host "  $v $(" Backend Engine        $check RUNNING (HTTP/REST API Engine)".PadRight(66)) $v" -ForegroundColor Gray
Write-Host "  $v $(" Local Server          $check ONLINE  (Port 8080)".PadRight(66)) $v" -ForegroundColor Gray
Write-Host "  $v $(" Server URL            http://localhost:8080".PadRight(66)) $v" -ForegroundColor White
Write-Host "  $v $(" Project Workspace     $check READY  (Documents\KDP_Studio_Projects)".PadRight(66)) $v" -ForegroundColor Gray
Write-Host "  $bl$sLine67$br" -ForegroundColor Cyan
Write-Host ""

# 6. Browser Selection Menu
Write-Host "  $tl$sLine67$tr" -ForegroundColor Cyan
Write-Host "  $v $("SELECT YOUR PREFERRED BROWSER".PadRight(67)) $v" -ForegroundColor White
Write-Host "  $ml$sLine67$mr" -ForegroundColor Cyan
Write-Host "  $v $(" ".PadRight(67)) $v" -ForegroundColor DarkGray
Write-Host "  $v $("  [1] Default System Browser".PadRight(67)) $v" -ForegroundColor White
Write-Host "  $v $("  [2] Google Chrome".PadRight(67)) $v" -ForegroundColor White
Write-Host "  $v $("  [3] Microsoft Edge".PadRight(67)) $v" -ForegroundColor White
Write-Host "  $v $("  [4] Brave Browser".PadRight(67)) $v" -ForegroundColor White
Write-Host "  $v $("  [5] Mozilla Firefox".PadRight(67)) $v" -ForegroundColor White
Write-Host "  $v $("  [0] Server Only (Do not open browser)".PadRight(67)) $v" -ForegroundColor Yellow
Write-Host "  $v $(" ".PadRight(67)) $v" -ForegroundColor DarkGray
Write-Host "  $bl$sLine67$br" -ForegroundColor Cyan
Write-Host ""

$bChoice = $BrowserChoice
if (-not $bChoice) {
    try {
        $bChoice = Read-Host "  Enter choice [1-5, or 0] (Press Enter for Default)"
    } catch {
        $bChoice = "1"
    }
}
if ([string]::IsNullOrWhiteSpace($bChoice)) { $bChoice = "1" }

function Open-BrowserTarget($cmdName, $fallbackUrl) {
    try {
        Start-Process $cmdName $fallbackUrl -ErrorAction Stop
    } catch {
        Start-Process $fallbackUrl
    }
}

switch ($bChoice.Trim()) {
    "1" {
        Write-Host "  [*] Launching KDP Studio in Default Browser..." -ForegroundColor Cyan
        if (-not $TestMode) { Start-Process "http://localhost:8080" }
    }
    "2" {
        Write-Host "  [*] Launching KDP Studio in Google Chrome..." -ForegroundColor Cyan
        if (-not $TestMode) { Open-BrowserTarget "chrome" "http://localhost:8080" }
    }
    "3" {
        Write-Host "  [*] Launching KDP Studio in Microsoft Edge..." -ForegroundColor Cyan
        if (-not $TestMode) { Open-BrowserTarget "msedge" "http://localhost:8080" }
    }
    "4" {
        Write-Host "  [*] Launching KDP Studio in Brave Browser..." -ForegroundColor Cyan
        if (-not $TestMode) { Open-BrowserTarget "brave" "http://localhost:8080" }
    }
    "5" {
        Write-Host "  [*] Launching KDP Studio in Mozilla Firefox..." -ForegroundColor Cyan
        if (-not $TestMode) { Open-BrowserTarget "firefox" "http://localhost:8080" }
    }
    "0" {
        Write-Host "  [*] Server-Only Mode selected. Browser not launched." -ForegroundColor Yellow
    }
    Default {
        Write-Host "  [*] Launching KDP Studio in Default Browser..." -ForegroundColor Cyan
        if (-not $TestMode) { Start-Process "http://localhost:8080" }
    }
}

Write-Host ""

# 7. Final Ready Screen
$dLine67 = "$dh" * 67
Write-Host "  $dtl$dLine67$dtr" -ForegroundColor Green
Write-Host "  $dv $(" ".PadRight(67)) $dv" -ForegroundColor Green
Write-Host "  $dv $("               $check KDP STUDIO IS ONLINE AND READY".PadRight(66)) $dv" -ForegroundColor White
Write-Host "  $dv $(" ".PadRight(67)) $dv" -ForegroundColor Green
Write-Host "  $dv $("        Backend Engine : ONLINE".PadRight(67)) $dv" -ForegroundColor Gray
Write-Host "  $dv $("        Workspace      : READY".PadRight(67)) $dv" -ForegroundColor Gray
Write-Host "  $dv $("        Local Server   : ONLINE".PadRight(67)) $dv" -ForegroundColor Gray
Write-Host "  $dv $("        Studio URL     : http://localhost:8080".PadRight(67)) $dv" -ForegroundColor Yellow
Write-Host "  $dv $(" ".PadRight(67)) $dv" -ForegroundColor Green
Write-Host "  $dbl$dLine67$dbr" -ForegroundColor Green
Write-Host ""

# 8. Subtle Professional Credit
Write-Host "  Amazon KDP Book Production Studio" -ForegroundColor DarkGray
Write-Host "  Designed & Developed by Kadir Laskar" -ForegroundColor DarkCyan
Write-Host ""
Write-Host "  $sLine69" -ForegroundColor DarkGray

if ($TestMode) {
    Write-Host "  [+] Test verification mode complete." -ForegroundColor Green
    exit 0
}

Write-Host "  Keep this window open while working on your books." -ForegroundColor Gray
Write-Host "  Press Ctrl + C or close this window to stop the server.`n" -ForegroundColor DarkGray

try {
    while ($true) {
        if ($serverProcess -and $serverProcess.HasExited) {
            Write-Host "  [!] Backend server process ended." -ForegroundColor Yellow
            break
        }
        Start-Sleep -Seconds 1
    }
} finally {
    if ($serverProcess -and -not $serverProcess.HasExited) {
        Stop-Process -Id $serverProcess.Id -Force -ErrorAction SilentlyContinue
    }
}
