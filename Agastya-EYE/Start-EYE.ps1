param(
    [switch]$ForDevice
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path

if ($ForDevice) {
    $bindHost = '0.0.0.0'
    $ports = 8773..8788
    if (-not $env:AGASTYA_DEVICE_TOKEN) {
        $tokenPath = Join-Path $env:LOCALAPPDATA 'Agastya\EYE\device-token.txt'
        if (Test-Path -LiteralPath $tokenPath) {
            $env:AGASTYA_DEVICE_TOKEN = (Get-Content -LiteralPath $tokenPath -Raw).Trim()
        }
        if (-not $env:AGASTYA_DEVICE_TOKEN) {
            $tokenDirectory = Split-Path -Parent $tokenPath
            New-Item -ItemType Directory -Path $tokenDirectory -Force | Out-Null
            $env:AGASTYA_DEVICE_TOKEN = [guid]::NewGuid().ToString('N') + [guid]::NewGuid().ToString('N')
            [System.IO.File]::WriteAllText($tokenPath, $env:AGASTYA_DEVICE_TOKEN, [System.Text.UTF8Encoding]::new($false))
        }
        if ($env:AGASTYA_DEVICE_TOKEN.Length -lt 24) {
            throw 'AGASTYA_DEVICE_TOKEN must be at least 24 characters.'
        }
    }
} else {
    $bindHost = '127.0.0.1'
    $ports = @(8765) + (8774..8788)
}

$pythonCandidates = [System.Collections.Generic.List[object]]::new()
if ($env:AGASTYA_EYE_PYTHON) {
    if (-not (Test-Path -LiteralPath $env:AGASTYA_EYE_PYTHON -PathType Leaf)) {
        throw "AGASTYA_EYE_PYTHON does not point to an interpreter file: $env:AGASTYA_EYE_PYTHON"
    }
    $pythonCandidates.Add([pscustomobject]@{ Path = $env:AGASTYA_EYE_PYTHON; Prefix = @() })
}

$venvPython = Join-Path $root '.venv\Scripts\python.exe'
if (Test-Path -LiteralPath $venvPython -PathType Leaf) {
    $pythonCandidates.Add([pscustomobject]@{ Path = $venvPython; Prefix = @() })
}

$userEnvsDirectory = Join-Path $env:USERPROFILE 'Envs'
if (Test-Path -LiteralPath $userEnvsDirectory -PathType Container) {
    Get-ChildItem -LiteralPath $userEnvsDirectory -Directory -ErrorAction SilentlyContinue |
        Sort-Object -Property Name |
        ForEach-Object {
            $environmentPython = Join-Path $_.FullName 'Scripts\python.exe'
            if (Test-Path -LiteralPath $environmentPython -PathType Leaf) {
                $pythonCandidates.Add([pscustomobject]@{ Path = $environmentPython; Prefix = @() })
            }
        }
}

$launcher = Get-Command py.exe -ErrorAction SilentlyContinue
if ($launcher) {
    $pythonCandidates.Add([pscustomobject]@{ Path = $launcher.Source; Prefix = @('-3.14') })
    $pythonCandidates.Add([pscustomobject]@{ Path = $launcher.Source; Prefix = @('-3') })
}
$pythonCommand = Get-Command python.exe -ErrorAction SilentlyContinue
if ($pythonCommand) {
    $pythonCandidates.Add([pscustomobject]@{ Path = $pythonCommand.Source; Prefix = @() })
}

$pythonProbe = 'import sys,torch,torchvision; import numpy,PIL; assert sys.version_info >= (3,11), "Python 3.11 or newer is required"; available=torch.cuda.is_available(); gpu=torch.cuda.get_device_name(0) if available else ""; print("python="+sys.executable+"; torch="+torch.__version__+"; torchvision="+torchvision.__version__+"; torch_cuda="+str(torch.version.cuda)+"; cuda_available="+str(available)+("; gpu="+gpu if gpu else ""))'
$selectionErrors = @()
$python = $null
$prefix = @()
foreach ($candidate in $pythonCandidates) {
    if (-not (Test-Path -LiteralPath $candidate.Path -PathType Leaf)) {
        $selectionErrors += "Missing interpreter: $($candidate.Path)"
        continue
    }
    $pythonArguments = @($candidate.Prefix) + @('-c', $pythonProbe)
    try {
        $probeOutput = & $candidate.Path @pythonArguments 2>&1
        $probeExit = $LASTEXITCODE
    } catch {
        $probeOutput = $_.Exception.Message
        $probeExit = 1
    }
    if ($probeExit -eq 0) {
        $python = $candidate.Path
        $prefix = @($candidate.Prefix)
        Write-Host "Selected EYE interpreter: $python"
        if ($probeOutput) {
            Write-Host "EYE runtime: $($probeOutput -join ' ')"
        }
        break
    }
    $selectionErrors += "$($candidate.Path) $($candidate.Prefix -join ' '): $($probeOutput -join ' ')"
}
if (-not $python) {
    $details = if ($selectionErrors.Count) { $selectionErrors -join [Environment]::NewLine } else { 'No Python launcher or interpreter was found.' }
    throw "No Python environment can import EYE requirements (Pillow, NumPy, PyTorch and torchvision). Use the existing EYE venv, set AGASTYA_EYE_PYTHON to a compatible interpreter, or install compatible dependencies in an existing Python 3.11+ environment.`n$details"
}

function Test-EyeApi([int]$CandidatePort) {
    try {
        $status = Invoke-RestMethod -Uri "http://127.0.0.1:$CandidatePort/api/ping" -TimeoutSec 2
        return ($status.app -eq 'Agastya-EYE' -and $status.status -eq 'ready')
    } catch {
        return $false
    }
}

function Test-PortAvailable([int]$CandidatePort) {
    $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Any, $CandidatePort)
    try {
        $listener.Start()
        return $true
    } catch {
        return $false
    } finally {
        $listener.Stop()
    }
}

