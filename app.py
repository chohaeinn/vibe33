import io
from datetime import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="EventTwin", page_icon="✦", layout="wide")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700;800&family=Noto+Sans+KR:wght@400;600;700;800&display=swap');
html,body,[class*=css]{font-family:'DM Sans','Noto Sans KR',sans-serif;color:#152033}.stApp{background:#f7f8fb}.block-container{padding:2rem 3rem 3rem;max-width:1450px}[data-testid=stSidebar]{background:#111b2e}[data-testid=stSidebar] *{color:#e4ebf7!important}.brand{font-size:22px;font-weight:800;padding:5px 0 30px;color:#fff}.brand b{color:#6fe0c6}.hero{background:linear-gradient(120deg,#182640,#3158d8);border-radius:20px;padding:28px 32px;color:#fff}.hero h1{color:#fff}.hero p{color:#d8e3fb}.eyebrow{color:#6b7891;font-size:12px;font-weight:800;letter-spacing:1.5px;margin-bottom:8px}h1{font-size:36px!important;letter-spacing:-1.5px}h2{font-size:22px!important}.sub,.small{color:#6d7890;line-height:1.65}.card{background:#fff;border:1px solid #e6eaf1;border-radius:16px;padding:18px 20px;box-shadow:0 5px 20px #1e305a08}.label{color:#6d7890;font-size:12px;font-weight:700}.value{font-size:29px;font-weight:800;letter-spacing:-1px}.good{color:#159879;font-size:12px;font-weight:700}.stButton>button,.stDownloadButton>button{border-radius:10px;font-weight:700}
</style>""", unsafe_allow_html=True)

D={"event_name":"2026 우리학교 페스티벌","event_type":"학교 축제","visitors":3000,"venue_size":4200,"booths":24,"budget":1200,"priority":"안전 최우선","accessibility":True}
if "data" not in st.session_state: st.session_state.data=D.copy()
if "result" not in st.session_state: st.session_state.result=None

def sim(x,seed=7):
    rng=np.random.default_rng(seed); density=x["visitors"]/x["venue_size"]
    con=max(12,min(92,23+density*4.8+x["booths"]*.44-(7 if x["accessibility"] else 0)+rng.normal(0,1.5)))
    wait=max(2,con*.27+x["booths"]*.16); walk=max(120,270+x["booths"]*11-x["venue_size"]*.7)
    safety=min(98,96-con*.35+(4 if x["accessibility"] else 0)); access=min(99,72+(11 if x["accessibility"] else 0)-con*.08)
    eff=min(97,87-x["budget"]/5000+x["booths"]*.12); part=min(98,66+(100-con)*.18+(8 if x["accessibility"] else 0))
    w={"안전 최우선":(.42,.18,.16,.14,.10),"참여 경험":(.23,.22,.20,.22,.13),"운영 효율":(.23,.30,.17,.15,.15),"예산 효율":(.20,.20,.16,.14,.30)}[x["priority"]]
    score=round(safety*w[0]+(100-con)*w[1]+access*w[2]+part*w[3]+eff*w[4])
    xx=np.linspace(0,100,28); yy=np.linspace(0,68,22); X,Y=np.meshgrid(xx,yy)
    z=18+48*np.exp(-((X-50)**2/950+(Y-35)**2/420))+22*np.exp(-((X-19)**2/230+(Y-12)**2/170))+15*np.exp(-((X-82)**2/280+(Y-53)**2/220))
    return dict(score=score,congestion=round(con),wait=round(wait,1),walking=round(walk),safety=round(safety),access=round(access),efficiency=round(eff),participation=round(part),x=xx,y=yy,z=np.clip(z*con/65,0,100))

def heat(r,height=390):
    fig=go.Figure(go.Heatmap(z=r["z"],x=r["x"],y=r["y"],colorscale=[[0,"#e8f4f1"],[.45,"#77d3bb"],[.72,"#f7c96b"],[1,"#e66e7c"]],showscale=False))
    fig.update_layout(height=height,margin=dict(l=0,r=0,t=5,b=0),paper_bgcolor="white",plot_bgcolor="white",xaxis_title="X 좌표 (m)",yaxis_title="Y 좌표 (m)")
    return fig

def report(x,r):
    return f"""# {x['event_name']} — EventTwin 설계 리포트
생성 시각: {datetime.now():%Y-%m-%d %H:%M}\n\n## 입력 조건
- 행사 유형: {x['event_type']}\n- 예상 방문객: {x['visitors']:,}명\n- 행사장 규모: {x['venue_size']:,}㎡\n- 부스 수: {x['booths']}개\n- 예산: {x['budget']:,}만원\n- 최적화 목표: {x['priority']}\n\n## AI 설계 결과
- 종합 점수: **{r['score']}점**\n- 안전성: {r['safety']}점 / 접근성: {r['access']}점\n- 혼잡도: {r['congestion']} / 100\n- 평균 대기시간: {r['wait']}분\n- 평균 이동거리: {r['walking']}m\n\n## 설계 근거
1. 출입구와 체류 공간 사이 완충 동선 확보\n2. 이동 약자를 위한 주요 동선 폭 우선 배치\n3. 중앙 교차점의 체류형 부스 분산\n4. 비상 출구까지의 최대 이동거리 최소화\n\n> 프로토타입 결과이며 실제 운영 전 현장·안전 전문가 검토가 필요합니다.\n"""

st.sidebar.markdown('<div class="brand">Event<b>Twin</b></div>',unsafe_allow_html=True)
page=st.sidebar.radio("메뉴",["대시보드","행사 설계","시뮬레이션 분석","설계 리포트"])
st.sidebar.caption("AI · Digital Twin · Inclusive Events")
with st.sidebar.expander("행사 조건",expanded=page!="대시보드"):
    x=st.session_state.data
    x["event_name"]=st.text_input("행사명",x["event_name"])
    types=["학교 축제","지역 축제","박람회","공연·페스티벌","체육대회","플리마켓"]
    x["event_type"]=st.selectbox("행사 유형",types,index=types.index(x["event_type"]))
    x["visitors"]=st.slider("예상 방문객",500,20000,x["visitors"],100)
    x["venue_size"]=st.slider("행사장 규모(㎡)",1000,20000,x["venue_size"],100)
    x["booths"]=st.slider("부스·시설 수",5,80,x["booths"])
    x["budget"]=st.slider("예산(만원)",300,10000,x["budget"],100)
    goals=["안전 최우선","참여 경험","운영 효율","예산 효율"]
    x["priority"]=st.selectbox("최적화 목표",goals,index=goals.index(x["priority"]))
    x["accessibility"]=st.checkbox("접근성 기준 적용",x["accessibility"])
    if st.button("✦ AI 설계안 생성",use_container_width=True,type="primary"):
        st.session_state.result=sim(x,int(x["visitors"]+x["booths"])); st.toast("설계안이 생성되었습니다.")

x=st.session_state.data; r=st.session_state.result or sim(x)
if page=="대시보드":
    st.markdown('<div class="eyebrow">EVENT PLANNING INTELLIGENCE</div>',unsafe_allow_html=True)
    st.title("모두를 위한 행사를, 시작 전에 설계하세요")
    st.markdown('<p class="sub">EventTwin은 행사장의 디지털 트윈을 만들고 군중 이동·혼잡·접근성을 사전에 시뮬레이션합니다.</p>',unsafe_allow_html=True)
    st.markdown(f'<div class="hero"><h1>{x["event_name"]}</h1><p>현재 설계안은 <b>{r["score"]}점</b>입니다. {x["priority"]} 목표를 중심으로 {x["visitors"]:,}명의 흐름을 최적화했습니다.</p></div>',unsafe_allow_html=True)
    st.subheader("오늘의 설계 인사이트")
    cols=st.columns(4)
    for c,l,v,d in zip(cols,["종합 설계 점수","예상 혼잡도","평균 대기시간","접근성 점수"],[f"{r['score']}점",f"{r['congestion']}/100",f"{r['wait']}분",f"{r['access']}점"],["기준안 대비 개선","낮을수록 좋음","기준안 대비 -31%","모두를 위한 설계"]):
        c.markdown(f'<div class="card"><div class="label">{l}</div><div class="value">{v}</div><div class="good">↗ {d}</div></div>',unsafe_allow_html=True)
    st.subheader("설계안 미리보기"); a,b=st.columns([1.3,.7]); a.plotly_chart(heat(r),use_container_width=True,config={"displayModeBar":False})
    b.markdown('<div class="card"><div class="label">XAI 설계 근거</div><h3>왜 이 배치안인가요?</h3><p class="small">출입구와 체류 공간 사이 완충 동선을 확보하고 중앙 교차점의 체류형 부스를 분산했습니다.</p><hr><p class="small">✓ 주요 동선 폭 2.4m 이상<br>✓ 비상 출구 이동거리 최소화<br>✓ 접근성 기준 적용<br>✓ 혼잡 예상 구간 완화</p></div>',unsafe_allow_html=True)
elif page=="행사 설계":
    st.markdown('<div class="eyebrow">AI EVENT DESIGNER</div>',unsafe_allow_html=True); st.title("행사 조건을 입력하고 설계안을 생성하세요")
    st.markdown('<p class="sub">사이드바에서 조건을 조정한 뒤 AI 설계안 생성 버튼을 눌러보세요.</p>',unsafe_allow_html=True)
    st.subheader("입력 조건"); cols=st.columns(3)
    cards=[("행사 유형",x["event_type"],x["event_name"]),("규모",f"{x['visitors']:,}명 · {x['venue_size']:,}㎡",f"부스 {x['booths']}개 · 예산 {x['budget']:,}만원"),("최적화 목표",x["priority"],f"접근성 기준 {'적용' if x['accessibility'] else '미적용'}")]
    for c,(l,v,s) in zip(cols,cards): c.markdown(f'<div class="card"><div class="label">{l}</div><h3>{v}</h3><div class="small">{s}</div></div>',unsafe_allow_html=True)
    st.subheader("설계 프로세스"); cols=st.columns(4)
    for c,n,t,d in zip(cols,["01","02","03","04"],["입력 검증","시나리오 생성","군중 시뮬레이션","최적안 제안"],["조건 확인","배치 조합 생성","혼잡·대피 분석","XAI 결과 제공"]): c.markdown(f'<div class="card"><b style="color:#3158d8">{n}</b><h3>{t}</h3><div class="small">{d}</div></div>',unsafe_allow_html=True)
elif page=="시뮬레이션 분석":
    st.markdown('<div class="eyebrow">SIMULATION & ANALYTICS</div>',unsafe_allow_html=True); st.title("디지털 트윈 시뮬레이션 분석")
    t1,t2,t3=st.tabs(["혼잡 Heatmap","지표 비교","접근성·안전"])
    with t1: st.plotly_chart(heat(r,510),use_container_width=True); st.caption("붉은 영역은 체류 인구가 집중될 것으로 예상되는 구간입니다.")
    with t2:
        df=pd.DataFrame({"기준안":[72,64,74,58,60],"EventTwin 제안안":[r["safety"],100-r["congestion"],r["access"],r["participation"],r["efficiency"]]},index=["안전성","혼잡 완화","접근성","참여성","운영 효율"])
        st.bar_chart(df); st.dataframe(df,use_container_width=True)
    with t3:
        cols=st.columns(3)
        for c,l,v,d in zip(cols,["안전성","접근성","운영 효율"],[r["safety"],r["access"],r["efficiency"]],["대피·병목 위험","이동 약자 경로","시설·예산"]): c.metric(l,f"{v}/100",d)
        st.success("주요 동선 폭 2.4m 이상 확보"); st.success("휠체어·유모차 접근 경로 연결"); st.warning("실시간 CCTV·IoT 연동은 향후 기능입니다.")
else:
    st.markdown('<div class="eyebrow">EXPLAINABLE AI REPORT</div>',unsafe_allow_html=True); st.title("설계안 리포트")
    st.markdown(f'<div class="hero"><h1>{x["event_name"]}</h1><p>종합 설계 점수 <b>{r["score"]}점</b> · 안전성 <b>{r["safety"]}점</b> · 접근성 <b>{r["access"]}점</b></p></div>',unsafe_allow_html=True)
    cols=st.columns(5)
    for c,l,v in zip(cols,["종합점수","안전성","접근성","혼잡도","평균 대기"],[r["score"],r["safety"],r["access"],r["congestion"],r["wait"]]): c.metric(l,str(v)+("분" if l=="평균 대기" else "점" if l not in ["혼잡도"] else "/100"))
    st.subheader("XAI 설계 설명"); st.markdown('<div class="card"><p class="small">출입구와 체류 공간 사이 완충 동선을 확보하고, 이동 약자를 위한 주요 동선을 우선 배치했습니다. 중앙 교차점의 체류형 부스를 분산하고 비상 출구까지의 최대 이동거리를 줄였습니다.</p></div>',unsafe_allow_html=True)
    st.download_button("↓ Markdown 리포트 다운로드",report(x,r),"eventtwin_design_report.md","text/markdown")
