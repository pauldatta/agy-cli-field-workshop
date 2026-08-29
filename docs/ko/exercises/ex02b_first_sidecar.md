# 실습 2B: 첫 번째 사이드카

> **소요 시간:** 20분 | **모듈:** 2 — 플러그인 생태계

---

## 목표

월요일부터 금요일까지 오전 9시에 실행되어 새로운 AGY 대화를 생성하고, 리포지토리 전체에서 어제의 git 커밋을 요약하도록 요청하는 예약된 **일일 스탠드업 사이드카**를 구축합니다.

---

## 배경

사이드카(Sidecar)는 AGY가 사용자를 위해 관리하는 지속적인 백그라운드 프로세스입니다. AGY가 시작될 때 자동으로 실행되고, 크래시 발생 시 다시 시작되며, 활성 대화와 독립적으로 실행됩니다. `schedule` 내장 기능은 cron 표현식과 해당 일정에 따라 실행할 명령을 받습니다.

---

## 파트 1: 사이드카 설정 생성 (5분)

사이드카 디렉터리와 설정 파일을 생성합니다:

```bash
mkdir -p ~/.gemini/config/sidecars/standup
```

`~/.gemini/config/sidecars/standup/sidecar.json`을 생성합니다:

```json
{
  "description": "Daily standup — summarises yesterday's git commits",
  "builtin": "schedule",
  "args": [
    "0 9 * * 1-5",
    "agentapi",
    "new-conversation",
    "Summarise all git commits from yesterday across my repos. Group by repo, list the most impactful changes first, and flag any commits that touch security-sensitive files."
  ]
}
```

**주요 결정 사항:**

- `builtin: "schedule"` — 원시 명령어 대신 AGY의 내장 크론(cron) 스케줄러를 사용합니다.
- `0 9 * * 1-5` — 월요일부터 금요일까지 09:00에 실행됩니다.
- `agentapi new-conversation` — 스탠드업 프롬프트를 사용하여 프로그래밍 방식으로 새로운 AGY 대화를 엽니다.

---

## 파트 2: 사이드카 활성화 (5분)

사이드카는 **기본적으로 비활성화되어 있습니다**. `~/.gemini/config/config.json`에서 활성화하세요:

```bash
# View current config (create if it doesn't exist)
cat ~/.gemini/config/config.json 2>/dev/null || echo '{}'
```

사이드카 항목을 포함하도록 `~/.gemini/config/config.json`을 편집하세요:

```json
{
  "sidecars": {
    "standup": {
      "enabled": true
    }
  }
}
```

> **참고:** `config.json`에 이미 내용이 있는 경우, 기존 JSON에 `sidecars` 블록을 병합하세요. 파일을 교체하지 마세요.

---

## 파트 3: 사이드카 확인 (5분)

AGY를 시작하고 사이드카가 검색되었는지 확인합니다:

```bash
agy
```

세션 내에서 다음과 같이 질문합니다:

```text
> What sidecars are currently configured? Is the standup sidecar active?
```

사이드카의 런타임 데이터 디렉터리를 확인합니다:

```bash
ls -la ~/.gemini/antigravity-cli/sidecar_data/standup/logs/
```

디렉터리가 존재하면 사이드카가 등록된 것입니다. 예약된 실행이 끝날 때마다 타임스탬프가 찍힌 stdout/stderr 출력과 함께 로그 파일이 여기에 나타납니다.

> **팁:** 사이드카는 평일 오전 9시 전에는 실행되지 않습니다. 즉시 테스트하려면 cron을 임시로 `* * * * *`(매분)로 변경하고 60초를 기다린 다음 로그를 확인하세요. **테스트 후에는 원래대로 되돌려 놓는 것을 잊지 마세요.**

---

## 파트 4: 런타임 레이아웃 검사 (5분)

전체 사이드카 데이터 구조를 검사합니다:

```bash
# The sidecar runtime directory layout
find ~/.gemini/antigravity-cli/sidecar_data/standup/ -type f 2>/dev/null
```

예상되는 구조:

```text
~/.gemini/antigravity-cli/sidecar_data/standup/
├── data/     ← persistent storage (ANTIGRAVITY_EXECUTABLE_DATA_DIR env var)
├── logs/     ← timestamped stdout/stderr logs
└── events/   ← JSON records of agentapi calls
```

---

## 추가 목표: 파일 감시자 사이드카

`schedule` 내장 기능 대신 `command: python3`을 사용하는 두 번째 사이드카를 추가합니다. 이 사이드카는 로컬 파일의 변경 사항을 감시하고 차이점(diff)을 감지하면 기존 대화로 메시지를 보냅니다.

`~/.gemini/config/sidecars/file-watcher/sidecar.json`을 생성합니다:

```json
{
  "description": "Watches a target file and alerts on changes",
  "command": "python3",
  "args": ["watch.py"],
  "restart_policy": "on-failure",
  "env": {
    "WATCH_FILE": "/path/to/your/important-file.yaml"
  }
}
```

`~/.gemini/config/sidecars/file-watcher/watch.py`를 생성합니다:

```python
import os
import time
import hashlib
import subprocess

WATCH_FILE = os.environ.get("WATCH_FILE", "")
POLL_INTERVAL = 5  # seconds

def file_hash(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def main():
    if not os.path.exists(WATCH_FILE):
        print(f"File not found: {WATCH_FILE}")
        return

    last_hash = file_hash(WATCH_FILE)
    print(f"Watching {WATCH_FILE} (initial hash: {last_hash[:12]}...)")

    while True:
        time.sleep(POLL_INTERVAL)
        current_hash = file_hash(WATCH_FILE)
        if current_hash != last_hash:
            print(f"Change detected! {last_hash[:12]} -> {current_hash[:12]}")
            subprocess.run([
                "agentapi", "new-conversation",
                f"The file {WATCH_FILE} was modified. Please review the changes."
            ])
            last_hash = current_hash

if __name__ == "__main__":
    main()
```

`~/.gemini/config/config.json`에서 이를 활성화합니다:

```json
{
  "sidecars": {
    "standup": {
      "enabled": true
    },
    "file-watcher": {
      "enabled": true
    }
  }
}
```

---

## 완료 기준

- [ ] `schedule` 내장 기능과 `0 9 * * 1-5` 크론(cron)이 포함된 `~/.gemini/config/sidecars/standup/sidecar.json` 파일이 존재합니다.
- [ ] `~/.gemini/config/config.json`에 `sidecars.standup.enabled: true`가 설정되어 있습니다.
- [ ] AGY가 사이드카를 인식합니다(세션 쿼리 또는 로그 디렉터리 존재 여부로 확인됨).
- [ ] `~/.gemini/antigravity-cli/sidecar_data/standup/`에 사이드카 런타임 디렉터리가 존재합니다.
- [ ] *(추가 목표)* `command: python3` 및 정상 작동하는 `watch.py`로 파일 감시자(File-watcher) 사이드카가 생성되었습니다.