$port = $null
$alreadyRunning = $false
foreach ($candidate in $ports) {
    if (-not $ForDevice -and (Test-EyeApi $candidate)) {
        $port = $candidate
        $alreadyRunning = $true
        break
    }
    if (Test-PortAvailable $candidate) {
        $port = $candidate
        break
    }
}
if ($null -eq $port) {
    throw 'No available EYE port was found in the configured range.'
}

$url = "http://127.0.0.1:$port"
if (-not $alreadyRunning) {
    $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $stdout = Join-Path $env:TEMP "agastya-eye-$stamp.out.log"
    $stderr = Join-Path $env:TEMP "agastya-eye-$stamp.err.log"
    $arguments = $prefix + @('app.py', '--host', $bindHost, '--port', [string]$port)
    $server = Start-Process -FilePath $python -ArgumentList $arguments -WorkingDirectory $root `
        -WindowStyle Hidden -RedirectStandardOutput $stdout -RedirectStandardError $stderr -PassThru

    $ready = $false
    for ($attempt = 0; $attempt -lt 45; $attempt++) {
        Start-Sleep -Seconds 1
        if ($server.HasExited) {
            throw "EYE stopped during startup. Check logs: $stderr and $stdout"
        }
        if (Test-EyeApi $port) {
            $ready = $true
            break
        }
    }
    if (-not $ready) {
        throw "EYE did not become ready. Check logs: $stderr and $stdout"
    }
}

Start-Process $url
Write-Host "Agastya EYE is ready at $url"
if ($ForDevice) {
    Write-Host "Device upload API: http://<this-PC-private-IP>:$port"
    Write-Host "Copy this token into firmware secrets.h: $env:AGASTYA_DEVICE_TOKEN"
    Write-Host 'Keep this service on a trusted private LAN. Do not port-forward it.'
}
