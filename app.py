import base64
import html
import uuid
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="알집 Alz' Zip",
    page_icon="🐣",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "assets" / "logo_remove.png"


# -----------------------------
# 공통 유틸리티
# -----------------------------
def format_date(value):
    """date 객체 또는 문자열을 YYYY-MM-DD 형태로 변환합니다."""
    if isinstance(value, date):
        return value.strftime("%Y-%m-%d")
    return str(value)


def parse_date_value(value, fallback=date(1950, 1, 1)):
    """date_input 기본값으로 사용할 수 있도록 날짜 값을 date 객체로 변환합니다."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value

    try:
        return datetime.strptime(str(value), "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return fallback


def safe_text(value):
    """HTML 렌더링 시 사용자 입력값을 안전하게 표시합니다."""
    return html.escape(str(value))


def apply_custom_css():
    """의료 서비스에 어울리는 정돈된 프리미엄 UI 스타일을 적용합니다."""
    st.markdown(
        """
        <style>
        /* -----------------------------
           Design Tokens
        ----------------------------- */
        :root {
            --az-primary: #0B6FB8;
            --az-primary-dark: #064E8A;
            --az-primary-soft: #E9F5FF;
            --az-accent: #2CB8AF;
            --az-accent-soft: #EAF9F7;
            --az-bg: #F5FBFC;
            --az-card: rgba(255, 255, 255, 0.86);
            --az-border: rgba(148, 163, 184, 0.22);
            --az-border-strong: rgba(100, 116, 139, 0.22);
            --az-text: #172033;
            --az-muted: #667085;
            --az-muted-light: #8A94A6;
            --az-success: #DFF7E9;
            --az-success-text: #177245;
            --az-warning: #FFF4D6;
            --az-warning-text: #8A5A00;
            --az-danger: #EF4444;
            --az-shadow-sm: 0 8px 22px rgba(15, 23, 42, 0.06);
            --az-shadow-md: 0 18px 48px rgba(15, 23, 42, 0.09);
            --az-shadow-lg: 0 28px 70px rgba(15, 23, 42, 0.12);
            --az-radius-sm: 14px;
            --az-radius-md: 20px;
            --az-radius-lg: 28px;
        }

        /* -----------------------------
           Streamlit 기본 장식 최소화
        ----------------------------- */
        #MainMenu,
        footer,
        div[data-testid="stToolbar"],
        div[data-testid="stDecoration"] {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
        }

        /*
           사이드바를 접었을 때 다시 펼치는 Streamlit 기본 버튼은
           header 영역 안에 있으므로 header 자체는 숨기지 않습니다.
        */
        header[data-testid="stHeader"] {
            display: block !important;
            visibility: visible !important;
            height: 3rem !important;
            background: transparent !important;
            box-shadow: none !important;
            pointer-events: auto !important;
            z-index: 999999 !important;
        }

        header[data-testid="stHeader"] button,
        header[data-testid="stHeader"] [role="button"],
        div[data-testid="collapsedControl"],
        div[data-testid="stSidebarCollapsedControl"],
        button[data-testid="stBaseButton-header"],
        button[data-testid="stSidebarCollapseButton"],
        button[aria-label="Open sidebar"],
        button[aria-label="Close sidebar"] {
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }

        html,
        body,
        [class*="css"],
        .stApp {
            font-family: -apple-system, BlinkMacSystemFont, "Pretendard", "Noto Sans KR", "Apple SD Gothic Neo", "Segoe UI", sans-serif;
            color: var(--az-text);
        }

        .stApp {
            background:
                radial-gradient(circle at 16% 10%, rgba(91, 192, 248, 0.20), transparent 28%),
                radial-gradient(circle at 86% 8%, rgba(44, 184, 175, 0.18), transparent 31%),
                linear-gradient(135deg, #F8FCFF 0%, #F2FBF9 50%, #F7FAFF 100%);
        }

        .main {
            background-color: transparent;
        }

        .block-container {
            /* 환자 목록 / 환자 상세 / AI 진단 화면이 모두 같은 기준 폭을 사용하도록 통일 */
            max-width: 1280px;
            padding-top: 2.4rem;
            padding-bottom: 4rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        h1, h2, h3, h4 {
            letter-spacing: -0.035em;
            color: var(--az-text);
        }

        p,
        label,
        div[data-testid="stMarkdownContainer"] p {
            color: inherit;
        }

        hr {
            border: none;
            border-top: 1px solid var(--az-border);
            margin: 1.2rem 0;
        }

        /* -----------------------------
           로그인 화면
        ----------------------------- */
        .login-top-copy {
            max-width: 980px;
            margin: 0.15rem auto 1.65rem auto;
            text-align: center;
        }

        .login-hero-logo {
            display: block;
            width: 310px;
            max-width: min(58vw, 360px);
            height: auto;
            margin: 0 auto 0.85rem auto;
            filter: drop-shadow(0 12px 22px rgba(10, 110, 189, 0.10));
        }

        .login-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.42rem 0.82rem;
            border-radius: 999px;
            background: rgba(11, 111, 184, 0.08);
            border: 1px solid rgba(11, 111, 184, 0.12);
            color: var(--az-primary);
            font-weight: 800;
            font-size: 0.82rem;
            margin-bottom: 0.9rem;
        }

        .login-top-copy h1 {
            margin: 0;
            color: var(--az-text);
            font-size: clamp(2.15rem, 3.6vw, 3.15rem);
            line-height: 1.16;
            font-weight: 900;
            letter-spacing: -0.055em;
        }

        .login-top-copy p {
            margin-top: 0.95rem;
            color: var(--az-muted);
            font-size: 1.03rem;
            line-height: 1.72;
        }

        .login-feature-panel {
            background: linear-gradient(180deg, rgba(255,255,255,0.90), rgba(255,255,255,0.72));
            border: 1px solid var(--az-border);
            border-radius: var(--az-radius-lg);
            padding: 1.25rem;
            box-shadow: var(--az-shadow-lg);
            backdrop-filter: blur(14px);
        }

        .feature-row {
            display: flex;
            gap: 1rem;
            padding: 1.05rem 0.45rem;
            border-bottom: 1px solid rgba(148, 163, 184, 0.16);
        }

        .feature-row:first-child {
            padding-top: 0.4rem;
        }

        .feature-row:last-child {
            border-bottom: none;
            padding-bottom: 0.35rem;
        }

        .feature-icon {
            width: 48px;
            min-width: 48px;
            height: 48px;
            border-radius: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #EFF8FF, #EAF9F7);
            box-shadow: inset 0 0 0 1px rgba(11, 111, 184, 0.06);
            font-size: 1.3rem;
        }

        .feature-row b {
            color: var(--az-text);
            font-size: 1.02rem;
            font-weight: 850;
        }

        .feature-row p {
            margin: 0.32rem 0 0 0;
            color: var(--az-muted);
            font-size: 0.91rem;
            line-height: 1.58;
        }

        .login-card-head {
            margin-bottom: 1.1rem;
        }

        .login-card-icon {
            width: 52px;
            height: 52px;
            border-radius: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, var(--az-primary-soft), var(--az-accent-soft));
            color: var(--az-primary);
            font-size: 1.45rem;
            margin-bottom: 0.9rem;
        }

        .login-card-title {
            margin: 0;
            font-size: 1.55rem;
            font-weight: 900;
            color: var(--az-text);
            letter-spacing: -0.045em;
        }

        .login-card-subtitle {
            margin: 0.35rem 0 0 0;
            color: var(--az-muted);
            font-size: 0.93rem;
            line-height: 1.55;
        }

        .login-helper {
            margin-top: 0.85rem;
            color: var(--az-muted-light);
            font-size: 0.82rem;
            text-align: center;
        }


        .auth-divider {
            height: 1px;
            background: rgba(148, 163, 184, 0.18);
            margin: 1.05rem 0 0.95rem 0;
        }

        .signup-cta-copy {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
            margin-bottom: 0.72rem;
            padding: 0.86rem 0.9rem;
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(233,245,255,0.72), rgba(234,249,247,0.64));
            border: 1px solid rgba(11, 111, 184, 0.10);
        }

        .signup-cta-copy strong {
            color: var(--az-text);
            font-size: 0.92rem;
            font-weight: 900;
            letter-spacing: -0.025em;
        }

        .signup-cta-copy span {
            color: var(--az-muted);
            font-size: 0.82rem;
            line-height: 1.45;
        }

        .signup-inline-head {
            margin: 0.2rem 0 0.85rem 0;
        }

        .signup-inline-title {
            margin: 0;
            color: var(--az-text);
            font-size: 1.04rem;
            font-weight: 900;
            letter-spacing: -0.035em;
        }

        .signup-inline-desc {
            margin: 0.24rem 0 0 0;
            color: var(--az-muted);
            font-size: 0.82rem;
            line-height: 1.5;
        }

        .signup-page-copy {
            max-width: 760px;
            margin: 0.15rem auto 1.35rem auto;
            text-align: center;
        }

        .signup-page-copy .login-hero-logo {
            width: 250px;
            max-width: min(52vw, 300px);
            margin-bottom: 0.7rem;
        }

        .signup-page-copy h1 {
            margin: 0.7rem 0 0 0;
            color: var(--az-text);
            font-size: clamp(1.95rem, 3.2vw, 2.72rem);
            line-height: 1.18;
            font-weight: 920;
            letter-spacing: -0.055em;
        }

        .signup-page-copy p {
            margin-top: 0.72rem;
            color: var(--az-muted);
            font-size: 0.98rem;
            line-height: 1.65;
        }

        .signup-step-head {
            display: flex;
            gap: 0.75rem;
            align-items: flex-start;
            margin: 0.35rem 0 1rem 0;
        }

        .signup-step-badge {
            width: 36px;
            min-width: 36px;
            height: 36px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, var(--az-primary-soft), var(--az-accent-soft));
            color: var(--az-primary-dark);
            font-weight: 900;
            font-size: 0.9rem;
            border: 1px solid rgba(11, 111, 184, 0.10);
        }

        .signup-step-title {
            margin: 0;
            color: var(--az-text);
            font-size: 1.18rem;
            font-weight: 900;
            letter-spacing: -0.04em;
        }

        .signup-step-desc {
            margin: 0.24rem 0 0 0;
            color: var(--az-muted);
            font-size: 0.86rem;
            line-height: 1.5;
        }

        .signup-complete-guide {
            margin: 1rem 0 0 0;
            padding: 0.88rem 0.95rem;
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(223,247,233,0.72), rgba(234,249,247,0.62));
            border: 1px solid rgba(23, 114, 69, 0.14);
            color: #276749;
            font-size: 0.84rem;
            line-height: 1.55;
            font-weight: 750;
        }

        .auth-mode-note {
            margin: 0.15rem 0 1rem 0;
            padding: 0.8rem 0.9rem;
            border-radius: 16px;
            background: linear-gradient(135deg, rgba(233,245,255,0.72), rgba(234,249,247,0.68));
            border: 1px solid rgba(11, 111, 184, 0.10);
            color: var(--az-muted);
            font-size: 0.84rem;
            line-height: 1.55;
        }

        .approval-status-card {
            min-height: 3.95rem;
            height: 100%;
            padding: 0.82rem 0.95rem;
            border-radius: 18px;
            border: 1px solid rgba(148, 163, 184, 0.18);
            background: rgba(255,255,255,0.78);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.68), 0 10px 22px rgba(15, 23, 42, 0.05);
            display: flex;
            align-items: center;
            gap: 0.78rem;
            margin: 0.05rem 0 0.45rem 0;
        }

        .approval-status-card.approved {
            background: linear-gradient(135deg, rgba(223,247,233,0.94), rgba(234,249,247,0.84));
            border-color: rgba(23, 114, 69, 0.20);
        }

        .approval-status-card.pending {
            background: linear-gradient(135deg, rgba(233,245,255,0.96), rgba(234,249,247,0.92));
            border-color: rgba(11, 111, 184, 0.16);
        }

        .approval-status-icon {
            width: 42px;
            min-width: 42px;
            height: 42px;
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, rgba(11,111,184,0.14), rgba(44,184,175,0.16));
            color: var(--az-primary-dark);
            font-size: 1.02rem;
            font-weight: 900;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.72);
        }

        .approval-status-body {
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 0.16rem;
        }

        .approval-status-title {
            margin: 0;
            color: var(--az-text);
            font-size: 0.9rem;
            font-weight: 900;
            letter-spacing: -0.02em;
        }

        .approval-status-desc {
            margin: 0;
            color: var(--az-muted);
            font-size: 0.8rem;
            line-height: 1.45;
        }

        .approval-status-card.pending .approval-status-desc {
            font-size: 0.74rem;
        }

        /* -----------------------------
           카드 / 컨테이너
        ----------------------------- */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            position: relative;
            overflow: hidden;
            background: linear-gradient(180deg, rgba(255,255,255,0.94), rgba(255,255,255,0.82));
            border: 1px solid rgba(255, 255, 255, 0.48) !important;
            border-radius: var(--az-radius-lg) !important;
            box-shadow: 0 12px 34px rgba(15, 23, 42, 0.07);
            backdrop-filter: blur(16px);
        }

        div[data-testid="stVerticalBlockBorderWrapper"]::before {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, rgba(11,111,184,0.05), rgba(44,184,175,0.02) 35%, rgba(255,255,255,0) 65%);
            pointer-events: none;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            border-color: rgba(11, 111, 184, 0.22) !important;
            box-shadow: 0 16px 36px rgba(15, 23, 42, 0.09);
            transform: translateY(-1px);
            transition: all 0.18s ease;
        }

        .section-title-row {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            gap: 1rem;
            margin: 1.2rem 0 0.75rem 0;
        }

        .section-kicker {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.28rem 0.65rem;
            border-radius: 999px;
            background: rgba(44, 184, 175, 0.10);
            color: #12877F;
            font-weight: 800;
            font-size: 0.78rem;
            margin-bottom: 0.45rem;
        }

        .section-title {
            margin: 0;
            color: var(--az-text);
            font-size: 1.45rem;
            font-weight: 900;
            letter-spacing: -0.045em;
        }

        .section-desc {
            margin: 0.25rem 0 0 0;
            color: var(--az-muted);
            font-size: 0.94rem;
        }

        /* -----------------------------
           메인 Hero 영역
        ----------------------------- */
        .medical-hero {
            position: relative;
            overflow: hidden;
            padding: 1.65rem 1.8rem;
            border-radius: 26px;
            background:
                radial-gradient(circle at 88% 18%, rgba(255,255,255,0.32), transparent 24%),
                linear-gradient(135deg, #075F9B 0%, #1389D4 48%, #55C7EE 100%);
            color: white;
            margin-bottom: 1.25rem;
            box-shadow: 0 18px 42px rgba(10, 110, 189, 0.22);
        }

        .medical-hero::after {
            content: "";
            position: absolute;
            width: 220px;
            height: 220px;
            right: -80px;
            top: -90px;
            border-radius: 999px;
            background: rgba(255,255,255,0.20);
        }

        .hero-kicker {
            display: inline-flex;
            align-items: center;
            padding: 0.28rem 0.64rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.18);
            border: 1px solid rgba(255,255,255,0.22);
            color: rgba(255,255,255,0.95);
            font-size: 0.78rem;
            font-weight: 800;
            margin-bottom: 0.68rem;
        }

        .medical-hero h1 {
            position: relative;
            z-index: 1;
            margin: 0;
            font-size: clamp(1.9rem, 3vw, 2.45rem);
            font-weight: 920;
            color: #fff;
            letter-spacing: -0.055em;
        }

        .medical-hero p {
            position: relative;
            z-index: 1;
            margin: 0.58rem 0 0 0;
            color: rgba(255,255,255,0.92);
            font-size: 1.02rem;
            line-height: 1.65;
        }

        /* -----------------------------
           환자 목록
        ----------------------------- */
        .patient-toolbar-copy {
            margin-bottom: 0.9rem;
        }

        .patient-toolbar-title {
            margin: 0;
            color: var(--az-text);
            font-size: 1.02rem;
            font-weight: 900;
            letter-spacing: -0.03em;
        }

        .patient-toolbar-desc {
            margin: 0.32rem 0 0 0;
            color: var(--az-muted);
            font-size: 0.91rem;
            line-height: 1.58;
        }

        .patient-toolbar-label {
            margin: 0 0 0.45rem 0;
            color: #344054;
            font-weight: 800;
            font-size: 0.88rem;
            line-height: 1.25rem;
        }

        .patient-table-header {
            display: grid;
            grid-template-columns: 1.55fr 1.25fr 0.85fr 1.45fr;
            gap: 1.1rem;
            padding: 0.82rem 1rem;
            margin-bottom: 0.45rem;
            color: #4B5565;
            font-size: 0.84rem;
            font-weight: 900;
            letter-spacing: 0.01em;
            border-radius: 18px;
            background: linear-gradient(180deg, rgba(255,255,255,0.78), rgba(246,250,253,0.62));
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.60);
        }

        .patient-row-content {
            min-height: 4.55rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .patient-name-row {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            flex-wrap: wrap;
        }

        .patient-name {
            margin-top: 0;
            font-weight: 900;
            color: var(--az-text);
            font-size: 1.02rem;
            letter-spacing: -0.02em;
        }

        .patient-id {
            margin-top: 0.26rem;
            color: var(--az-muted-light);
            font-size: 0.78rem;
            font-weight: 700;
        }

        .patient-history-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.2rem;
            padding: 0.32rem 0.58rem;
            border-radius: 999px;
            background: rgba(44, 184, 175, 0.10);
            color: #127C75;
            font-size: 0.74rem;
            font-weight: 850;
            line-height: 1;
        }

        .patient-result-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 0.75rem;
            margin: 0.85rem 0 0.6rem 0;
        }

        .patient-result-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.46rem 0.78rem;
            border-radius: 999px;
            background: linear-gradient(135deg, rgba(11,111,184,0.10), rgba(44,184,175,0.10));
            border: 1px solid rgba(11,111,184,0.14);
            color: var(--az-primary-dark);
            font-size: 0.82rem;
            font-weight: 850;
        }

        .patient-result-meta {
            color: var(--az-muted);
            font-size: 0.84rem;
            font-weight: 700;
        }

        .patient-list-bottom-spacer {
            min-height: clamp(1.2rem, 6vh, 4rem);
        }

        .gender-pill,
        .score-pill,
        .info-pill {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: fit-content;
            border-radius: 999px;
            font-weight: 850;
            line-height: 1;
        }

        .gender-pill {
            padding: 0.46rem 0.78rem;
            background: linear-gradient(135deg, rgba(233,245,255,0.96), rgba(234,249,247,0.92));
            color: var(--az-primary-dark);
            font-size: 0.82rem;
            border: 1px solid rgba(11, 111, 184, 0.08);
        }

        .info-pill {
            padding: 0.44rem 0.74rem;
            background: rgba(100, 116, 139, 0.08);
            color: var(--az-muted);
            font-size: 0.82rem;
            border: 1px solid rgba(148, 163, 184, 0.12);
        }

        /* -----------------------------
           환자 프로필 요약 패널
        ----------------------------- */
        .profile-grid {
            display: grid;
            grid-template-columns: 1.25fr repeat(3, minmax(0, 1fr));
            gap: 0.75rem;
            margin: 0.35rem 0 1rem 0;
            padding: 0.9rem;
            border-radius: 24px;
            background: linear-gradient(135deg, rgba(255,255,255,0.92), rgba(248,252,255,0.74));
            border: 1px solid rgba(148, 163, 184, 0.20);
            box-shadow: 0 14px 34px rgba(15, 23, 42, 0.055);
            backdrop-filter: blur(14px);
        }

        .profile-card {
            position: relative;
            display: flex;
            align-items: center;
            gap: 0.78rem;
            min-height: 82px;
            padding: 0.9rem 0.95rem;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.66);
            border: 1px solid rgba(148, 163, 184, 0.14);
            box-shadow: none;
        }

        .profile-card:first-child {
            background: linear-gradient(135deg, rgba(233,245,255,0.92), rgba(234,249,247,0.76));
            border-color: rgba(11, 111, 184, 0.14);
        }

        .profile-icon {
            width: 38px;
            min-width: 38px;
            height: 38px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(11, 111, 184, 0.08);
            color: var(--az-primary-dark);
            font-size: 1.05rem;
        }

        .profile-label {
            margin: 0;
            color: var(--az-muted-light);
            font-size: 0.74rem;
            font-weight: 800;
            letter-spacing: -0.01em;
        }

        .profile-value {
            margin: 0.22rem 0 0 0;
            color: var(--az-text);
            font-size: 1.02rem;
            font-weight: 400; /* 실제 값 전체를 가늘게 */
            letter-spacing: -0.025em;
            line-height: 1.25;
        }

        .profile-card:first-child .profile-value {
            font-size: 1.16rem;
            font-weight: 400; /* 이름 값도 동일하게 */
        }

        /* -----------------------------
           입력창 / 폼 / 버튼
        ----------------------------- */
        div[data-testid="stForm"] {
            border: 0;
            padding: 0;
        }

        .stTextInput input,
        .stDateInput input,
        .stNumberInput input,
        textarea,
        div[data-baseweb="select"] > div {
            border-radius: 14px !important;
            border: 1px solid rgba(206, 220, 235, 0.92) !important;
            background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(248, 250, 252, 0.92)) !important;
            min-height: 3rem;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.85) !important;
            color: var(--az-text) !important;
        }

        .stTextInput input:focus,
        .stDateInput input:focus,
        .stNumberInput input:focus,
        textarea:focus {
            border-color: #55BEE8 !important;
            box-shadow: 0 0 0 3px rgba(85, 190, 232, 0.18) !important;
        }

        label[data-testid="stWidgetLabel"] p {
            color: #344054;
            font-weight: 800;
            font-size: 0.88rem;
        }

        .stButton > button,
        .stFormSubmitButton > button {
            border-radius: 14px !important;
            min-height: 2.95rem;
            font-weight: 850 !important;
            letter-spacing: -0.015em;
            transition: transform 0.16s ease, box-shadow 0.16s ease, border-color 0.16s ease, background 0.16s ease;
        }

        button[kind="primary"],
        .stFormSubmitButton button[kind="primary"] {
            background: linear-gradient(135deg, var(--az-primary) 0%, var(--az-accent) 100%) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 12px 24px rgba(11, 111, 184, 0.22) !important;
        }

        button[kind="primary"]:hover,
        .stFormSubmitButton button[kind="primary"]:hover {
            transform: translateY(-1px);
            box-shadow: 0 16px 30px rgba(11, 111, 184, 0.28) !important;
            filter: saturate(1.05);
        }

        button[kind="secondary"] {
            background: rgba(255,255,255,0.84) !important;
            color: #24364D !important;
            border: 1px solid var(--az-border-strong) !important;
            box-shadow: 0 8px 18px rgba(15, 23, 42, 0.04) !important;
        }

        button[kind="secondary"]:hover {
            transform: translateY(-1px);
            border-color: rgba(11, 111, 184, 0.32) !important;
            color: var(--az-primary-dark) !important;
            box-shadow: 0 12px 24px rgba(15, 23, 42, 0.07) !important;
        }

        .mmse-guide-card {
            height: 100%;
            padding: 0.92rem 1rem;
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(233,245,255,0.78), rgba(234,249,247,0.72));
            border: 1px solid rgba(11, 111, 184, 0.12);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.68);
        }

        .mmse-guide-card h4 {
            margin: 0;
            color: var(--az-text);
            font-size: 0.96rem;
            font-weight: 900;
            letter-spacing: -0.03em;
        }

        .mmse-guide-card p {
            margin: 0.34rem 0 0 0;
            color: var(--az-muted);
            font-size: 0.84rem;
            line-height: 1.55;
            word-break: keep-all;
        }

        .mmse-score-note {
            margin-top: 0.52rem;
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.34rem 0.58rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.72);
            color: var(--az-primary-dark);
            font-size: 0.76rem;
            font-weight: 850;
        }

        div[data-testid="stFileUploaderDropzone"] {
            background: rgba(255,255,255,0.72);
            border: 1.5px dashed rgba(11, 111, 184, 0.30);
            border-radius: 20px;
            padding: 1.1rem;
        }

        div[data-testid="stFileUploaderDropzone"]:hover {
            background: rgba(233, 245, 255, 0.60);
            border-color: rgba(11, 111, 184, 0.48);
        }

        div[data-testid="stCheckbox"] label {
            background: rgba(255,255,255,0.72);
            border: 1px solid var(--az-border);
            border-radius: 14px;
            padding: 0.62rem 0.72rem;
            width: 100%;
            transition: all 0.15s ease;
        }

        div[data-testid="stCheckbox"] label:hover {
            border-color: rgba(44, 184, 175, 0.38);
            background: rgba(234, 249, 247, 0.60);
        }

        /* -----------------------------
           알림 / Expander / Dataframe
        ----------------------------- */
        div[data-testid="stAlert"] {
            border-radius: 18px;
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow: 0 10px 22px rgba(15, 23, 42, 0.035);
        }

        details[data-testid="stExpander"] {
            border-radius: 18px !important;
            border: 1px solid var(--az-border) !important;
            background: rgba(255,255,255,0.74) !important;
            box-shadow: var(--az-shadow-sm);
            overflow: hidden;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 18px;
            overflow: hidden;
            border: 1px solid var(--az-border);
        }

        /* -----------------------------
           진단 결과 카드
        ----------------------------- */
        .result-card {
            background: rgba(255,255,255,0.88);
            border: 1px solid var(--az-border);
            border-left: 6px solid var(--az-primary);
            border-radius: 22px;
            padding: 1.05rem 1.2rem;
            margin: 1rem 0 0.65rem 0;
            box-shadow: var(--az-shadow-sm);
        }

        .result-card-head {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 0.35rem;
        }

        .result-card h4 {
            margin: 0;
            color: var(--az-text);
            font-size: 1.08rem;
            font-weight: 900;
        }

        .score-pill {
            padding: 0.46rem 0.72rem;
            background: linear-gradient(135deg, var(--az-primary-soft), var(--az-accent-soft));
            color: var(--az-primary-dark);
            font-size: 0.84rem;
        }

        .small-muted {
            color: var(--az-muted);
            font-size: 0.91rem;
            line-height: 1.6;
        }

        .result-card p {
            margin: 0.45rem 0 0 0;
            color: #344054;
            line-height: 1.62;
            font-size: 0.94rem;
        }

        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, var(--az-primary), var(--az-accent));
        }

        /* -----------------------------
           사이드바
        ----------------------------- */
        section[data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, rgba(239, 248, 255, 0.96), rgba(242, 251, 249, 0.94));
            border-right: 1px solid var(--az-border);
        }

        section[data-testid="stSidebar"] > div:first-child {
            padding: 1.65rem 1.05rem 2rem 1.05rem;
        }

        .sidebar-brand {
            padding: 0.2rem 0.2rem 0.6rem 0.2rem;
        }

        .sidebar-brand-title {
            margin: 0;
            color: var(--az-text);
            font-size: 1.18rem;
            font-weight: 920;
            letter-spacing: -0.045em;
        }

        .sidebar-brand-caption {
            margin: 0.35rem 0 0 0;
            color: var(--az-muted);
            font-size: 0.76rem;
            line-height: 1.45;
        }

        .sidebar-user-card {
            margin: 1rem 0 0.8rem 0;
            padding: 0.95rem;
            border-radius: 20px;
            background: rgba(255,255,255,0.70);
            border: 1px solid var(--az-border);
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
        }

        .sidebar-user-label {
            margin: 0;
            color: var(--az-muted);
            font-size: 0.75rem;
            font-weight: 800;
        }

        .sidebar-user-name {
            margin: 0.32rem 0 0 0;
            color: var(--az-text);
            font-size: 0.98rem;
            font-weight: 900;
        }

        section[data-testid="stSidebar"] .stButton > button {
            border-radius: 14px !important;
            min-height: 2.78rem;
            justify-content: flex-start;
        }

        /* -----------------------------
           앱 내부 고정 내비게이션
           - Streamlit 기본 사이드바의 접힘 상태나 브라우저 저장 상태와 무관하게
             로그인 후 좌측 메뉴가 항상 보이도록 메인 레이아웃 안에 렌더링합니다.
        ----------------------------- */
        .app-sidebar-shell {
            position: sticky;
            top: 1rem;
            padding: 1.1rem;
            border-radius: var(--az-radius-lg);
            background: linear-gradient(180deg, rgba(239, 248, 255, 0.96), rgba(242, 251, 249, 0.94));
            border: 1px solid var(--az-border);
            box-shadow: var(--az-shadow-md);
            backdrop-filter: blur(14px);
        }

        .app-sidebar-divider {
            height: 1px;
            background: rgba(148, 163, 184, 0.22);
            margin: 0.85rem 0;
        }

        .sidebar-status-card {
            margin-top: 1rem;
        }

        .sidebar-stat-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.55rem;
            margin-top: 0.9rem;
        }

        .sidebar-stat-card {
            padding: 0.72rem 0.75rem;
            border-radius: 16px;
            background: linear-gradient(180deg, rgba(255,255,255,0.92), rgba(248,252,255,0.75));
            border: 1px solid rgba(148, 163, 184, 0.14);
        }

        .sidebar-stat-card span {
            display: block;
            color: var(--az-muted);
            font-size: 0.72rem;
            font-weight: 800;
        }

        .sidebar-stat-card strong {
            display: block;
            margin-top: 0.28rem;
            color: var(--az-text);
            font-size: 1rem;
            font-weight: 900;
            letter-spacing: -0.03em;
        }

        /* -----------------------------
           삭제 확인 영역
        ----------------------------- */
        .danger-zone-card {
            padding: 1rem 1.05rem;
            border-radius: 20px;
            background: rgba(255, 244, 246, 0.72);
            border: 1px solid rgba(239, 68, 68, 0.18);
        }

        .danger-zone-title {
            margin: 0;
            color: #9F1239;
            font-size: 1rem;
            font-weight: 900;
            letter-spacing: -0.025em;
        }

        .danger-zone-desc {
            margin: 0.42rem 0 0 0;
            color: #667085;
            font-size: 0.9rem;
            line-height: 1.58;
        }

        /* -----------------------------
           모바일 대응
        ----------------------------- */
        @media screen and (max-width: 768px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
                padding-top: 1.25rem;
            }

            .login-hero-logo {
                width: 250px;
                max-width: 78vw;
            }

            .login-top-copy {
                margin-bottom: 1.1rem;
            }

            .login-top-copy p {
                font-size: 0.94rem;
            }

            .login-feature-panel {
                padding: 1.05rem;
                border-radius: 22px;
            }

            .feature-row {
                gap: 0.8rem;
            }

            .medical-hero {
                padding: 1.25rem;
                border-radius: 22px;
            }

            .profile-grid {
                grid-template-columns: 1fr;
                padding: 0.75rem;
            }

            .profile-card {
                min-height: 72px;
            }

            .patient-table-header {
                display: none;
            }

            .patient-row-content {
                min-height: 3.6rem;
            }

            .patient-result-bar {
                align-items: flex-start;
                flex-direction: column;
            }

            .sidebar-stat-grid {
                grid-template-columns: 1fr;
            }

            .patient-list-bottom-spacer {
                min-height: 1rem;
            }
        }


        /* -----------------------------
           로그인 첫 화면 리디자인 override
           - 로그인 이후 화면에는 영향을 주지 않도록 login-* 클래스 중심으로만 적용합니다.
        ----------------------------- */
        .login-page-head {
            max-width: 1160px;
            margin: -0.25rem auto 1.15rem auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
        }

        .login-brand-lockup {
            display: inline-flex;
            align-items: center;
            gap: 0.85rem;
            padding: 0.52rem 0.82rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.58);
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.05);
            backdrop-filter: blur(14px);
        }

        .login-brand-lockup .login-hero-logo {
            width: 176px;
            max-width: 36vw;
            margin: 0;
            filter: drop-shadow(0 8px 16px rgba(10, 110, 189, 0.10));
        }

        .login-fallback-logo {
            width: 220px;
            max-width: min(56vw, 300px);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.6rem;
            padding: 0.68rem 0.8rem;
            border-radius: 24px;
            margin: 0 auto 0.85rem auto;
            background: linear-gradient(135deg, rgba(255,255,255,0.86), rgba(234,249,247,0.76));
            border: 1px solid rgba(11, 111, 184, 0.12);
            box-shadow: 0 14px 32px rgba(15, 23, 42, 0.08);
        }

        .login-brand-lockup .login-fallback-logo {
            width: auto !important;
            margin: 0;
            padding: 0;
            border: 0;
            background: transparent;
            box-shadow: none;
        }

        .fallback-logo-mark {
            width: 42px;
            height: 42px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 16px;
            background: linear-gradient(135deg, #E9F5FF, #EAF9F7);
            box-shadow: inset 0 0 0 1px rgba(11,111,184,0.08);
            font-size: 1.25rem;
        }

        .fallback-logo-text {
            display: inline-flex;
            flex-direction: column;
            line-height: 1.08;
        }

        .fallback-logo-text strong {
            color: var(--az-text);
            font-size: 1.05rem;
            font-weight: 950;
            letter-spacing: -0.04em;
        }

        .fallback-logo-text em {
            color: var(--az-accent);
            font-size: 0.88rem;
            font-style: normal;
            font-weight: 900;
            letter-spacing: -0.02em;
        }

        .login-brand-meta {
            display: flex;
            flex-direction: column;
            gap: 0.12rem;
        }

        .login-brand-meta strong {
            color: var(--az-text);
            font-size: 0.95rem;
            font-weight: 950;
            letter-spacing: -0.03em;
        }

        .login-brand-meta span {
            color: var(--az-muted);
            font-size: 0.74rem;
            font-weight: 750;
        }

        .login-screen-note {
            display: inline-flex;
            align-items: center;
            gap: 0.42rem;
            padding: 0.62rem 0.9rem;
            border-radius: 999px;
            color: #34506A;
            background: rgba(255, 255, 255, 0.56);
            border: 1px solid rgba(148, 163, 184, 0.16);
            font-size: 0.78rem;
            font-weight: 850;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.045);
            backdrop-filter: blur(12px);
        }

        .login-main-copy {
            position: relative;
            overflow: hidden;
            min-height: 548px;
            padding: clamp(1.45rem, 2.9vw, 2.55rem);
            border-radius: 36px;
            border: 1px solid rgba(255,255,255,0.72);
            background:
                radial-gradient(circle at 15% 8%, rgba(255,255,255,0.96), transparent 26%),
                radial-gradient(circle at 90% 13%, rgba(44,184,175,0.20), transparent 32%),
                linear-gradient(135deg, rgba(255,255,255,0.92) 0%, rgba(239,248,255,0.82) 46%, rgba(235,250,248,0.78) 100%);
            box-shadow: 0 30px 80px rgba(15, 23, 42, 0.10);
            backdrop-filter: blur(18px);
        }

        .login-main-copy::before {
            content: "";
            position: absolute;
            width: 300px;
            height: 300px;
            right: -120px;
            top: -112px;
            border-radius: 999px;
            background: linear-gradient(135deg, rgba(11,111,184,0.18), rgba(44,184,175,0.18));
        }

        .login-main-copy::after {
            content: "";
            position: absolute;
            width: 190px;
            height: 190px;
            right: 58px;
            bottom: 44px;
            border-radius: 999px;
            background: rgba(255,255,255,0.48);
            border: 1px solid rgba(255,255,255,0.70);
        }

        .login-main-copy > * {
            position: relative;
            z-index: 1;
        }

        .login-main-copy .login-badge {
            margin-bottom: 1.08rem;
            padding: 0.48rem 0.86rem;
            background: linear-gradient(135deg, rgba(11,111,184,0.10), rgba(44,184,175,0.10));
            border-color: rgba(11,111,184,0.16);
            color: var(--az-primary-dark);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.72);
        }

        .login-main-copy h1 {
            margin: 0;
            color: var(--az-text);
            font-size: clamp(2.35rem, 4.8vw, 4.35rem);
            line-height: 1.04;
            font-weight: 950;
            letter-spacing: -0.072em;
        }

        .login-main-copy h1 span {
            display: inline-block;
            color: transparent;
            background: linear-gradient(135deg, #0B6FB8 0%, #2CB8AF 80%);
            -webkit-background-clip: text;
            background-clip: text;
        }

        .login-main-copy .login-lead {
            max-width: 640px;
            margin: 1rem 0 0 0;
            color: #4B6278;
            font-size: 1.05rem;
            line-height: 1.78;
            word-break: keep-all;
        }

        .login-stat-strip {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.74rem;
            max-width: 680px;
            margin-top: 1.55rem;
        }

        .login-stat {
            min-height: 92px;
            padding: 0.95rem 1rem;
            border-radius: 22px;
            background: rgba(255,255,255,0.70);
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow: 0 10px 26px rgba(15, 23, 42, 0.045);
        }

        .login-stat span {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 30px;
            height: 30px;
            border-radius: 12px;
            color: var(--az-primary-dark);
            background: linear-gradient(135deg, var(--az-primary-soft), var(--az-accent-soft));
            font-size: 0.78rem;
            font-weight: 950;
        }

        .login-stat strong {
            display: block;
            margin-top: 0.55rem;
            color: var(--az-text);
            font-size: 0.96rem;
            font-weight: 920;
            letter-spacing: -0.035em;
        }

        .login-stat p {
            margin: 0.22rem 0 0 0;
            color: var(--az-muted);
            font-size: 0.78rem;
            line-height: 1.42;
        }

        .login-feature-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.82rem;
            max-width: 680px;
            margin-top: 0.9rem;
        }

        .login-feature-card {
            display: flex;
            gap: 0.72rem;
            align-items: flex-start;
            padding: 0.86rem 0.9rem;
            border-radius: 20px;
            background: rgba(255,255,255,0.54);
            border: 1px solid rgba(148, 163, 184, 0.14);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.65);
        }

        .login-feature-icon {
            width: 38px;
            min-width: 38px;
            height: 38px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 15px;
            background: linear-gradient(135deg, rgba(233,245,255,0.95), rgba(234,249,247,0.92));
            box-shadow: inset 0 0 0 1px rgba(11, 111, 184, 0.06);
            font-size: 1.06rem;
        }

        .login-feature-card b {
            display: block;
            color: var(--az-text);
            font-size: 0.9rem;
            font-weight: 920;
            letter-spacing: -0.03em;
        }

        .login-feature-card p {
            margin: 0.24rem 0 0 0;
            color: var(--az-muted);
            font-size: 0.78rem;
            line-height: 1.45;
            word-break: keep-all;
        }

        .login-auth-eyebrow {
            margin: 0 0 0.8rem 0;
            padding: 0.68rem 0.82rem;
            border-radius: 18px;
            text-align: center;
            color: var(--az-primary-dark);
            background: rgba(255,255,255,0.58);
            border: 1px solid rgba(11, 111, 184, 0.10);
            font-size: 0.8rem;
            font-weight: 900;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.04);
            backdrop-filter: blur(12px);
        }

        .login-card-head {
            margin-bottom: 1.25rem;
        }

        .login-card-title {
            font-size: 1.72rem;
            letter-spacing: -0.055em;
        }

        .login-card-subtitle {
            color: #5A6B7D;
            word-break: keep-all;
        }

        .login-helper {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.36rem;
            padding: 0.62rem 0.74rem;
            border-radius: 999px;
            background: rgba(248, 250, 252, 0.86);
            border: 1px solid rgba(148, 163, 184, 0.14);
            color: #687789;
            font-weight: 800;
        }

        .login-card-footer-note {
            margin-top: 0.9rem;
            color: var(--az-muted-light);
            text-align: center;
            font-size: 0.78rem;
            font-weight: 750;
        }

        .signup-cta-copy {
            background: linear-gradient(135deg, rgba(233,245,255,0.82), rgba(234,249,247,0.74));
        }

        @media screen and (max-width: 1024px) {
            .login-page-head {
                align-items: flex-start;
                flex-direction: column;
                max-width: 760px;
            }

            .login-main-copy {
                min-height: auto;
            }

            .login-stat-strip,
            .login-feature-grid {
                max-width: none;
            }
        }

        @media screen and (max-width: 768px) {
            .login-page-head {
                margin-top: 0;
                margin-bottom: 0.9rem;
            }

            .login-screen-note {
                width: 100%;
                justify-content: center;
            }

            .login-brand-lockup {
                width: 100%;
                justify-content: center;
            }

            .login-brand-lockup .login-hero-logo {
                width: 148px;
                max-width: 54vw;
            }

            .login-main-copy {
                padding: 1.2rem;
                border-radius: 26px;
            }

            .login-main-copy h1 {
                font-size: clamp(2.05rem, 11vw, 3rem);
            }

            .login-stat-strip,
            .login-feature-grid {
                grid-template-columns: 1fr;
            }

            .login-stat {
                min-height: auto;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def show_hero(title, subtitle):
    """페이지 상단 타이틀 영역을 표시합니다."""
    st.markdown(
        f"""
        <div class="medical-hero">
            <div class="hero-kicker">Alz' Zip Clinical Workspace</div>
            <h1>{safe_text(title)}</h1>
            <p>{safe_text(subtitle)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title, description=None, kicker=None):
    """섹션 타이틀을 일관된 스타일로 표시합니다."""
    kicker_html = f'<div class="section-kicker">{safe_text(kicker)}</div>' if kicker else ""
    description_html = f'<p class="section-desc">{safe_text(description)}</p>' if description else ""
    st.markdown(
        f"""
        <div class="section-title-row">
            <div>
                {kicker_html}
                <h3 class="section-title">{safe_text(title)}</h3>
                {description_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_patient_profile_cards(patient):
    """환자 기본 정보를 하나의 요약 패널로 표시합니다."""
    # Streamlit markdown이 들여쓰기/빈 줄을 코드블록으로 해석하지 않도록 HTML을 한 문자열로 조립합니다.
    profile_html = (
        f'<div class="profile-grid">'
        f'<div class="profile-card"><div class="profile-icon">👤</div><div>'
        f'<p class="profile-label">이름</p>'
        f'<p class="profile-value">{safe_text(patient["name"])}</p>'
        f'</div></div>'
        f'<div class="profile-card"><div class="profile-icon">🔵</div><div>'
        f'<p class="profile-label">생년월일</p>'
        f'<p class="profile-value">{safe_text(format_date(patient["birthdate"]))}</p>'
        f'</div></div>'
        f'<div class="profile-card"><div class="profile-icon">🔵</div><div>'
        f'<p class="profile-label">성별</p>'
        f'<p class="profile-value">{safe_text(patient["gender"])}</p>'
        f'</div></div>'
        f'<div class="profile-card"><div class="profile-icon">🔵</div><div>'
        f'<p class="profile-label">학력 사항</p>'
        f'<p class="profile-value">{safe_text(patient["education"])}</p>'
        f'</div></div>'
        f'</div>'
    )
    st.markdown(profile_html, unsafe_allow_html=True)


def get_patient_by_id(patient_id):
    """환자 ID로 session_state의 환자 정보를 조회합니다."""
    for patient in st.session_state["patients"]:
        if patient["id"] == patient_id:
            return patient
    return None


def navigate(page, patient_id=None, clear_latest_result=True):
    """화면 이동을 처리합니다."""
    st.session_state["page"] = page

    if patient_id is not None:
        st.session_state["selected_patient_id"] = patient_id

    if clear_latest_result:
        st.session_state["latest_diagnosis_result"] = None
        st.session_state["latest_diagnosis_patient_id"] = None

    st.session_state["delete_confirm_patient_id"] = None

    st.rerun()


# -----------------------------
# 1. 세션 상태 초기화
# -----------------------------
def init_session_state():
    """로그인 상태, 환자 목록, 화면 상태를 초기화합니다."""
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if "page" not in st.session_state:
        st.session_state["page"] = "login"

    if "auth_page" not in st.session_state:
        # 로그인 전 인증 화면 전용 상태입니다.
        # 로그인 화면과 계정 생성 화면을 분리해 오른쪽 패널만 길어지는 문제를 방지합니다.
        st.session_state["auth_page"] = "login"

    if "selected_patient_id" not in st.session_state:
        st.session_state["selected_patient_id"] = None

    if "login_success_flash" not in st.session_state:
        st.session_state["login_success_flash"] = False

    if "patient_added_flash" not in st.session_state:
        st.session_state["patient_added_flash"] = False

    if "patient_updated_flash" not in st.session_state:
        st.session_state["patient_updated_flash"] = False

    if "patient_deleted_flash" not in st.session_state:
        st.session_state["patient_deleted_flash"] = False

    if "delete_confirm_patient_id" not in st.session_state:
        st.session_state["delete_confirm_patient_id"] = None

    if "latest_diagnosis_result" not in st.session_state:
        st.session_state["latest_diagnosis_result"] = None

    if "latest_diagnosis_patient_id" not in st.session_state:
        st.session_state["latest_diagnosis_patient_id"] = None

    if "accounts" not in st.session_state:
        # 데모용 계정 저장소입니다. 실제 서비스에서는 DB와 암호화 저장소로 교체하세요.
        st.session_state["accounts"] = {
            "demo": {
                "password": "demo",
                "name": "데모 의료진",
                "clinician_code": "DEMO-0000",
                "approved": True,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        }

    if "current_user" not in st.session_state:
        st.session_state["current_user"] = None

    if "signup_code_approved" not in st.session_state:
        st.session_state["signup_code_approved"] = False

    if "signup_code_last_value" not in st.session_state:
        st.session_state["signup_code_last_value"] = ""

    if "account_created_flash" not in st.session_state:
        st.session_state["account_created_flash"] = False

    if "signup_success_account_id" not in st.session_state:
        st.session_state["signup_success_account_id"] = ""

    if "patients" not in st.session_state:
        # 초기 데모용 샘플 환자 3명
        st.session_state["patients"] = [
            {
                "id": "P-001",
                "name": "정민호",
                "birthdate": date(1949, 5, 10),
                "gender": "남성",
                "education": "고",
                "diagnosis_history": [],
            },
            {
                "id": "P-002",
                "name": "한영숙",
                "birthdate": date(1952, 9, 24),
                "gender": "여성",
                "education": "중",
                "diagnosis_history": [],
            },
            {
                "id": "P-003",
                "name": "오순자",
                "birthdate": date(1946, 1, 18),
                "gender": "여성",
                "education": "저",
                "diagnosis_history": [],
            },
        ]


# -----------------------------
# 2. 로그인 화면
# -----------------------------
def get_logo_html(width=310):
    """로그인 상단에 표시할 로고 이미지를 HTML img 태그로 반환합니다."""
    if not LOGO_PATH.exists():
        return (
            f'<div class="login-fallback-logo" style="width:{width}px">'
            f'<span class="fallback-logo-mark">🐣</span>'
            f"<span class=\"fallback-logo-text\"><strong>알집</strong><em>Alz' Zip</em></span>"
            f'</div>'
        )

    logo_base64 = base64.b64encode(LOGO_PATH.read_bytes()).decode("utf-8")
    return (
        f'<img class="login-hero-logo" src="data:image/png;base64,{logo_base64}" '
        f'width="{width}" alt="알집 Alz Zip 로고" />'
    )


def authenticate_account(account_id, password):
    """세션에 저장된 승인 계정으로 로그인합니다."""
    account_id = account_id.strip()

    if not account_id or not password:
        return False, "아이디와 비밀번호를 모두 입력해 주세요."

    account = st.session_state["accounts"].get(account_id)

    if account is None:
        return False, "등록된 계정을 찾을 수 없습니다. 계정 생성 후 다시 시도해 주세요."

    if not account.get("approved"):
        return False, "의료진 코드 승인이 완료되지 않은 계정입니다."

    if account.get("password") != password:
        return False, "비밀번호가 올바르지 않습니다."

    st.session_state["current_user"] = {
        "id": account_id,
        "name": account.get("name", account_id),
        "clinician_code": account.get("clinician_code", ""),
    }
    return True, ""


def create_clinician_account(account_id, password, name, clinician_code):
    """프로토타입용 계정을 session_state에 저장합니다."""
    account_id = account_id.strip()
    st.session_state["accounts"][account_id] = {
        "password": password,
        "name": name.strip(),
        "clinician_code": clinician_code.strip(),
        "approved": True,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def render_login_panel():
    """승인된 의료진 계정으로 로그인하는 패널입니다."""
    st.markdown(
        """
        <div class="login-card-head">
            <h2 class="login-card-title">의료진 로그인</h2>
            <p class="login-card-subtitle">로그인을 통해 환자 워크스페이스에 접근하세요.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.get("account_created_flash"):
        created_id = st.session_state.get("signup_success_account_id", "")
        st.success(f"{created_id} 계정이 생성되었습니다. 생성한 계정으로 로그인해 주세요.")
        st.session_state["account_created_flash"] = False

    with st.form("login_form"):
        account_id = st.text_input("아이디", placeholder=" ", key="login_account_id")
        password = st.text_input("비밀번호", type="password", placeholder=" ", key="login_password")
        submitted = st.form_submit_button(
            "로그인",
            use_container_width=True,
            type="primary",
        )

    if submitted:
        success, message = authenticate_account(account_id, password)
        if not success:
            st.warning(message)
        else:
            st.session_state["logged_in"] = True
            st.session_state["page"] = "main"
            st.session_state["auth_page"] = "login"
            st.session_state["login_success_flash"] = True
            st.rerun()

    st.markdown('<div class="auth-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="signup-cta-copy">
            <strong>처음 접속하는 의료진인가요?</strong>
            <span>의료진 코드를 인증 받아, 계정을 생성하세요.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("의료진 계정 생성하기", use_container_width=True, key="go_to_signup_page"):
        st.session_state["auth_page"] = "signup"
        st.session_state["signup_code_approved"] = False
        st.session_state["signup_code_last_value"] = ""
        st.rerun()


def render_signup_panel():
    """별도 계정 생성 화면 안에서 단계형 회원가입 폼을 표시합니다."""
    is_approved = st.session_state.get("signup_code_approved", False)

    if not is_approved:
        st.markdown(
            """
            <div class="signup-step-head">
                <div class="signup-step-badge">1</div>
                <div>
                    <p class="signup-step-title">의료진 코드 승인</p>
                    <p class="signup-step-desc">먼저 의료진 코드를 확인합니다. 승인 후 계정 정보 입력 단계가 열립니다.</p>
                </div>
            </div>
            <div class="auth-mode-note">
                의료진 승인 코드는 관리자 요청을 통해 발급 받을 수 있습니다.
            </div>
            """,
            unsafe_allow_html=True,
        )

        clinician_code = st.text_input(
            "의료진 코드",
            placeholder="예: MED-2026-CHA",
            key="signup_clinician_code",
            help="프로토타입에서는 승인 버튼 클릭 시 어떤 코드든 승인됩니다.",
        )

        approval_col, status_col = st.columns([0.42, 0.58], vertical_alignment="center")
        show_code_warning = False

        with approval_col:
            if st.button("의료진 코드 승인", use_container_width=True, type="primary", key="approve_clinician_code"):
                if not clinician_code.strip():
                    show_code_warning = True
                else:
                    st.session_state["signup_code_approved"] = True
                    st.session_state["signup_code_last_value"] = clinician_code.strip()
                    st.rerun()

        with status_col:
            st.markdown(
                """
                <div class="approval-status-card pending">
                    <div class="approval-status-icon">✓</div>
                    <div class="approval-status-body">
                        <p class="approval-status-title">승인 대기</p>
                        <p class="approval-status-desc">코드 승인 후 계정 정보를 입력합니다.</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if show_code_warning:
            st.warning("의료진 코드를 입력한 뒤 승인해 주세요.")

        return

    approved_code = st.session_state.get("signup_code_last_value", "")

    st.markdown(
        f"""
        <div class="signup-step-head">
            <div class="signup-step-badge">2</div>
            <div>
                <p class="signup-step-title">계정 정보 입력</p>
                <p class="signup-step-desc">승인된 코드로 로그인 계정을 생성합니다.</p>
            </div>
        </div>
        <div class="approval-status-card approved">
            <div class="approval-status-icon">✓</div>
            <div class="approval-status-body">
                <p class="approval-status-title">의료진 코드 승인 완료</p>
                <p class="approval-status-desc">승인 코드 · {safe_text(approved_code)}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    reset_col, spacer_col = st.columns([0.42, 0.58])
    with reset_col:
        if st.button("코드 다시 입력", use_container_width=True, key="reset_signup_code"):
            st.session_state["signup_code_approved"] = False
            st.session_state["signup_code_last_value"] = ""
            st.rerun()

    name_col, id_col = st.columns([1, 1])
    with name_col:
        clinician_name = st.text_input(
            "의료진 이름",
            placeholder=" ",
            key="signup_clinician_name",
        )
    with id_col:
        account_id = st.text_input(
            "새 아이디",
            placeholder=" ",
            key="signup_account_id",
        )

    pw_col, pw_confirm_col = st.columns([1, 1])
    with pw_col:
        password = st.text_input(
            "새 비밀번호",
            type="password",
            placeholder=" ",
            key="signup_password",
        )
    with pw_confirm_col:
        password_confirm = st.text_input(
            "비밀번호 확인",
            type="password",
            placeholder=" ",
            key="signup_password_confirm",
        )

    if st.button("계정 생성", use_container_width=True, type="primary", key="create_clinician_account"):
        normalized_account_id = account_id.strip()

        if not clinician_name.strip():
            st.warning("의료진 이름을 입력해 주세요.")
            return

        if not normalized_account_id:
            st.warning("로그인에 사용할 아이디를 입력해 주세요.")
            return

        if normalized_account_id in st.session_state["accounts"]:
            st.warning("이미 사용 중인 아이디입니다. 다른 아이디를 입력해 주세요.")
            return

        if not password:
            st.warning("비밀번호를 입력해 주세요.")
            return

        if password != password_confirm:
            st.warning("비밀번호 확인이 일치하지 않습니다.")
            return

        create_clinician_account(
            normalized_account_id,
            password,
            clinician_name,
            approved_code,
        )
        st.session_state["account_created_flash"] = True
        st.session_state["signup_success_account_id"] = normalized_account_id
        st.session_state["signup_code_approved"] = False
        st.session_state["signup_code_last_value"] = ""
        st.session_state["auth_page"] = "login"
        st.rerun()


def signup_page():
    """로그인 화면과 분리된 의료진 계정 생성 전용 화면입니다."""
    logo_html = get_logo_html(width=250)

    st.markdown(
        f"""
        <div class="signup-page-copy">
            {logo_html}
            <div class="login-badge">의료진 인증 플로우</div>
            <h1>의료진 계정 생성</h1>
            <p>
                  의료진 인증과 계정 생성을<br/>
                  안전한 단계별 절차에 따라 진행합니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    outer_left, center, outer_right = st.columns([0.28, 0.44, 0.28])

    with center:
        if st.button("← 로그인으로 돌아가기", use_container_width=True, key="back_to_login_page"):
            st.session_state["auth_page"] = "login"
            st.session_state["signup_code_approved"] = False
            st.session_state["signup_code_last_value"] = ""
            st.rerun()

        with st.container(border=True):
            render_signup_panel()


def login_page():
    """로그인 전 인증 화면입니다. 로그인과 계정 생성을 별도 화면으로 분리합니다."""
    if st.session_state.get("auth_page") == "signup":
        signup_page()
        return

    logo_html = get_logo_html()

    # Streamlit의 markdown 파서가 들여쓰기된 HTML을 코드블록으로 표시하는 문제를 막기 위해
    # 로그인 첫 화면 HTML은 한 줄 문자열 조합으로 렌더링합니다.
    header_html = (
        '<div class="login-page-head">'
        '<div class="login-brand-lockup">'
        f'{logo_html}'
        '<div class="login-brand-meta">'
        '<strong>Alz\' Zip Clinical</strong>'
        '<span>AI 기반 알츠하이머 진단 지원</span>'
        '</div>'
        '</div>'
        '<div class="login-screen-note">의료진 전용 접속</div>'
        '</div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)

    outer_left, center, outer_right = st.columns([0.03, 0.94, 0.03])

    with center:
        left, right = st.columns([1.18, 0.82], gap="large", vertical_alignment="center")

        with left:
            hero_html = (
                '<section class="login-main-copy">'
                '<div class="login-badge">알츠하이머 진단 의사결정 지원 시스템</div>'
                '<h1>기억을 지키는<br/><span>따뜻한 진단 동반자</span></h1>'
                '<p class="login-lead">'
                '환자 정보 조회부터 유사 사례 확인, 진단 기록 관리까지 '
                '하나의 흐름으로 연결해 의료진이 빠르게 진단에 집중할 수 있도록 설계했습니다.'
                '</p>'
                '<div class="login-stat-strip">'
                '<div class="login-stat">'
                '<span>01</span>'
                '<strong>환자 프로필 기반</strong>'
                '<p>기본 정보와 진단 이력을 한 곳에서 확인합니다.</p>'
                '</div>'
                '<div class="login-stat">'
                '<span>02</span>'
                '<strong>유사 사례 매칭</strong>'
                '<p>근거를 기반으로 유사한 환자를 추천하여 제공합니다.</p>'
                '</div>'
                '<div class="login-stat">'
                '<span>03</span>'
                '<strong>의료진 인증</strong>'
                '<p>승인된 계정으로 안전하게 환자 정보를 관리합니다.</p>'
                '</div>'
                '</div>'
                '<div class="login-feature-grid">'
                '<div class="login-feature-card">'
                '<div class="login-feature-icon">🧠</div>'
                '<div><b>AI 유사 환자군 매칭</b><p>환자 프로필을 바탕으로 유사 환자군을 추천합니다.</p></div>'
                '</div>'
                '<div class="login-feature-card">'
                '<div class="login-feature-icon">🩺</div>'
                '<div><b>의료진 중심 워크플로우</b><p>환자 이력과 진단 결과를 체계적으로 관리합니다.</p></div>'
                '</div>'
                '<div class="login-feature-card">'
                '<div class="login-feature-icon">📁</div>'
                '<div><b>의료 데이터 관리</b><p>fMRI 등 의료 데이터 입력 및 관리를 지원합니다.</p></div>'
                '</div>'
                '<div class="login-feature-card">'
                '<div class="login-feature-icon">🔒</div>'
                '<div><b>승인 계정 접속</b><p>의료진 코드 인증 후 개인 계정을 생성합니다.</p></div>'
                '</div>'
                '</div>'
                '</section>'
            )
            st.markdown(hero_html, unsafe_allow_html=True)

        with right:
            st.markdown(
                '<div class="login-auth-eyebrow">Authorized Clinician Workspace</div>',
                unsafe_allow_html=True,
            )
            with st.container(border=True):
                render_login_panel()
            st.markdown(
                '<div class="login-card-footer-note">제공되는 정보는 전문의의 의학적 진단을 대체할 수 없습니다.</div>',
                unsafe_allow_html=True,
            )

# -----------------------------
# 3. 메인 화면: 환자 목록
# -----------------------------
def main_page():
    """로그인 후 환자 목록을 표시합니다."""
    show_hero(
        "환자 목록",
        "등록된 환자의 상세 정보를 확인하거나 AI 기반 유사 사례 매칭 진단을 실행할 수 있습니다.",
    )

    if st.session_state.get("patient_added_flash"):
        st.success("새 환자 프로필이 환자 목록에 추가되었습니다.")
        st.session_state["patient_added_flash"] = False

    if st.session_state.get("patient_deleted_flash"):
        st.success("환자 프로필이 삭제되었습니다.")
        st.session_state["patient_deleted_flash"] = False

    top_left, top_right = st.columns([3, 1], vertical_alignment="center")
    with top_left:
        section_title("등록 환자", "환자별 상세 정보와 진단 실행을 빠르게 선택할 수 있습니다.", "Patient Registry")
    with top_right:
        st.write("")
        if st.button("＋ 프로필 추가", use_container_width=True, type="primary", key="main_add_patient_button"):
            navigate("add_patient")

    patients = st.session_state["patients"]

    if not patients:
        st.info("등록된 환자가 없습니다. 프로필 추가 버튼으로 환자를 등록해 주세요.")
        return

    with st.container(border=True):
        search_col, sort_col = st.columns([2, 1], vertical_alignment="top")

        with search_col:
            st.markdown(
                '<div class="patient-toolbar-label">환자 이름 검색</div>',
                unsafe_allow_html=True,
            )
            search_keyword = st.text_input(
                "환자 이름 검색",
                placeholder=" ",
                key="patient_name_search",
                label_visibility="collapsed",
            )

        with sort_col:
            st.markdown(
                '<div class="patient-toolbar-label">정렬 기준</div>',
                unsafe_allow_html=True,
            )
            sort_option = st.selectbox(
                "정렬 기준",
                ["이름 가나다순", "생년월일 순", "성별 순"],
                key="patient_sort_option",
                label_visibility="collapsed",
            )

    keyword = search_keyword.strip().casefold()
    filtered_patients = [
        patient for patient in patients
        if not keyword or keyword in str(patient.get("name", "")).casefold()
    ]

    if sort_option == "이름 가나다순":
        filtered_patients = sorted(filtered_patients, key=lambda patient: patient.get("name", ""))
    elif sort_option == "생년월일 순":
        filtered_patients = sorted(
            filtered_patients,
            key=lambda patient: parse_date_value(patient.get("birthdate")),
        )
    elif sort_option == "성별 순":
        filtered_patients = sorted(
            filtered_patients,
            key=lambda patient: (patient.get("gender", ""), patient.get("name", "")),
        )

    st.markdown(
        f"""
        <div class="patient-result-bar">
            <div class="patient-result-pill">검색 결과 <strong>{len(filtered_patients)}명</strong></div>
            <div class="patient-result-meta">전체 {len(patients)}명 · 현재 정렬 {safe_text(sort_option)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not filtered_patients:
        st.info("검색 조건에 맞는 환자가 없습니다. 이름 검색어를 다시 확인해 주세요.")
        return

    st.markdown(
        """
        <div class="patient-table-header">
            <div>이름</div>
            <div>생년월일</div>
            <div>성별</div>
            <div>관리</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for patient in filtered_patients:
        with st.container(border=True):
            cols = st.columns([1.55, 1.25, 0.85, 0.72, 0.72], vertical_alignment="center")
            cols[0].markdown(
                f"""
                <div class="patient-row-content">
                    <div class="patient-name-row">
                        <div class="patient-name">{safe_text(patient['name'])}</div>
                        <span class="patient-history-pill">진단 이력 {len(patient.get('diagnosis_history', []))}건</span>
                    </div>
                    <div class="patient-id">환자 ID · {safe_text(patient['id'])}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            cols[1].markdown(
                f"<span class='info-pill'>{safe_text(format_date(patient['birthdate']))}</span>",
                unsafe_allow_html=True,
            )
            cols[2].markdown(
                f"<span class='gender-pill'>{safe_text(patient['gender'])}</span>",
                unsafe_allow_html=True,
            )

            if cols[3].button("상세 보기", key=f"detail_{patient['id']}", use_container_width=True):
                navigate("patient_detail", patient["id"])

            if cols[4].button("AI 진단", key=f"diagnosis_{patient['id']}", use_container_width=True, type="primary"):
                navigate("ai_diagnosis", patient["id"])

    st.markdown('<div class="patient-list-bottom-spacer"></div>', unsafe_allow_html=True)


# -----------------------------
# 4. 프로필 추가 기능
# -----------------------------
def add_patient_form():
    """새 환자 정보를 입력받아 st.session_state['patients']에 저장합니다."""
    show_hero(
        "환자 프로필 추가",
        "기본 인적 사항과 학력 정보를 입력하여 데모 환자 목록에 등록합니다.",
    )

    if st.button("← 환자 목록으로 돌아가기", key="add_patient_back_to_main"):
        navigate("main")

    section_title("환자 기본 정보", "환자 식별에 필요한 기본 정보를 입력합니다.", "New Profile")

    with st.container(border=True):
        with st.form("add_patient_form"):
            name = st.text_input("이름", placeholder=" ")
            birthdate = st.date_input(
                "생년월일",
                value=date(1950, 1, 1),
                min_value=date(1900, 1, 1),
                max_value=date.today(),
            )
            gender = st.radio("성별", ["남성", "여성"], horizontal=True)
            education = st.selectbox("학력 사항", ["고", "중", "저"])

            submitted = st.form_submit_button("저장", use_container_width=True, type="primary")

    if submitted:
        if not name.strip():
            st.warning("이름을 입력해 주세요.")
            return

        new_patient = {
            "id": f"P-{uuid.uuid4().hex[:8].upper()}",
            "name": name.strip(),
            "birthdate": birthdate,
            "gender": gender,
            "education": education,
            "diagnosis_history": [],
        }

        st.session_state["patients"].append(new_patient)
        st.session_state["patient_added_flash"] = True
        navigate("main")


# -----------------------------
# 5. 환자 기본정보 수정 화면
# -----------------------------
def edit_patient_form():
    """선택된 환자의 기본 정보를 수정합니다."""
    patient_id = st.session_state.get("selected_patient_id")
    patient = get_patient_by_id(patient_id)

    if patient is None:
        st.error("수정할 환자를 찾을 수 없습니다.")
        if st.button("환자 목록으로 이동", key="not_found_back_to_main"):
            navigate("main")
        return

    show_hero(
        "환자 기본정보 수정",
        "등록된 환자의 이름, 생년월일, 성별, 학력 정보를 업데이트합니다.",
    )

    col_back, col_detail = st.columns([1, 1])
    with col_back:
        if st.button("← 환자 상세로 돌아가기", use_container_width=True, key=f"edit_back_detail_{patient['id']}"):
            navigate("patient_detail", patient["id"], clear_latest_result=False)
    with col_detail:
        if st.button("환자 목록", use_container_width=True, key="edit_back_to_main"):
            navigate("main")

    section_title("수정할 기본 정보", "저장하면 환자 목록과 상세 화면에 즉시 반영됩니다.", "Edit Profile")

    gender_options = ["남성", "여성"]
    education_options = ["고", "중", "저"]
    current_gender_index = gender_options.index(patient["gender"]) if patient.get("gender") in gender_options else 0
    current_education_index = (
        education_options.index(patient["education"]) if patient.get("education") in education_options else 0
    )

    with st.container(border=True):
        with st.form(f"edit_patient_form_{patient['id']}"):
            name = st.text_input("이름", value=patient.get("name", ""), placeholder=" ")
            birthdate = st.date_input(
                "생년월일",
                value=parse_date_value(patient.get("birthdate")),
                min_value=date(1900, 1, 1),
                max_value=date.today(),
            )
            gender = st.radio("성별", gender_options, index=current_gender_index, horizontal=True)
            education = st.selectbox("학력 사항", education_options, index=current_education_index)

            submitted = st.form_submit_button("변경사항 저장", use_container_width=True, type="primary")

    if submitted:
        if not name.strip():
            st.warning("이름을 입력해 주세요.")
            return

        updated = update_patient_profile(
            patient["id"],
            name=name.strip(),
            birthdate=birthdate,
            gender=gender,
            education=education,
        )

        if not updated:
            st.error("환자 정보를 수정하지 못했습니다.")
            return

        st.session_state["patient_updated_flash"] = True
        navigate("patient_detail", patient["id"], clear_latest_result=False)


# -----------------------------
# 6. 환자 상세 / 과거 이력 화면
# -----------------------------
def patient_detail_page():
    """선택된 환자의 상세 정보와 과거 진단 이력을 표시합니다."""
    patient_id = st.session_state.get("selected_patient_id")
    patient = get_patient_by_id(patient_id)

    if patient is None:
        st.error("선택된 환자를 찾을 수 없습니다.")
        if st.button("환자 목록으로 이동", key="not_found_back_to_main"):
            navigate("main")
        return

    show_hero(
        "환자 상세 정보",
        "환자의 기본 프로필과 과거 AI 진단 지원 이력을 확인합니다.",
    )

    if st.session_state.get("patient_updated_flash"):
        st.success("환자 기본정보가 수정되었습니다.")
        st.session_state["patient_updated_flash"] = False

    col_back, col_diag, col_edit, col_delete = st.columns([1, 1, 1, 1])
    with col_back:
        if st.button("← 환자 목록", use_container_width=True, key=f"diagnosis_back_main_{patient['id']}"):
            navigate("main")
    with col_diag:
        if st.button("AI 진단 실행", use_container_width=True, type="primary", key=f"detail_ai_diagnosis_{patient['id']}"):
            navigate("ai_diagnosis", patient["id"])
    with col_edit:
        if st.button("기본정보 수정", use_container_width=True, key=f"edit_profile_{patient['id']}"):
            navigate("edit_patient", patient["id"], clear_latest_result=False)
    with col_delete:
        if st.button("프로필 삭제", use_container_width=True, key=f"request_delete_{patient['id']}"):
            st.session_state["delete_confirm_patient_id"] = patient["id"]
            st.rerun()

    section_title("기본 정보", "선택된 환자의 핵심 프로필입니다.", "Patient Profile")
    render_patient_profile_cards(patient)

    if st.session_state.get("delete_confirm_patient_id") == patient["id"]:
        with st.container(border=True):
            st.markdown(
                f"""
                <div class="danger-zone-card">
                    <p class="danger-zone-title">프로필 삭제 확인</p>
                    <p class="danger-zone-desc">
                        {safe_text(patient['name'])} 환자 프로필을 삭제하면 기본 정보와 과거 진단 이력이 함께 제거됩니다.
                        데모 세션 안에서만 저장된 데이터이지만, 삭제 후에는 현재 화면에서 복구할 수 없습니다.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            confirm_delete = st.checkbox(
                "위 내용을 확인했으며 이 환자 프로필을 삭제합니다.",
                key=f"confirm_delete_{patient['id']}",
            )
            cancel_col, delete_col = st.columns([1, 1])
            with cancel_col:
                if st.button("삭제 취소", use_container_width=True, key=f"cancel_delete_{patient['id']}"):
                    st.session_state["delete_confirm_patient_id"] = None
                    st.rerun()
            with delete_col:
                if st.button("프로필 영구 삭제", use_container_width=True, key=f"delete_patient_{patient['id']}"):
                    if not confirm_delete:
                        st.warning("삭제 확인 체크박스를 먼저 선택해 주세요.")
                        return

                    deleted = delete_patient_profile(patient["id"])
                    if not deleted:
                        st.error("환자 프로필을 삭제하지 못했습니다.")
                        return

                    st.session_state["patient_deleted_flash"] = True
                    st.session_state["delete_confirm_patient_id"] = None
                    navigate("main")

    section_title("과거 진단 이력", "저장된 AI 진단 지원 결과를 시간순으로 확인합니다.", "History")

    history = patient.get("diagnosis_history", [])
    if not history:
        st.info("아직 진단 이력이 없습니다.")
        return

    # 최신 진단이 위로 오도록 역순 출력
    for idx, record in enumerate(reversed(history), start=1):
        with st.expander(f"{idx}. 진단 일시: {record['diagnosis_datetime']}", expanded=(idx == 1)):
            mmse_score = record.get("mmse_score")
            mmse_text = f"{mmse_score}/30" if mmse_score is not None else "기록 없음"
            st.write(f"**MMSE 점수:** {mmse_text}")
            st.write(f"**입력 증상:** {', '.join(record['symptoms'])}")
            st.write(f"**fMRI 파일명:** {record['fmri_filename']}")

            similar_patients = record.get("similar_patients", [])
            if similar_patients:
                # [중요] 새로운 계층형 구조를 표(DataFrame)로 만들기 위한 평탄화 작업
                flat_data = []
                for p in similar_patients:
                    summary = p.get('summary', {})
                    symptoms = p.get('symptoms', {})
                    
                    flat_data.append({
                        "환자 ID": summary.get('ptid'),
                        "유사도": f"{summary.get('similarity')}%",
                        "매칭 시점": f"{summary.get('matched_month')}개월 차",
                        "보정 MMSE": summary.get('mmse'),
                        "학력": "고" if summary.get('edu_level') == 2 else "중" if summary.get('edu_level') == 1 else "저",
                        "공통 증상": ", ".join(symptoms.get('common', []))
                    })
                
                # 데이터프레임 생성 및 출력
                df_summary = pd.DataFrame(flat_data)
                st.dataframe(df_summary, use_container_width=True, hide_index=True)
                
                # 상세 분석 결과가 있다면 다시 보기 버튼 제공
                if st.button("이 결과 상세 분석 다시 보기", key=f"hist_review_{idx}"):
                    # 선택한 이력의 첫 번째 유사 환자 정보를 세션에 담고 리런
                    st.session_state['selected_detail'] = similar_patients[0]
                    st.rerun()

# -----------------------------
# 7. AI 진단 화면
# -----------------------------
def ai_diagnosis_page():
    """증상과 fMRI 이미지를 입력받아 mock AI 진단 결과를 표시합니다."""
    patient_id = st.session_state.get("selected_patient_id")
    patient = get_patient_by_id(patient_id)

    if patient is None:
        st.error("선택된 환자를 찾을 수 없습니다.")
        if st.button("환자 목록으로 이동", key="not_found_back_to_main"):
            navigate("main")
        return

    show_hero(
        "AI 진단 지원",
        "환자 증상과 fMRI 이미지를 바탕으로 유사 사례 매칭 결과를 제공합니다.",
    )

    col_back, col_detail = st.columns([1, 1])
    with col_back:
        if st.button("← 환자 목록", use_container_width=True, key=f"diagnosis_back_main_{patient['id']}"):
            navigate("main")
    with col_detail:
        if st.button("환자 상세 보기", use_container_width=True, key=f"diagnosis_patient_detail_{patient['id']}"):
            navigate("patient_detail", patient["id"])

    section_title("선택된 환자 프로필", "진단 입력 전 환자 정보를 확인합니다.", "Selected Patient")
    render_patient_profile_cards(patient)

    section_title("진단 입력", "MMSE 점수, 증상, fMRI 이미지를 입력하여 유사 사례 매칭을 실행합니다.", "Diagnosis Input")

    symptom_options = [
        {"code": "AXNAUSEA", "label": "메스꺼움"},
        {"code": "AXVOMIT", "label": "구토"},
        {"code": "AXDIARRH", "label": "설사"},
        {"code": "AXCONSTP", "label": "변비"},
        {"code": "AXABDOMN", "label": "복통"},
        {"code": "AXSWEATN", "label": "과도한 발한"},
        {"code": "AXDIZZY", "label": "어지러움"},
        {"code": "AXENERGY", "label": "에너지 감소 / 피로감"},
        {"code": "AXDROWSY", "label": "졸림"},
        {"code": "AXVISION", "label": "시야 문제 (흐림 등)"},
        {"code": "AXHDACHE", "label": "두통"},
        {"code": "AXDRYMTH", "label": "구강 건조"},
        {"code": "AXBREATH", "label": "호흡 곤란"},
        {"code": "AXCOUGH", "label": "기침"},
        {"code": "AXPALPIT", "label": "심계항진 (두근거림)"},
        {"code": "AXCHEST", "label": "흉통"},
        {"code": "AXURNDIS", "label": "배뇨 장애"},
        {"code": "AXURNFRQ", "label": "잦은 소변"},
        {"code": "AXANKLE", "label": "발목 부종"},
        {"code": "AXMUSCLE", "label": "근육통"},
        {"code": "AXRASH", "label": "피부 발진"},
        {"code": "AXINSOMN", "label": "불면증"},
        {"code": "AXDPMOOD", "label": "우울감 (depressed mood)"},
        {"code": "AXCRYING", "label": "울음 증가"},
        {"code": "AXELMOOD", "label": "감정 기복 (elevated mood)"},
        {"code": "AXWANDER", "label": "배회 행동"},
        {"code": "AXFALL", "label": "낙상"},
        {"code": "AXOTHER", "label": "기타 증상"},
    ]

    selected_symptoms = []

    with st.container(border=True):
        st.write("**간이 정신상태검사(MMSE)**")
        mmse_input_col, mmse_guide_col = st.columns([0.35, 0.65], vertical_alignment="center")

        with mmse_input_col:
            mmse_score = st.number_input(
                "MMSE 점수",
                min_value=0,
                max_value=30,
                value=24,
                step=1,
                help="0~30점 범위로 입력합니다. 점수가 낮을수록 인지 장애 가능성이 커질 수 있습니다.",
                key=f"mmse_score_{patient['id']}",
            )

        with mmse_guide_col:
            st.markdown(
                """
                <div class="mmse-guide-card">
                    <h4>MMSE 입력 안내</h4>
                    <p>시간·장소 지남력, 기억, 주의·계산, 언어 능력 등을 종합 평가하는 0~30점 척도입니다.</p>
                    <div class="mmse-score-note">낮은 점수일수록 인지 저하 가능성 증가</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.write("**증상 체크박스**")
        symptom_cols = st.columns(4)

        for idx, symptom in enumerate(symptom_options):
            symptom_code = symptom["code"]
            symptom_label = symptom["label"]
            checkbox_label = f"{symptom_code}: {symptom_label}"

            with symptom_cols[idx % 4]:
                if st.checkbox(checkbox_label, key=f"symptom_{patient['id']}_{symptom_code}"):
                    selected_symptoms.append(checkbox_label)

        fmri_file = st.file_uploader(
            "fMRI 이미지 업로드",
            type=["png", "jpg", "jpeg"],
            help="png, jpg, jpeg 형식의 이미지 파일을 업로드할 수 있습니다.",
        )

        if fmri_file is not None:
            st.image(fmri_file, caption=f"업로드된 fMRI 이미지: {fmri_file.name}", use_container_width=True)

        if st.button("진단 실행", type="primary", use_container_width=True, key=f"run_diagnosis_{patient['id']}"):
            if not selected_symptoms:
                st.warning("최소 1개 이상의 증상을 선택해 주세요.")
                return

            patient_profile = {
                "id": patient["id"],
                "name": patient["name"],
                "birthdate": format_date(patient["birthdate"]),
                "gender": patient["gender"],
                "education": patient["education"],
            }

            # [수정 지점] 구성한 프로필을 세션 스테이트에 저장 (상세 페이지 출력용)
            st.session_state['patient_profile'] = patient_profile

            if fmri_file is not None:
                fmri_file.seek(0)

            with st.spinner("유사 사례 매칭 결과를 생성하는 중입니다..."):
                ai_result = run_ai_diagnosis(patient_profile, selected_symptoms, fmri_file, int(mmse_score))

            diagnosis_result = {
                "diagnosis_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "mmse_score": int(mmse_score),
                "mmse_max_score": 30,
                "symptoms": selected_symptoms,
                "fmri_filename": fmri_file.name if fmri_file is not None else "업로드 없음",
                "similar_patients": ai_result,
            }

            save_diagnosis_history(patient["id"], diagnosis_result)

            st.session_state["latest_diagnosis_result"] = diagnosis_result
            st.session_state["latest_diagnosis_patient_id"] = patient["id"]

            st.success("진단 결과가 해당 환자의 과거 진단 이력에 저장되었습니다.")
            st.rerun() # [권장] 결과를 즉시 반영하기 위해 리런 추가

    latest_result = st.session_state.get("latest_diagnosis_result")
    latest_patient_id = st.session_state.get("latest_diagnosis_patient_id")

    if latest_result is not None and latest_patient_id == patient["id"]:
        st.markdown("---")
        render_diagnosis_result(latest_result)


# -----------------------------
# 8. AI 진단 mock/stub 함수
# -----------------------------
def run_ai_diagnosis(patient_profile, symptoms, fmri_file, mmse_score):
    """
    AI 진단 지원 함수: 프론트엔드 입력을 AI 엔진으로 전달합니다.
    """
    from ai.similarity import SimilarityEngine
    import os

    # 1. 엔진 초기화
    engine = SimilarityEngine()

    # 2. 데이터 형식 변환 (프론트엔드 -> 엔진 규격)
    # 학력: '고' -> 2, '중' -> 1, '저' -> 0
    edu_map = {"고": 2, "중": 1, "저": 0}
    
    # 엔진이 기대하는 dict 구조 생성
    input_data = {
        'EDUCATION_LEVEL': edu_map.get(patient_profile['education'], 0),
        'MMSE_SCORE': mmse_score
    }
    
    # 증상 리스트 ("AXNAUSEA: 메스꺼움")에서 코드("AXNAUSEA")만 추출하여 1로 설정
    for s in symptoms:
        code = s.split(':')[0]
        input_data[code] = 1

    # 3. 업로드된 fMRI 이미지 처리
    # 엔진은 파일 경로를 요구하므로, 업로드된 파일을 임시로 저장합니다.
    temp_path = os.path.join("data", "temp_upload.png")
    if fmri_file is not None:
        with open(temp_path, "wb") as f:
            f.write(fmri_file.getbuffer())
    else:
        # 이미지가 없을 경우를 대비한 예외 처리 (엔진 로직에 따라 변경 가능)
        temp_path = None 

    # 4. 실제 AI 엔진 실행 및 결과 반환
    # 이제 가짜 데이터가 아닌 SimilarityEngine의 결과가 나옵니다.
    detailed_results = engine.find_top_3_similar(input_data, temp_path)
    
    return detailed_results


# -----------------------------
# 9. 환자 프로필 수정 / 삭제
# -----------------------------
def update_patient_profile(patient_id, name, birthdate, gender, education):
    """선택된 환자의 기본 정보를 수정합니다. 진단 이력은 그대로 유지합니다."""
    patient = get_patient_by_id(patient_id)

    if patient is None:
        return False

    patient["name"] = name
    patient["birthdate"] = birthdate
    patient["gender"] = gender
    patient["education"] = education
    return True


def delete_patient_profile(patient_id):
    """선택된 환자 프로필과 진단 이력을 현재 세션에서 삭제합니다."""
    patients = st.session_state.get("patients", [])
    remaining_patients = [patient for patient in patients if patient["id"] != patient_id]

    if len(remaining_patients) == len(patients):
        return False

    st.session_state["patients"] = remaining_patients

    if st.session_state.get("selected_patient_id") == patient_id:
        st.session_state["selected_patient_id"] = None

    if st.session_state.get("latest_diagnosis_patient_id") == patient_id:
        st.session_state["latest_diagnosis_result"] = None
        st.session_state["latest_diagnosis_patient_id"] = None

    return True


# -----------------------------
# 10. 진단 이력 저장
# -----------------------------
def save_diagnosis_history(patient_id, diagnosis_result):
    """
    선택된 환자의 과거 진단 이력에 AI 진단 결과를 저장합니다.
    데모 버전이므로 데이터베이스 대신 st.session_state를 사용합니다.
    """
    patient = get_patient_by_id(patient_id)

    if patient is None:
        return False

    patient.setdefault("diagnosis_history", []).append(diagnosis_result)
    return True


# -----------------------------
# 화면 렌더링 보조 함수
# -----------------------------
def render_diagnosis_result(results_data):
    """
    진단 결과를 화면에 렌더링하는 함수입니다.
    """
    # run_ai_diagnosis에서 {"similar_patients": [...]} 형태로 반환하므로 리스트를 추출합니다.
    results = results_data.get("similar_patients", [])
    
    st.markdown("### 유사 사례 분석 결과")
    
    if not results:
        st.warning("유사한 환자 사례를 찾을 수 없습니다.")
        return

    for idx, item in enumerate(results):
        # [수정] 이제 정보는 item['summary'] 안에 들어있습니다.
        summary = item.get('summary', {})
        symptoms = item.get('symptoms', {})
        
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                # [수정] similarity_score 대신 summary['similarity'] 사용
                st.subheader(f"{idx+1}. 환자 {summary.get('ptid')} (일치율: {summary.get('similarity') or 0}%)")
                
                # 공통 증상 표시
                common_syms = symptoms.get('common', [])
                if common_syms:
                    st.markdown(f"**공통 증상:** {', '.join(common_syms)}")
                
                st.write(f"매칭 시점: {summary.get('matched_month')}개월 차 | 보정 MMSE: {summary.get('mmse')}")
            
            with col2:
                # 상세 페이지로 이동하기 위한 버튼
                unique_key = f"detail_{idx}_{summary.get('ptid', 'unknown')}"
                
                if st.button("상세 분석", key=unique_key):
                    st.session_state['selected_detail'] = item
                    st.rerun()

    # 상세 정보가 선택된 경우 하단에 상세 뷰 렌더링
    if st.session_state.get('selected_detail') is not None:
        render_detail_view(st.session_state['selected_detail'])




def render_sidebar():
    """로그인 이후 공통 좌측 내비게이션을 표시합니다.

    Streamlit 기본 st.sidebar는 브라우저에 저장된 접힘 상태와 버전별 DOM 구조에 영향을 받아
    로그인 직후 보이지 않는 경우가 있어, 메인 레이아웃 내부의 좌측 컬럼으로 안정적으로 렌더링합니다.
    """
    current_page = st.session_state.get("page", "main")

    with st.container(border=True):
        patient_count = len(st.session_state.get("patients", []))
        diagnosis_count = sum(len(patient.get("diagnosis_history", [])) for patient in st.session_state.get("patients", []))
        st.markdown(
            f"""
            <div class="sidebar-brand">
                <p class="sidebar-brand-title">💉 차차 병원</p>
                <p class="sidebar-brand-caption">Cha Cha Clinic</p>
            </div>
            <div class="app-sidebar-divider"></div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "환자 목록",
            use_container_width=True,
            type="primary" if current_page == "main" else "secondary",
            key="sidebar_main",
        ):
            navigate("main")

        if st.button(
            "프로필 추가",
            use_container_width=True,
            type="primary" if current_page == "add_patient" else "secondary",
            key="sidebar_add_patient",
        ):
            navigate("add_patient")

        

        if st.button("로그아웃", use_container_width=True, key="sidebar_logout"):
            st.session_state["logged_in"] = False
            st.session_state["page"] = "login"
            st.session_state["auth_page"] = "login"
            st.session_state["current_user"] = None
            st.session_state["selected_patient_id"] = None
            st.session_state["latest_diagnosis_result"] = None
            st.session_state["latest_diagnosis_patient_id"] = None
            st.session_state["signup_code_approved"] = False
            st.session_state["signup_code_last_value"] = ""
            st.rerun()

        st.markdown(
            f"""
            <div class="app-sidebar-divider"></div>
            <div class="sidebar-user-card sidebar-status-card">
                <p class="sidebar-user-name">Status</p>
                <div class="sidebar-stat-grid">
                    <div class="sidebar-stat-card">
                        <span>등록</span>
                        <strong>{patient_count}명</strong>
                    </div>
                    <div class="sidebar-stat-card">
                        <span>이력</span>
                        <strong>{diagnosis_count}건</strong>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

def render_detail_view(res):
    """
    유사 환자 상세 분석 페이지를 렌더링합니다.
    """
    if res is None:
        return

    st.markdown("---")
    st.header(f"🔍 환자 {res['summary']['ptid']} 사례 상세 분석 리포트")
    
    # 1. 환자 프로필 비교 (Diagnostic vs Similar)
    st.subheader("👤 환자 프로필 비교")
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.markdown("**[진단 중인 환자]**")
        st.write(f"- 학력 수준: {st.session_state['patient_profile']['education']}")
        st.write(f"- 보정 MMSE: {res['mmse_chart']['input_patient_score']}점")
    with p_col2:
        st.markdown(f"**[유사 환자 {res['summary']['ptid']}]**")
        st.write(f"- 학력 수준: {'고' if res['summary']['edu_level']==2 else '중' if res['summary']['edu_level']==1 else '저'}")
        st.write(f"- 매칭 시점 MMSE: {res['summary']['mmse']}점")
        st.write(f"- 사례 일치율: :green[{res['summary']['similarity']}%]")

    # 2. 공통 증상 하이라이트
    st.subheader("📋 공통 증상 매칭")
    common = res['symptoms']['common']
    if common:
        # 의료적 매핑 예시 (실제 DB 코드에 맞게 수정 가능)
        st.success(f"**두 환자에게서 공통으로 나타나는 주요 증상:** {', '.join(common)}")
    else:
        st.info("공통으로 나타나는 신체/행동 증상이 없습니다.")

    # 3. MMSE 변화 추이 그래프
    st.subheader("📈 인지 기능 진행 추이 (MMSE)")
    history_data = res['mmse_chart']['similar_patient_history']
    df_history = pd.DataFrame(history_data)
    df_history.columns = ['Month', 'MMSE']
    
    # 그래프 시각화 (유사환자 선 그래프 + 진단환자 현재 점수 점선)
    st.write("유사 환자의 전체 방문 이력 중 현재 환자와 가장 일치하는 시점을 보여줍니다.")
    st.line_chart(df_history.set_index('Month'))

    # 4. fMRI 시계열 및 매칭 비교 (핵심 기능)
    st.subheader("🧠 fMRI 시각적 유사성 대조")
    st.write("유사 환자의 상태 변화(3~5장)와 진단 환자의 현재 영상을 대조합니다.")
    
    sequence = res['fmri_display']['sequence']
    input_fmri = res['fmri_display']['input_fmri']
    matched_idx = sequence['matched_idx']
    
    # 이미지 가로 나열을 위한 컬럼 생성
    cols = st.columns(len(sequence['paths']))
    
    for i, path in enumerate(sequence['paths']):
        with cols[i]:
            is_matched = (i == matched_idx)
            # 초록색 테두리 스타일 정의
            border_style = "border: 5px solid #28a745; border-radius: 10px; padding: 5px;" if is_matched else ""
            
            # 유사 환자 시퀀스 이미지
            st.markdown(f"<div style='{border_style}'>", unsafe_allow_html=True)
            st.image(path, caption=f"유사환자 ({sequence['months'][i]}m)")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # 매칭된 지점 바로 아래에 진단 환자 이미지 배치 및 강조
            if is_matched:
                st.markdown("<p style='text-align:center; color:#28a745; font-weight:bold; margin-top:10px;'>최대 유사 지점 ▼</p>", unsafe_allow_html=True)
                st.markdown(f"<div style='{border_style}'>", unsafe_allow_html=True)
                st.image(input_fmri, caption="현재 진단 환자")
                st.markdown("</div>", unsafe_allow_html=True)

def render_authenticated_page():
    """로그인 이후 좌측 내비게이션과 현재 페이지 본문을 함께 렌더링합니다."""
    nav_col, content_col = st.columns([0.17, 0.83], gap="medium")

    with nav_col:
        render_sidebar()

    with content_col:
        page = st.session_state.get("page", "main")

        if page == "main":
            main_page()
        elif page == "add_patient":
            add_patient_form()
        elif page == "edit_patient":
            edit_patient_form()
        elif page == "patient_detail":
            patient_detail_page()
        elif page == "ai_diagnosis":
            ai_diagnosis_page()
        else:
            main_page()


# -----------------------------
# 앱 엔트리포인트
# -----------------------------
def main():
    # 세션 상태 초기화 코드 추가
    if 'patient_profile' not in st.session_state:
        # 기본값을 빈 딕셔너리로 설정하여 에러 방지
        st.session_state['patient_profile'] = {'education': '미설정', 'id': 'Unknown'}
    
    if 'selected_detail' not in st.session_state:
        st.session_state['selected_detail'] = None
        
    init_session_state()
    apply_custom_css()

    if not st.session_state["logged_in"]:
        login_page()
        return

    render_authenticated_page()


if __name__ == "__main__":
    main()
