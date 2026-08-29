# 환경 설정

> 모듈을 시작하기 전에 이 작업을 완료하세요. 약 15분이 소요됩니다.

---

## 시스템 요구 사항

| 구성 요소 | 최소 사양 | 참고 |
| :-- | :-- | :-- |
| **agy** | 최신 버전 | 아래 설치 지침 참조 |
| **Git** | v2.30+ | 실습 저장소용 |
| **터미널** | 제한 없음 | iTerm2, macOS 터미널 또는 VS Code 통합 터미널 |
| **jq** | 선택 사항 | `--print` JSON 출력 파싱에 유용함 |

---

## 1단계: agy 설치

> 📖 전체 지침: [시작하기 문서](https://www.antigravity.google/docs/cli-getting-started)

### macOS / Linux

```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

### Windows

```powershell
# PowerShell
irm https://antigravity.google/cli/install.ps1 | iex

# Or via WSL (recommended)
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

설치 후, 바이너리가 사용 가능한지 확인합니다:

```bash
# Verify the binary is in your PATH
which agy

# Confirm the version
agy --version
```

---

## 2단계: 인증

agy는 **브라우저 기반 Google 로그인**을 사용합니다. 첫 실행 시 다음과 같이 작동합니다:

- **로컬 머신:** 로그인을 위해 기본 브라우저를 자동으로 엽니다.
- **SSH / 원격 세션:** 아무 브라우저에나 붙여넣을 수 있는 URL을 출력하며, 이후 인증 코드를 터미널에 다시 붙여넣습니다.

```bash
# Start agy — auth will trigger automatically on first run
agy
```

로그아웃하려면:

```text
# Run this inside an agy interactive session (not in your terminal):
/logout
```

> 📖 GCP 프로젝트를 통한 엔터프라이즈 인증에 대해서는 [엔터프라이즈 문서](https://www.antigravity.google/docs/enterprise)를 참조하세요.

인증이 구성되면, 간단한 스모크 테스트를 실행하세요:

```bash
agy --print "Say 'Workshop ready!' in exactly two words." --print-timeout 30s
```

예상 출력: `Workshop ready!`

---

## 3단계: 프로젝트 작업 공간 초기화

agy는 현재 디렉토리에서 상위로 이동하며 `.agents/` 폴더를 찾아 프로젝트 설정을 자동으로 검색합니다. 워크샵을 위해 하나를 생성하세요:

```bash
# Clone the workshop exercises repo
git clone https://github.com/pauldatta/agy-cli-field-workshop.git
cd agy-cli-field-workshop

# agy will create .agents/ on first run
agy --print "List the files in the current directory."
```

프로젝트 설정 파일(settings.json, mcp.json 등)이 포함된 `.agents/` 폴더가 생성된 것을 볼 수 있습니다.

!!! info ".gemini/ 호환성"
    agy는 `.gemini/` 디렉토리도 읽습니다. 이는 이미 Gemini CLI 프로젝트 설정이 있는 경우에 유용합니다. 두 설정 위치 모두 적용됩니다.

---

## 4단계: 모든 항목 확인

```bash
# Check agy is accessible
agy --help

# List installed plugins (output is JSON)
agy plugin list

# Pretty-print the plugin list (works once plugins are installed in Module 2)
# agy plugin list | python3 -m json.tool

# Quick print-mode smoke test
agy --print "What is 2 + 2?" --print-timeout 30s
```

워크숍 시작 전 체크리스트:

- [ ] `agy --help` 실행 시 플래그와 하위 명령어가 표시됨
- [ ] `agy plugin list` 가 정상적으로 실행됨
- [ ] `agy --print "..."` 실행 시 응답을 반환함

---

## 문제 해결

| 문제 | 해결 방법 |
| :-- | :-- |
| `agy: command not found` | 바이너리가 PATH에 있는지 확인하세요. `echo $PATH`를 실행하여 설치 디렉터리가 포함되어 있는지 확인합니다. 필요한 경우 설치 스크립트를 다시 실행하세요. |
| 인증 오류 / 브라우저가 열리지 않음 | SSH 세션의 경우 출력된 URL을 수동으로 복사하세요. 로컬의 경우 기본 브라우저 설정을 확인하세요. `/logout`을 실행하고 다시 시도하세요. |
| `agy plugin list`가 `No imported plugins.`를 반환함 | 새로 설치한 경우 정상적인 동작입니다(JSON 아님). 모듈 2에서 플러그인을 추가하게 됩니다. |
| 첫 응답이 느림 | agy가 작업 공간을 인덱싱하므로 첫 실행은 더 느릴 수 있습니다. |
| 설정이 로드되지 않음 | `~/.gemini/antigravity-cli/settings.json`(사용자 설정) 및 `.agents/`(프로젝트 설정)를 확인하세요. |

---

## 다음 단계

→ **[모듈 1: SDLC 생산성 향상](sdlc-productivity.md)**으로 시작하세요
