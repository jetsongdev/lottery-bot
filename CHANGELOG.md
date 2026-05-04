# Changelog

## [Unreleased]

## [1.1.0] - 2026-05-04

### Added
- Telegram 알림 지원 (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`)
- 멀티채널 동시 발송 — Discord, Slack, Telegram 중 복수 설정 시 모두 발송
- `_to_telegram_html()`: Discord 마크다운 → Telegram HTML 변환 (코드블록, 볼드, 이모지)
- `.env.sample`에 `TELEGRAM_CHAT_ID` 항목 추가
- GitHub Actions 워크플로우에 Telegram secrets 연동

### Changed
- 구매 스케줄 변경: 매주 월요일 → **수요일 09:00 KST** (`0 0 * * 3`)
- `requests.post()` 전체에 `timeout=10` 적용
- 알림 전송 실패 시 에러 로그 출력 (`raise_for_status` + `RequestException` 처리)
- `_dispatch()` 로그 개선: 채널 미설정 vs 전송 실패 구분
- 타입 힌트 개선: `str = None` → `Optional[str]`
- Webhook 로그 라벨 "Discord" → "Webhook" (Slack 포함 대응)

## [1.0.0] - 2025-01-01

### Added
- 동행복권 자동 로그인
- 로또645 자동 구매 (자동/수동 모드)
- 연금복권720 자동 구매
- 로또645 당첨 확인
- 연금복권720 당첨 확인
- Discord / Slack Webhook 알림
- GitHub Actions 스케줄 자동화 (구매: 수요일, 당첨확인: 토요일)
