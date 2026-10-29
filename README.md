EventTwin — AI 기반 행사 설계 플랫폼

AI와 디지털 트윈 개념을 활용해 행사장의 배치·동선·혼잡·접근성을 사전에 시뮬레이션하는 Streamlit 프로토타입입니다.

주요 기능

•
행사명, 유형, 규모, 예상 방문객, 부스 수, 예산 입력

•
안전·참여·운영·예산 중심의 최적화 목표 선택

•
포용적 접근성 기준 적용

•
AI 설계안 생성 버튼을 통한 결정론적 데모 시뮬레이션

•
혼잡 Heatmap, 핵심 KPI, 기준안 대비 비교 차트

•
XAI 설계 근거와 Markdown 리포트 다운로드


현재 버전은 외부 AI API 없이 실행되는 데모 엔진입니다. 실제 AI/백엔드 연동 시 simulate() 함수를 API 호출 모듈로 교체하면 됩니다.

로컬 실행

Bash


python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py



Streamlit Community Cloud 배포

1.
이 폴더의 파일을 GitHub 저장소에 업로드합니다.

2.


share.streamlit.io에서 GitHub로 로그인합니다.

3.
저장소와 브랜치를 선택하고 Main file path에 app.py를 입력합니다.

4.
Deploy를 누릅니다.

프로젝트 구조

Plain Text


.
├── app.py             # Streamlit 앱 및 데모 시뮬레이션 엔진
├── requirements.txt   # 배포 의존성
├── README.md
└── .gitignore



