# gapchae (내 영양제 성분 분석기)

2025 한국인 영양소 섭취기준(KDRI) 대비 중복, 과다, 부족 섭취 여부를 진단하고 안 챙기는 주요 영양소(빈틈)를 찾아주는 모바일 최적화 웹 애플리케이션입니다.

---

## 🌿 주요 기능

1. **개인화 기준 설정**: 성별(남성/여성) 및 연령대(19~29세, 30~49세, 50~64세, 65~74세, 75세 이상)를 설정하여 개개인에 최적화된 영양소 권장량(RNI) 및 상한섭취량(UL)을 적용합니다.
2. **영양제 등록 및 자동완성 검색**: 
   - 식약처 건강기능식품 영양성분 공공 API 데이터를 기반으로 정제한 제품 DB를 통해 편리하게 검색 및 영양 성분을 자동완성 등록할 수 있습니다.
   - 제품 통 가격, 총 개수, 하루 복용 횟수를 입력하여 1일 복용 비용 및 가성비를 함께 파악합니다.
3. **안 챙기는 성분 찾기 (GAP)**: 복용 중인 영양제 성분을 분석하여 현재 챙기지 못하고 있는 필수 영양소(빈틈)를 단계(Tier)별로 분류하여 보여주고 추천 정보를 제공합니다.
4. **섭취량 과다·부족 판정**: 하루 복용 성분 총량을 2025 한국인 기준과 비교하여 부족, 적정, 주의, 과다 상태를 판정하고 시각화 바(Bar)로 가시화합니다.
5. **보관 및 공유 기능**: 판정 결과를 텍스트 형식으로 클립보드에 복사하거나 깔끔한 카드 이미지(`html2canvas`)로 다운로드할 수 있습니다.
6. **영양제 섭취 가이드**: 중복 섭취 가이드 및 흡수 방해 조합 가이드를 포함합니다.

---

## 🛠️ 기술 스택
- **Core**: HTML5, Vanilla JavaScript, jQuery-style Selector
- **Styling**: Vanilla CSS3 (Curated Green/Mint theme, 반응형 모바일 우선 디자인)
- **Library**: `html2canvas.min.js` (판정 결과 이미지 저장용)
- **Data Source**: 보건복지부·한국영양학회 2025 한국인 영양소 섭취기준 (2025.12 요약표), 식약처 공공 API

---

## 📁 주요 파일 및 구조

### 서비스 프론트엔드
* **[index.html](file:///Users/tony/gapchae/index.html)**: 메인 페이지. 영양소 공식 기준 DB, 섭취량 계산 공식, UI 인터랙션 등이 통합된 메인 코드입니다.
* **[combo.html](file:///Users/tony/gapchae/combo.html)**: 영양소 조합 가이드 (상호 흡수 방해 vs 시너지 조합).
* **[multivitamin.html](file:///Users/tony/gapchae/multivitamin.html)**: 종합비타민과 개별 영양제 중복 섭취 가이드.
* **[gap.html](file:///Users/tony/gapchae/gap.html)**: 영양제 성분 중심의 부족 빈틈 점검 가이드.

### 데이터 파이프라인 (Python / Node.js)
* **[parse-excel.py](file:///Users/tony/gapchae/parse-excel.py)**: 식품안전나라에서 다운로드한 `건강기능식품DB.xlsx` 파일을 직접 파싱하여 비타민 B12, 아연, 엽산, 마그네슘 등 총 19종의 미량 영양소 성분이 모두 매핑된 경량 검색 DB(`nutrition-search.json`)를 직접 빌드합니다.
* **[fetch-data.js](file:///Users/tony/gapchae/fetch-data.js)**: 식약처 공공 API에서 제품 원본 데이터를 수집해 `nutrition-db.json`을 임시 생성하는 파일입니다. (24개 필수 성분 제한이 있어 미량 영양소 누락 이슈가 있습니다.)
* **[trim-data.js](file:///Users/tony/gapchae/trim-data.js)**: 원본 데이터에서 영양제 이름 및 핵심 영양소 성분량만 정제하여 검색용 경량 데이터베이스를 빌드하는 스크립트입니다.
* **[nutrition-search.json](file:///Users/tony/gapchae/nutrition-search.json)**: 자동완성 검색에 연동된 정제된 제품 DB 파일입니다.

---

## 🤖 개발 및 협업 환경 (MultiAgent Orchestration)

이 저장소는 Antigravity(Gemini 3.1 Pro High)를 오케스트레이터로 두고 Claude·Codex를 워커로 호출하는 **파일 기반 멀티에이전트 시스템**을 개발 협업 환경으로 구축하고 있습니다.

### 핵심 아이디어
- **Orchestrator = Antigravity 세션** (이 폴더 안에서 실행 시 `AGENTS.md` 적용)
- **Workers** = 별도 worker/model 호출. 모두 승인 게이트 통과 필요.
  - `claude-main` — 메인 코딩·설계
  - `codex-main` — 보조 구현·분석·테스트
  - `codex-critic` — 산출물 리뷰·비평(교차 벤더)
- **Memory = filesystem.** 런타임 상태 없음. 모든 결정·승인·검증이 파일로 남습니다.

### 사용 시작
이 폴더 안에서 Antigravity CLI를 실행하거나 Antigravity IDE로 열어 개발을 시작합니다.
```bash
cd /Users/tony/gapchae
agy            # 또는 Antigravity IDE에서 이 폴더 열기
```

자연어로 새로운 에이전트 작업을 지시합니다:
> "새 작업 만들어줘. 목표는 ○○이고 codex-critic 검수가 필요할 것 같아."

자세한 에이전트 오퍼레이션 규칙은 **[AGENTS.md](file:///Users/tony/gapchae/AGENTS.md)** 및 **[_shared/](file:///Users/tony/gapchae/_shared/)** 내부 파일들을 참고하시기 바랍니다.
