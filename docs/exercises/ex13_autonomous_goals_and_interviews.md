# Exercise 13: Requirements Interviews & Autonomous Loops

> **Duration:** 25 min (Fast: 15 min · Average: 25 min · Thorough: 35 min) | **Module:** 1 — SDLC Productivity / Advanced Workflows

---

## Objective

Master two of Antigravity's most powerful interactive workflows:
1. Use **`/grill-me`** to conduct an interactive requirements interview where the agent probes edge cases, challenges assumptions, and produces a concrete Architecture Decision Record (ADR).
2. Switch to **`/goal`** mode to execute an autonomous build-test-fix loop that iterates until all test suites pass without premature termination.

---

## Setup

Use any existing project or create a quick test workspace:

```bash
mkdir -p ~/agy-goal-lab/src ~/agy-goal-lab/test
cd ~/agy-goal-lab
git init
```

Create a sample flawed token bucket rate limiter in `src/limiter.py`:

```python
import time


class RateLimiter:
    """Token bucket rate limiter with intentional concurrency and reset bugs."""

    def __init__(self, capacity: int, refill_rate_per_sec: float):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate_per_sec
        self.last_refill = time.time()

    def allow_request(self, tokens: int = 1) -> bool:
        now = time.time()
        elapsed = now - self.last_refill
        # BUG: Doesn't clamp tokens to capacity properly
        self.tokens += elapsed * self.refill_rate
        self.last_refill = now

        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
```

And a test suite in `test/test_limiter.py`:

```python
import time
from src.limiter import RateLimiter


def test_capacity_burst():
    limiter = RateLimiter(capacity=5, refill_rate_per_sec=1.0)
    for _ in range(5):
        assert limiter.allow_request() is True
    # 6th request should fail
    assert limiter.allow_request() is False


def test_refill_over_time():
    limiter = RateLimiter(capacity=2, refill_rate_per_sec=2.0)
    assert limiter.allow_request() is True
    assert limiter.allow_request() is True
    assert limiter.allow_request() is False
    time.sleep(1.1)
    # Should have refilled to 2 tokens, not more
    assert limiter.allow_request() is True
    assert limiter.allow_request() is True
    assert limiter.allow_request() is False
```

```bash
git add -A && git commit -m "initial rate limiter"
```

---

## Part 1: Requirements Interview with `/grill-me` (10 min)

Launch `agy`:

```bash
agy
```

Start the requirements interview:

```text
/grill-me I want to add distributed Redis-backed rate limiting with sliding window support to this rate limiter.
```

Observe how `agy` responds:
* It will not blindly write code.
* Instead, it enters an interactive interview modal, asking multiple-choice and clarifying questions about:
  1. Concurrency model (async vs thread-safe locks vs Redis Lua scripts).
  2. Failure mode policy (fail-open vs fail-closed if Redis is unreachable).
  3. Window granularity and memory footprint requirements.

Answer the questions. Once you finish the interview, prompt:

```text
> Synthesize our interview into a formal Architecture Decision Record (ADR) and write it to docs/adr-001-rate-limiter.md.
```

Inspect the generated ADR artifact:

```text
> Review the ADR artifact. Does it capture all the constraints we agreed on?
```

---

## Part 2: Autonomous Execution with `/goal` (10 min)

Now execute the plan autonomously without babysitting compiler errors:

```text
/goal Fix the bugs in src/limiter.py and make all tests in test/test_limiter.py pass. Run `python3 -m pytest test/` (or `python3 -m unittest discover test/`) to verify. Do not stop until all tests pass with 0 failures.
```

Observe the autonomous loop:
1. `agy` reads the source and test files.
2. It identifies the calculation and clamping errors.
3. It applies a fix to `src/limiter.py`.
4. It executes the test suite in the terminal sandbox.
5. If tests fail, it reads the traceback, refines its fix, and re-runs the tests automatically until complete.

Expand and inspect the model's reasoning trajectory during the loop by pressing **`Ctrl+O`**.

---

## Part 3: Verifying the Goal Completion (5 min)

Exit the interactive session (`/exit`) and verify the result from the terminal:

```bash
python3 -m unittest discover -s test -p "test_*.py"
```

Check the git diff to inspect the autonomous modifications:

```bash
git diff src/limiter.py
```

---

## ⚠️ Field Gotchas & Failure Modes

!!! warning "Common Workshop Gotchas"
    1. **Vague `/goal` Criteria:** `/goal` works best when paired with an objective verification command (e.g. `pytest`, `mvn test`, `npm test`, or `make lint`). If the goal is subjective (e.g. "make the code look nicer"), the loop may terminate early.
    2. **Halting Infinite Loops:** If a test failure is impossible to resolve without architectural changes, you can stop the `/goal` loop at any time with **Ctrl+C**.
    3. **Interview Synthesis:** In `/grill-me` mode, always ask `agy` to output the final spec or ADR to a markdown artifact so downstream sessions or subagents can reference it.

---

## Completion Criteria

- [ ] Ran `/grill-me` to conduct an interactive requirements interview
- [ ] Produced an ADR markdown artifact capturing architectural decisions
- [ ] Executed an autonomous loop using `/goal`
- [ ] Toggled trajectory inspection with `Ctrl+O`
- [ ] Verified that all unit tests pass cleanly after autonomous remediation
