# Jupyter 커널 자동 설정 스크립트 (PowerShell)
# 현재 프로젝트의 가상 환경을 동기화하고 Jupyter 커널을 등록합니다.

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "🚀 Jupyter 커널 자동 설정 시작" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# pyproject.toml에서 프로젝트 이름 읽기
$pyprojectPath = "pyproject.toml"
if (-not (Test-Path $pyprojectPath)) {
    Write-Host "❌ pyproject.toml을 찾을 수 없습니다." -ForegroundColor Red
    exit 1
}

$pyprojectContent = Get-Content $pyprojectPath -Raw
if ($pyprojectContent -match 'name = "([^"]+)"') {
    $projectName = $matches[1]
} else {
    Write-Host "❌ 프로젝트 이름을 찾을 수 없습니다." -ForegroundColor Red
    exit 1
}

Write-Host "📦 프로젝트 이름: $projectName" -ForegroundColor Green

# 1. uv sync 실행
Write-Host "🔄 가상 환경 동기화..." -ForegroundColor Yellow
try {
    uv sync --group dev
    if ($LASTEXITCODE -ne 0) {
        throw "uv sync failed"
    }
    Write-Host "✅ 가상 환경 동기화 완료" -ForegroundColor Green
} catch {
    Write-Host "❌ 가상 환경 동기화 실패: $_" -ForegroundColor Red
    exit 1
}

# 2. Jupyter 커널 등록
$kernelName = $projectName -replace "-", "_"
$kernelDisplayName = "Python ($projectName)"

Write-Host "🔄 Jupyter 커널 등록..." -ForegroundColor Yellow
try {
    $kernelCmd = "uv run python -m ipykernel install --user --name $kernelName --display-name `"$kernelDisplayName`""
    Invoke-Expression $kernelCmd
    if ($LASTEXITCODE -ne 0) {
        throw "ipykernel install failed"
    }
    Write-Host "✅ Jupyter 커널 등록 완료" -ForegroundColor Green
} catch {
    Write-Host "❌ Jupyter 커널 등록 실패: $_" -ForegroundColor Red
    exit 1
}

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "✅ 모든 작업이 완료되었습니다!" -ForegroundColor Green
Write-Host "📝 노트북에서 '$kernelDisplayName' 커널을 선택하세요." -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Cyan
