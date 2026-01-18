#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jupyter 커널 자동 설정 스크립트
현재 프로젝트의 가상 환경을 동기화하고 Jupyter 커널을 등록합니다.
"""
import subprocess
import sys
import tomllib
from pathlib import Path
import io

# Windows에서 UTF-8 출력을 위한 인코딩 설정
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def read_project_name():
    """pyproject.toml에서 프로젝트 이름을 읽어옵니다."""
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        print("❌ pyproject.toml을 찾을 수 없습니다.")
        sys.exit(1)
    
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)
        return data.get("project", {}).get("name", "unknown")


def run_command(cmd, description):
    """명령어를 실행하고 결과를 출력합니다."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ {description} 완료")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 실패: {e.stderr}")
        return False


def main():
    """메인 함수"""
    print("=" * 50)
    print("🚀 Jupyter 커널 자동 설정 시작")
    print("=" * 50)
    
    # 프로젝트 이름 가져오기
    project_name = read_project_name()
    print(f"📦 프로젝트 이름: {project_name}")
    
    # 1. uv sync 실행
    if not run_command("uv sync --group dev", "가상 환경 동기화"):
        sys.exit(1)
    
    # 2. Jupyter 커널 등록
    kernel_name = project_name.replace("-", "_")
    kernel_display_name = f"Python ({project_name})"
    
    kernel_cmd = (
        f'uv run python -m ipykernel install --user '
        f'--name {kernel_name} '
        f'--display-name "{kernel_display_name}"'
    )
    
    if not run_command(kernel_cmd, "Jupyter 커널 등록"):
        sys.exit(1)
    
    print("=" * 50)
    print("✅ 모든 작업이 완료되었습니다!")
    print(f"📝 노트북에서 '{kernel_display_name}' 커널을 선택하세요.")
    print("=" * 50)


if __name__ == "__main__":
    main()
