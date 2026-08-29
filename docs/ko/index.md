---
title: ""
hide:
  - navigation
  - toc
---

<div class="hero-banner" markdown>
  <img src="assets/banner.png" alt="Antigravity CLI 필드 워크숍">
</div>

<div class="workshop-meta-bar" markdown>
<span class="workshop-meta-item">:material-update: **최근 업데이트:** 2026년 8월</span>
<span class="workshop-meta-item">:material-check-decagram: **Antigravity 2.11 · CLI 1.1.22 · SDK 0.1.15**</span>
<span class="workshop-meta-item">:material-translate: **English · 한국어 · Bahasa Indonesia · 简体中文**</span>
</div>

---

## 워크숍 모듈

<div class="grid cards" markdown>

- :material-rocket-launch:{ .lg .middle } **모듈 1 — SDLC 생산성 향상**

    ---

    첫 번째 Antigravity CLI 세션입니다. 코드 설명, 리팩토링, 테스트, 리뷰와 더불어 자율 목표(`/goal`), 요구사항 인터뷰(`/grill-me`), 시각적 diff 및 플러그인을 알아봅니다.

    **75분** · 연습 문제: ex01–ex03, ex13, ex14

    [:octicons-arrow-right-24: 모듈 1 시작하기](sdlc-productivity.md)

- :material-wrench:{ .lg .middle } **모듈 2 — 레거시 현대화**

    ---

    가장 핵심적인 모듈입니다. 엄격한 모드, 에이전트 자체 온보딩 및 서브에이전트 계획을 사용하여 실제 레거시 코드베이스(.NET 또는 Java)를 마이그레이션합니다.

    **90분** · 연습 문제: ex07–ex09

    [:octicons-arrow-right-24: 모듈 2 시작하기](legacy-modernization.md)

- :material-code-braces:{ .lg .middle } **모듈 3 — AGY 에이전트 구축**

    ---

    Antigravity SDK로 프로덕션 에이전트를 구축합니다. 도구, 세션 상태, 다중 에이전트 오케스트레이션 및 Cloud Run 배포를 다룹니다.

    **90분** · 연습 문제: ex10, ex11

    [:octicons-arrow-right-24: 모듈 3 시작하기](agy-sdk.md)

- :material-sitemap:{ .lg .middle } **모듈 4 — 다중 에이전트 및 고급 기능**

    ---

    격리된 서브에이전트를 생성하고, `/btw`로 실행 중 작업을 제어하며, 반복 작업을 예약하고, DevTools MCP로 브라우저 테스트를 자동화합니다.

    **60분** · 연습 문제: ex04–ex06, ex15

    [:octicons-arrow-right-24: 모듈 4 시작하기](multi-agent-advanced.md)

- :material-rocket-launch-outline:{ .lg .middle } **모듈 5 — agents-cli를 사용한 ADK 에이전트**

    ---

    agents-cli를 사용하여 프로덕션 ADK 에이전트를 스캐폴딩, 빌드, 평가 및 배포합니다. 프로토타입부터 Cloud Run까지 전체 7단계 수명 주기를 다룹니다.

    **75분** · 연습 문제: ex12

    [:octicons-arrow-right-24: 모듈 5 시작하기](../agents-cli.md)

</div>

---

## 워크숍 일정

| 시간 | 내용 | 소요 시간 |
| :-- | :-- | :-- |
| `0:00` | 설정 + 첫 실행 | 20분 |
| `0:20` | **모듈 1:** SDLC 생산성 향상 + 플러그인 | 75분 |
| `1:35` | :coffee: 휴식 | 10분 |
| `1:45` | **모듈 2:** 레거시 코드베이스 현대화 | 90분 |
| `3:15` | :coffee: 휴식 | 10분 |
| `3:25` | **모듈 3:** SDK를 사용한 AGY 에이전트 구축 | 90분 |
| `4:55` | **모듈 4:** 멀티 에이전트 및 고급 | 60분 |
| `5:55` | :coffee: 휴식 | 10분 |
| `6:05` | **모듈 5:** agents-cli를 사용한 ADK 에이전트 | 75분 |
| `7:20` | 마무리 및 Q&A | 15분 |

> **종일 과정:** 모듈 1–4 (약 5.5시간). **연장 과정:** 전체 5개 모듈 (7시간). **반일 과정:** 모듈 1 + 2 (2.5시간). **단기 과정:** 모듈 1 + 모듈 2 핵심 내용 (1.5시간).

---

## 시작하기 전에

!!! warning "사전 작업 필수"
    워크숍 전에 [환경 설정](setup.md)을 완료하세요. Antigravity CLI가 설치되고 인증되어 있어야 합니다.

!!! info "공식 문서"
    전체 참조는 [antigravity.google/docs](https://www.antigravity.google/docs/cli-overview)에서 확인할 수 있습니다.

!!! info "사전 요구 사항"
    터미널, Git 및 기본 코딩 워크플로에 익숙해야 합니다. 이전 AI 코딩 어시스턴트 경험은 필요하지 않습니다.
