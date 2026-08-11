$ErrorActionPreference = 'Stop'

Write-Host 'Losing-the-Loop / Qwen3-4B Windows runner'

if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    throw 'Ollama was not found in PATH. Install Ollama for Windows and reopen PowerShell.'
}

$models = ollama list
if ($models -notmatch 'qwen3:4b') {
    Write-Host 'Downloading qwen3:4b...'
    ollama pull qwen3:4b
}

$env:LLM_BASE_URL = 'http://localhost:11434/v1'
$env:LLM_MODEL = 'qwen3:4b'
$env:LLM_API_KEY = 'ollama'

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw 'Python launcher (py) was not found. Install Python 3.11+ and reopen PowerShell.'
}

py -m pip install --quiet openai
Write-Host 'Running Qwen3-4B benchmark...'
py benchmarks\run_large_qwen.py

if ($LASTEXITCODE -ne 0) {
    throw "Benchmark exited with code $LASTEXITCODE"
}

Write-Host 'Benchmark completed.'
