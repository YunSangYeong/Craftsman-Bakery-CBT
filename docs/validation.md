# 현재 작업 검증 기록

작업일: 2026-11-03. 작업 디렉터리: `/workspace/Craftsman-Bakery-CBT`.
Node 24.19.0, npm lockfile, Linux Chromium `/usr/bin/chromium`을 사용했다.

| 검사 | 최종 결과 |
| --- | --- |
| npm ci --no-audit --no-fund | 성공, lockfile 기반 110개 설치 |
| npm test -- --reporter=dot | 938개 통과, 종료 0 |
| npm run build | TypeScript 및 Vite 프로덕션 빌드 성공, 종료 0 |
| PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e | 28개 통과, 2개 명시적 건너뜀, 실패 0, 종료 0 |
| python3 scripts/generate_bank.py | 1,000개 재생성, 두 실행의 SHA-256 동일 |
| 기본 은행 품질 | 고유 ID/정규화 지문 1,000개, 자체 제작, 미확인 연도·회차 null |
| 독립 수치 검증 | 계산 920개 재계산·반올림·단위·정답 위치·동치 보기 검사 통과 |
| 표준 폴더 복사 | 최신 main 원본과 9개 파일 바이트 일치 |
| git diff --check | 통과 |

브라우저 테스트 30개 중 2개는 데스크톱 프로젝트의 모바일 CDP 터치 전용 검사이므로 건너뛰었다.
해당 두 검사는 모바일 프로젝트에서 실제 touchStart/move/end 입력으로 실행해 통과했다.
PC는 Desktop Chrome 설정, 모바일은 Pixel 7 에뮬레이션이다. 실물 스마트폰 검증은 미실시다.
390×480 및 740×360 메뉴에서 실제 휠/터치로 아래→백업/초기화 접근→위→대시보드 선택을 검사했다.
scrollTop을 코드로 대입하는 방법은 사용하지 않았다. 확대 글자와 높이 축소 후 접근도 통과했다.

시험 60문항 중 36정답의 합격 경계·답안 변경·새로고침·미응답·결과/해설·오답 필터/재학습,
절대 시각 60분 만료·타이머 콜백 이전 만료 클릭·중복 제출 방지,
랜덤 채점·오답·북마크·통계·이어하기, JSON/CSV 등록·검수·초기화,
저장 손상 원본 보존, 양쪽 모드의 실제 Space keydown/keyup와 본문 포커스를 검사했다.
화면별 가로 넘침·학습 기준 선택 UI 부재·상시 면책 배너 부재도 확인했다.
대시보드와 출처 화면의 PC/모바일 캡처를 실제로 열어 시각 확인했다. 캡처/테스트 결과물은 Git에서 제외했다.

초기 로컬 실패는 그대로 완료 결과로 세지 않았다.
확대 메뉴 검사는 휠 입력 처리 이전 위치 읽기 문제를 입력 결과 polling으로 수정한 뒤 통과했다.
화면별 검사는 모든 notice를 금지해 통계 집계 범위 안내까지 실패시키던 조건을 면책/검증 대기 배너로 좁혔다.
이 과정에서 기준 앱의 별도 시험 준비 화면에 남은 비공식 안내 박스를 제거했다. 실제 저장 오류 경고는 유지했다.
최종 전체 30개 검사를 다시 실행해 위 결과를 확인했다.

Vite는 단일 JS 청크 약 1.69 MB(압축 약 150 KB)에 크기 경고를 냈다. 기본 JSON을 포함한 크기이며 빌드 실패는 아니다.
공식 시험 기준 대조, 외부 전문가 문항 검수, 실물 기기, Safari/Firefox, 블로그 iframe, 다른 새 작업에서의 복원은 검증하지 않았다.

## 배포 사전 확인: 첫 차단에서 종료

1. 원격 main 읽기 성공: `5c46d678d94e32046cf05e21935fab16ddb49378`. 기존 작업과 다른 원격 변경이 없었다.
2. 기존 GitHub 환경 인증을 사용해 저장소 권한을 한 번 조회했다.
   `gh api repos/YunSangYeong/Craftsman-Bakery-CBT --jq '{default_branch,has_pages,permissions}'`
3. 실제 오류: `Get "https://api.github.com/repos/YunSangYeong/Craftsman-Bakery-CBT": Forbidden` (종료 1).

배포 사전 필수 API 접근에서 차단됐으므로 그 즉시 배포 진행을 중단했다.
Pages Source·관리 권한·환경 승인 필요 여부는 확인하지 못했다. 없는 Pages 설정이나 토큰 문제로 단정하지 않는다.
API 재조회, main push, 수동 workflow 실행, workflow 재실행, 대체 플랫폼 배포는 하지 않았다.
신규 CI·Pages 파이프라인은 시작하지 않았다. 현재 배포 성공 및 공개 화면은 미확인이다.
기존 원격 main에는 README만 있었으며 이번 앱은 main으로 게시하지 않았다.

코드 보존 대상은 자동 배포를 유발하지 않는 `codex/bakery-cbt-standard-v1-4-20261103` 브랜치다.
원격 반영의 최종 커밋과 성공 여부는 작업 완료 보고에 기록한다. PR 생성·수동 실행은 하지 않는다.
예상 Pages 주소: https://YunSangYeong.github.io/Craftsman-Bakery-CBT/ (게시 확인 아님).

사용자의 지금 최소 동작: 이 클라우드 환경 설정의 인터넷 허용 도메인에 `api.github.com`을 추가한다.
이는 확인된 거부에 대한 첫 설정 점검이며 권한 문제가 함께 없는지까지 증명하지 않는다.
사용자가 이후 직접 배포를 마무리한다. 설정 변경을 추정하여 에이전트가 자동 재시도하지 않는다.
