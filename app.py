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


        /* -----------------------------
           AI 진단 결과 / 상세 리포트 리디자인
        ----------------------------- */
        .ai-results-head,
        .detail-report-head {
            display: flex;
            align-items: flex-start;
            gap: 1.1rem;
            margin: 0.35rem 0 1.15rem 0;
        }

        .ai-head-icon,
        .detail-head-icon {
            width: 68px;
            min-width: 68px;
            height: 68px;
            border-radius: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, rgba(255,255,255,0.96), rgba(234,249,247,0.82));
            border: 1px solid rgba(44, 184, 175, 0.16);
            box-shadow: 0 16px 42px rgba(15, 23, 42, 0.08);
            font-size: 2rem;
        }

        .ai-results-head h2,
        .detail-report-head h2 {
            margin: 0;
            font-size: clamp(2rem, 3.4vw, 3.05rem);
            line-height: 1.08;
            font-weight: 950;
            letter-spacing: -0.065em;
            color: var(--az-text);
        }

        .ai-results-head p,
        .detail-report-head p {
            margin: 0.48rem 0 0 0;
            color: #4B5B6B;
            font-size: 1.02rem;
            font-weight: 650;
            line-height: 1.62;
        }

        .ai-eyebrow,
        .detail-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 0.42rem;
            margin-bottom: 0.42rem;
            color: var(--az-primary-dark);
            font-weight: 900;
            font-size: 0.78rem;
            letter-spacing: 0.03em;
            text-transform: uppercase;
        }

        .ai-summary-chip-row,
        .detail-summary-strip {
            display: flex;
            flex-wrap: wrap;
            gap: 0.72rem;
            margin: 0.6rem 0 1.35rem 0;
        }

        .ai-summary-chip,
        .detail-summary-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.55rem;
            min-height: 45px;
            padding: 0.58rem 1rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.78);
            border: 1px solid rgba(148, 163, 184, 0.18);
            box-shadow: 0 10px 26px rgba(15, 23, 42, 0.045);
            backdrop-filter: blur(12px);
            color: #253449;
            font-weight: 850;
        }

        .ai-summary-chip strong,
        .detail-summary-chip strong {
            color: #139363;
            font-weight: 950;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.similarity-card-marker) {
            border-radius: 28px !important;
            border: 1px solid rgba(148, 163, 184, 0.18) !important;
            background: linear-gradient(180deg, rgba(255,255,255,0.92), rgba(255,255,255,0.78)) !important;
            box-shadow: 0 18px 48px rgba(15, 23, 42, 0.075) !important;
            backdrop-filter: blur(16px);
            margin-bottom: 1.5rem;
            overflow: hidden;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.similarity-card-marker.best) {
            border-color: rgba(24, 166, 102, 0.62) !important;
            box-shadow: 0 22px 56px rgba(20, 120, 85, 0.13) !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.similarity-card-marker.best)::before {
            content: "★ Best Match";
            display: inline-flex;
            position: absolute;
            top: 0;
            left: 0;
            padding: 0.42rem 1.35rem 0.5rem 1.05rem;
            border-bottom-right-radius: 18px;
            background: linear-gradient(135deg, #13A36F, #2CB8AF);
            color: #fff;
            font-size: 0.88rem;
            font-weight: 950;
            letter-spacing: -0.01em;
            z-index: 10;
        }

        .similarity-card-marker {
            display: block;
            height: 0.5rem;
        }

        .result-rank-badge {
            width: 86px;
            height: 86px;
            margin: 0.35rem auto 0.2rem auto;
            border-radius: 999px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #0F2742;
            background: linear-gradient(135deg, #F2F7FB, #EAF2F7);
            border: 1px solid rgba(11,111,184,0.10);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.78), 0 14px 24px rgba(15,23,42,0.05);
            font-size: 2.05rem;
            font-weight: 950;
            position: relative;
        }

        .result-rank-badge.best {
            color: #fff;
            background: linear-gradient(135deg, #18A66B, #2CB8AF);
            box-shadow: 0 16px 34px rgba(24,166,107,0.22);
        }

        .result-patient-title {
            margin: 0.2rem 0 0.55rem 0;
            font-size: clamp(1.65rem, 2.35vw, 2.4rem);
            line-height: 1.12;
            color: var(--az-text);
            font-weight: 950;
            letter-spacing: -0.05em;
        }

        .result-meta-chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.56rem;
            margin-top: 0.55rem;
        }

        .result-meta-chip-row.compact {
            gap: 0.62rem;
        }

        .result-meta-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.46rem 0.78rem;
            border-radius: 12px;
            background: rgba(248,250,252,0.78);
            border: 1px solid rgba(148, 163, 184, 0.19);
            color: #29405A;
            font-size: 0.92rem;
            font-weight: 820;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.68);
        }

        .result-meta-chip b {
            color: #15395D;
            font-weight: 950;
        }

        .result-score-pill {
            max-width: 126px;
            min-height: 74px;
            margin: 0.3rem auto 0.7rem auto;
            padding: 0.7rem 0.8rem;
            border-radius: 24px;
            text-align: center;
            background: linear-gradient(180deg, rgba(236,253,245,0.95), rgba(240,253,250,0.86));
            border: 1px solid rgba(24,166,107,0.18);
            color: #139363;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.86);
        }

        .result-score-pill strong {
            display: block;
            font-size: 1.55rem;
            font-weight: 950;
            letter-spacing: -0.04em;
        }

        .result-score-pill span {
            display: block;
            margin-top: 0.1rem;
            color: #4E6A62;
            font-size: 0.82rem;
            font-weight: 900;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.similarity-card-marker) .stButton > button {
            min-height: 54px;
            border-radius: 16px !important;
            border: 1px solid rgba(19, 147, 99, 0.38) !important;
            background: rgba(255,255,255,0.74) !important;
            color: #0D6B4B !important;
            font-weight: 950 !important;
            box-shadow: 0 10px 22px rgba(15,23,42,0.05) !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.similarity-card-marker) .stButton > button:hover {
            border-color: rgba(19, 147, 99, 0.68) !important;
            background: linear-gradient(135deg, rgba(236,253,245,0.94), rgba(255,255,255,0.86)) !important;
            transform: translateY(-1px);
        }

        .detail-topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
            margin: 1.2rem 0 0.25rem 0;
            color: #1A6A72;
            font-size: 0.92rem;
            font-weight: 850;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.detail-card-marker),
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.report-section-marker),
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.fmri-thumb-marker) {
            border-radius: 24px !important;
            border: 1px solid rgba(148, 163, 184, 0.18) !important;
            background: linear-gradient(180deg, rgba(255,255,255,0.92), rgba(255,255,255,0.78)) !important;
            box-shadow: 0 14px 38px rgba(15, 23, 42, 0.065) !important;
            backdrop-filter: blur(14px);
            overflow: hidden;
        }

        .section-title-row {
            display: flex;
            align-items: center;
            gap: 0.62rem;
            margin: 0.15rem 0 0.85rem 0;
            color: var(--az-text);
        }

        .section-title-row .section-num {
            width: 32px;
            height: 32px;
            border-radius: 11px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #EAF9F7, #E9F5FF);
            color: #0B6FB8;
            font-size: 0.95rem;
            font-weight: 950;
        }

        .section-title-row h3 {
            margin: 0;
            font-size: 1.28rem;
            font-weight: 950;
            letter-spacing: -0.045em;
        }

        .profile-compare-grid {
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            align-items: stretch;
            gap: 1rem;
        }

        .profile-panel {
            border-radius: 20px;
            border: 1px solid rgba(148, 163, 184, 0.18);
            background: rgba(255,255,255,0.72);
            overflow: hidden;
        }

        .profile-panel-head {
            padding: 0.72rem 0.92rem;
            background: linear-gradient(135deg, rgba(233,245,255,0.90), rgba(234,249,247,0.76));
            color: #0B4B77;
            font-size: 0.9rem;
            font-weight: 950;
            text-align: center;
        }

        .profile-panel.similar .profile-panel-head {
            background: linear-gradient(135deg, rgba(236,253,245,0.96), rgba(234,249,247,0.82));
            color: #0D6B4B;
        }

        .profile-row {
            display: flex;
            align-items: center;
            gap: 0.72rem;
            padding: 0.82rem 0.95rem;
            border-top: 1px solid rgba(148, 163, 184, 0.13);
        }

        .profile-row-icon {
            width: 38px;
            min-width: 38px;
            height: 38px;
            border-radius: 15px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: rgba(233,245,255,0.80);
        }

        .profile-row span {
            display: block;
            color: #667085;
            font-size: 0.76rem;
            font-weight: 850;
        }

        .profile-row strong {
            display: block;
            margin-top: 0.08rem;
            color: var(--az-text);
            font-size: 0.98rem;
            font-weight: 950;
        }

        .profile-vs {
            align-self: center;
            width: 44px;
            height: 44px;
            border-radius: 999px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: #EEF7FB;
            color: #18415D;
            font-weight: 950;
            border: 1px solid rgba(11,111,184,0.10);
        }

        .symptom-callout {
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 1.05rem 1.15rem;
            border-radius: 19px;
            background: linear-gradient(135deg, rgba(236,253,245,0.98), rgba(240,253,250,0.88));
            border: 1px solid rgba(24,166,107,0.20);
        }

        .symptom-callout-icon {
            width: 50px;
            min-width: 50px;
            height: 50px;
            border-radius: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            background: linear-gradient(135deg, #18A66B, #2CB8AF);
            box-shadow: 0 12px 24px rgba(24,166,107,0.18);
        }

        .symptom-callout span {
            color: #3E5A52;
            font-size: 0.88rem;
            font-weight: 850;
        }

        .symptom-callout strong {
            display: block;
            margin-top: 0.12rem;
            color: #0D6B4B;
            font-size: 1.18rem;
            font-weight: 950;
            letter-spacing: 0.02em;
        }

        .chart-caption,
        .fmri-caption {
            margin: -0.25rem 0 0.85rem 0;
            color: #5D6F80;
            font-size: 0.9rem;
            font-weight: 650;
        }

        .fmri-thumb-label {
            text-align: center;
            margin-top: 0.42rem;
            color: #5D6F80;
            font-size: 0.84rem;
            font-weight: 850;
        }

        .fmri-thumb-label.matched {
            color: #14925F;
            font-weight: 950;
        }

        .fmri-match-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            padding: 0.32rem 0.45rem;
            margin-bottom: 0.46rem;
            border-radius: 12px;
            background: linear-gradient(135deg, #18A66B, #2CB8AF);
            color: white;
            font-size: 0.82rem;
            font-weight: 950;
            box-shadow: 0 10px 20px rgba(24,166,107,0.18);
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.fmri-thumb-marker.matched) {
            border-color: rgba(24,166,107,0.58) !important;
            box-shadow: 0 16px 36px rgba(24,166,107,0.13) !important;
        }

        .fmri-placeholder {
            min-height: 132px;
            border-radius: 16px;
            border: 1px dashed rgba(100,116,139,0.28);
            background: linear-gradient(135deg, rgba(248,250,252,0.78), rgba(241,245,249,0.62));
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: #708090;
            font-size: 0.82rem;
            font-weight: 800;
            padding: 0.8rem;
        }

        .current-fmri-note {
            padding: 1rem 1.1rem;
            border-radius: 20px;
            background: linear-gradient(135deg, rgba(236,253,245,0.92), rgba(255,255,255,0.72));
            border: 1px solid rgba(24,166,107,0.18);
        }

        .current-fmri-note strong {
            display: block;
            color: var(--az-text);
            font-size: 1.06rem;
            font-weight: 950;
            margin-bottom: 0.22rem;
        }

        .current-fmri-note span {
            color: #536777;
            line-height: 1.62;
            font-weight: 700;
        }

        .report-disclaimer {
            display: flex;
            align-items: center;
            gap: 0.62rem;
            padding: 0.8rem 1rem;
            border-radius: 16px;
            border: 1px solid rgba(11,111,184,0.12);
            background: rgba(233,245,255,0.55);
            color: #45586A;
            font-size: 0.86rem;
            font-weight: 760;
            margin-top: 0.85rem;
        }

        @media screen and (max-width: 900px) {
            .profile-compare-grid {
                grid-template-columns: 1fr;
            }

            .profile-vs {
                margin: 0 auto;
            }

            .ai-results-head,
            .detail-report-head {
                flex-direction: column;
            }
        }



        /* -----------------------------
           AI 결과/리포트 레이아웃 재정렬 override v2
           - 과도한 여백, 좁은 썸네일, 카드 높이 불균형 보정
        ----------------------------- */
        .ai-results-head,
        .detail-report-head {
            gap: 0.95rem;
            margin: 0.15rem 0 0.9rem 0;
        }

        .ai-head-icon,
        .detail-head-icon {
            width: 58px;
            min-width: 58px;
            height: 58px;
            border-radius: 20px;
            font-size: 1.55rem;
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
        }

        .ai-results-head h2,
        .detail-report-head h2 {
            font-size: clamp(1.85rem, 2.65vw, 2.65rem);
            line-height: 1.12;
            letter-spacing: -0.06em;
        }

        .ai-results-head p,
        .detail-report-head p {
            margin-top: 0.38rem;
            font-size: 0.96rem;
            line-height: 1.52;
        }

        .ai-summary-chip-row,
        .detail-summary-strip {
            gap: 0.55rem;
            margin: 0.4rem 0 1rem 0;
        }

        .ai-summary-chip,
        .detail-summary-chip {
            min-height: 40px;
            padding: 0.48rem 0.82rem;
            font-size: 0.88rem;
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.035);
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.similarity-card-marker) {
            border-radius: 22px !important;
            margin-bottom: 1.2rem !important;
            box-shadow: 0 12px 28px rgba(15, 23, 42, 0.055) !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.similarity-card-marker.best)::before {
            padding: 0.34rem 1.05rem 0.4rem 0.9rem;
            border-bottom-right-radius: 14px;
            font-size: 0.78rem;
        }

        .similarity-card-marker {
            height: 0.2rem;
        }

        .result-rank-badge {
            width: 68px;
            height: 68px;
            margin: 0.18rem auto 0 auto;
            font-size: 1.55rem;
        }

        .result-patient-title {
            margin: 0.05rem 0 0.45rem 0;
            font-size: clamp(1.42rem, 1.85vw, 2rem);
            line-height: 1.12;
            letter-spacing: -0.048em;
        }

        .result-meta-chip-row {
            gap: 0.46rem;
            margin-top: 0.4rem;
        }

        .result-meta-chip {
            padding: 0.38rem 0.62rem;
            border-radius: 11px;
            font-size: 0.82rem;
            line-height: 1.18;
            white-space: normal;
        }

        .result-score-pill {
            max-width: 108px;
            min-height: 64px;
            margin: 0.2rem auto 0.55rem auto;
            padding: 0.58rem 0.62rem;
            border-radius: 20px;
        }

        .result-score-pill strong {
            font-size: 1.26rem;
        }

        .result-score-pill span {
            font-size: 0.76rem;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.similarity-card-marker) .stButton > button {
            min-height: 46px;
            border-radius: 14px !important;
            font-size: 0.9rem;
        }

        .detail-topbar {
            margin: 0.8rem 0 0.15rem 0;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.detail-card-marker),
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.report-section-marker),
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.fmri-thumb-marker) {
            border-radius: 20px !important;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.052) !important;
        }

        .section-title-row {
            margin: 0.05rem 0 0.7rem 0;
        }

        .section-title-row .section-num {
            width: 28px;
            height: 28px;
            border-radius: 10px;
            font-size: 0.84rem;
        }

        .section-title-row h3 {
            font-size: 1.13rem;
        }

        .profile-compare-grid.refined {
            grid-template-columns: minmax(0, 1fr) 46px minmax(0, 1fr);
            gap: 0.8rem;
            align-items: stretch;
        }

        .profile-panel {
            border-radius: 17px;
        }

        .profile-panel-head {
            padding: 0.62rem 0.82rem;
            font-size: 0.84rem;
        }

        .profile-row {
            min-height: 58px;
            padding: 0.66rem 0.82rem;
            gap: 0.62rem;
        }

        .profile-row-icon {
            width: 34px;
            min-width: 34px;
            height: 34px;
            border-radius: 13px;
        }

        .profile-row span {
            font-size: 0.72rem;
        }

        .profile-row strong {
            font-size: 0.92rem;
        }

        .profile-vs {
            width: 40px;
            height: 40px;
            font-size: 0.8rem;
        }

        .symptom-callout {
            padding: 0.9rem 1rem;
            border-radius: 17px;
        }

        .symptom-callout-icon {
            width: 44px;
            min-width: 44px;
            height: 44px;
            border-radius: 16px;
        }

        .symptom-callout strong {
            font-size: 1.04rem;
            line-height: 1.42;
            letter-spacing: -0.01em;
        }

        .chart-caption,
        .fmri-caption {
            margin: -0.18rem 0 0.72rem 0;
            font-size: 0.86rem;
        }

        .fmri-sequence-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(132px, 1fr));
            gap: 0.78rem;
            margin-top: 0.35rem;
        }

        .fmri-sequence-card {
            position: relative;
            min-height: 178px;
            padding: 0.7rem;
            border-radius: 18px;
            background: rgba(255,255,255,0.72);
            border: 1px solid rgba(148, 163, 184, 0.20);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.65);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            gap: 0.52rem;
        }

        .fmri-sequence-card.matched {
            border-color: rgba(24,166,107,0.62);
            background: linear-gradient(180deg, rgba(236,253,245,0.92), rgba(255,255,255,0.78));
            box-shadow: 0 14px 28px rgba(24,166,107,0.11);
        }


        .fmri-match-spacer {
            height: 1.65rem;
        }

        .fmri-sequence-label.current {
            color: #14925F;
            font-weight: 950;
            margin-top: 0.55rem;
        }

        .fmri-sequence-card .fmri-match-badge {
            position: static;
            width: auto;
            padding: 0.26rem 0.55rem;
            margin: 0;
            border-radius: 999px;
            font-size: 0.72rem;
            line-height: 1.1;
        }

        .fmri-mini-image {
            width: 100%;
            max-width: 132px;
            aspect-ratio: 1.12 / 1;
            object-fit: cover;
            border-radius: 12px;
            background: #0B0F14;
            box-shadow: 0 8px 18px rgba(15,23,42,0.08);
        }

        .fmri-mini-placeholder {
            width: 100%;
            max-width: 132px;
            aspect-ratio: 1.12 / 1;
            border-radius: 12px;
            border: 1px dashed rgba(100,116,139,0.25);
            background: linear-gradient(135deg, rgba(248,250,252,0.90), rgba(241,245,249,0.68));
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: #708090;
            font-size: 0.74rem;
            font-weight: 800;
            padding: 0.5rem;
        }

        .fmri-sequence-label {
            color: #5D6F80;
            font-size: 0.82rem;
            font-weight: 850;
            text-align: center;
            line-height: 1.25;
            word-break: keep-all;
        }

        .fmri-sequence-card.matched .fmri-sequence-label {
            color: #14925F;
            font-weight: 950;
        }

        .current-fmri-grid {
            display: grid;
            grid-template-columns: minmax(220px, 0.42fr) minmax(0, 1fr);
            gap: 1rem;
            align-items: stretch;
            margin-top: 1rem;
        }

        .current-fmri-card {
            padding: 0.82rem;
            border-radius: 18px;
            border: 1px solid rgba(24,166,107,0.24);
            background: rgba(255,255,255,0.74);
            text-align: center;
        }

        .current-fmri-image {
            width: 100%;
            max-height: 240px;
            object-fit: contain;
            border-radius: 14px;
            background: #0B0F14;
        }

        .current-fmri-note {
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 1.1rem 1.2rem;
        }

        .current-fmri-note strong {
            font-size: 1rem;
        }

        .current-fmri-note span {
            font-size: 0.92rem;
        }

        .report-disclaimer {
            margin-top: 1rem;
        }

        @media screen and (max-width: 1100px) {
            .profile-compare-grid.refined {
                grid-template-columns: 1fr;
            }

            .profile-vs {
                margin: 0 auto;
            }
        }

        @media screen and (max-width: 760px) {
            .current-fmri-grid {
                grid-template-columns: 1fr;
            }

            .result-rank-badge {
                width: 58px;
                height: 58px;
                font-size: 1.28rem;
            }
        }



        /* -----------------------------
           AI 결과/상세 리포트 UI polish v3
           - 기존 정보 구조는 유지하고, 화면 밀도·정렬·의료 서비스 톤을 재정리
        ----------------------------- */
        :root {
            --az-page: #F7F9FC;
            --az-surface: #FFFFFF;
            --az-surface-soft: #F8FAFC;
            --az-line: #D9E2EC;
            --az-line-soft: #E9EEF5;
            --az-ink: #172033;
            --az-ink-2: #344054;
            --az-ink-3: #667085;
            --az-brand: #0B6FB8;
            --az-brand-2: #1279A8;
            --az-match: #0F8F63;
            --az-match-soft: #EAF8F1;
            --az-card-shadow: 0 10px 26px rgba(16, 24, 40, 0.055);
            --az-card-shadow-hover: 0 14px 34px rgba(16, 24, 40, 0.075);
        }

        .stApp {
            background:
                radial-gradient(circle at 8% 0%, rgba(11,111,184,0.055), transparent 26%),
                linear-gradient(180deg, #F8FAFC 0%, #F4F8FB 100%) !important;
        }

        .block-container {
            max-width: 1320px;
            padding-top: 2rem;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--az-surface) !important;
            border: 1px solid var(--az-line) !important;
            border-radius: 18px !important;
            box-shadow: var(--az-card-shadow) !important;
            backdrop-filter: none !important;
            transition: border-color .16s ease, box-shadow .16s ease !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]::before {
            display: none !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: none !important;
            border-color: #C7D5E3 !important;
            box-shadow: var(--az-card-shadow-hover) !important;
        }

        .ai-results-head,
        .detail-report-head {
            position: relative;
            gap: 1rem !important;
            align-items: center !important;
            padding: 1.15rem 1.25rem !important;
            margin: 0 0 1rem 0 !important;
            border: 1px solid var(--az-line) !important;
            border-radius: 20px !important;
            background: linear-gradient(180deg, #FFFFFF 0%, #F8FBFD 100%) !important;
            box-shadow: var(--az-card-shadow) !important;
        }

        .ai-results-head::before,
        .detail-report-head::before {
            content: "";
            position: absolute;
            left: 0;
            top: 18px;
            bottom: 18px;
            width: 4px;
            border-radius: 999px;
            background: linear-gradient(180deg, var(--az-brand), var(--az-match));
        }

        .ai-head-icon,
        .detail-head-icon {
            width: 46px !important;
            min-width: 46px !important;
            height: 46px !important;
            border-radius: 14px !important;
            color: var(--az-brand) !important;
            background: #F2F7FB !important;
            border: 1px solid #DDEAF5 !important;
            box-shadow: none !important;
            font-size: 0 !important;
            position: relative;
        }

        .ai-head-icon::after,
        .detail-head-icon::after {
            content: "AI";
            font-size: 0.9rem;
            font-weight: 900;
            letter-spacing: -0.02em;
        }

        .detail-head-icon::after {
            content: "RPT";
            font-size: 0.78rem;
        }

        .ai-eyebrow,
        .detail-eyebrow {
            margin-bottom: 0.25rem !important;
            color: #5B6B7C !important;
            font-size: 0.72rem !important;
            font-weight: 850 !important;
            letter-spacing: 0.08em !important;
        }

        .ai-results-head h2,
        .detail-report-head h2 {
            margin: 0 !important;
            font-size: clamp(1.55rem, 2.1vw, 2.15rem) !important;
            font-weight: 850 !important;
            line-height: 1.18 !important;
            letter-spacing: -0.045em !important;
            color: var(--az-ink) !important;
        }

        .ai-results-head p,
        .detail-report-head p {
            margin-top: 0.28rem !important;
            color: var(--az-ink-3) !important;
            font-size: 0.94rem !important;
            font-weight: 520 !important;
            line-height: 1.55 !important;
        }

        .ai-flow-strip {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.75rem;
            margin: 0 0 1rem 0;
        }

        .ai-flow-step {
            position: relative;
            min-height: 74px;
            padding: 0.9rem 1rem 0.85rem 1rem;
            border: 1px solid var(--az-line-soft);
            border-radius: 16px;
            background: #FFFFFF;
            box-shadow: 0 6px 18px rgba(16,24,40,0.035);
        }

        .ai-flow-step b {
            display: block;
            color: var(--az-ink);
            font-size: 0.92rem;
            font-weight: 850;
            letter-spacing: -0.025em;
        }

        .ai-flow-step span {
            display: block;
            margin-top: 0.24rem;
            color: var(--az-ink-3);
            font-size: 0.78rem;
            line-height: 1.38;
        }

        .ai-flow-step::before {
            content: attr(data-step);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 1.5rem;
            height: 1.5rem;
            margin-bottom: 0.42rem;
            border-radius: 999px;
            background: #F1F6FA;
            color: var(--az-brand);
            font-weight: 900;
            font-size: 0.72rem;
        }

        .ai-flow-step.active {
            border-color: rgba(15, 143, 99, 0.28);
            background: linear-gradient(180deg, #FFFFFF 0%, #F2FBF7 100%);
        }

        .ai-flow-step.active::before {
            color: #fff;
            background: var(--az-match);
        }

        .ai-summary-chip-row,
        .detail-summary-strip {
            display: grid !important;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.75rem !important;
            margin: 0 0 1rem 0 !important;
        }

        .detail-summary-strip {
            grid-template-columns: repeat(4, minmax(0, 1fr));
        }

        .ai-summary-chip,
        .detail-summary-chip {
            display: block !important;
            min-height: 72px !important;
            padding: 0.82rem 0.95rem !important;
            border-radius: 16px !important;
            background: #FFFFFF !important;
            border: 1px solid var(--az-line-soft) !important;
            box-shadow: 0 6px 18px rgba(16, 24, 40, 0.035) !important;
            color: var(--az-ink-3) !important;
            font-size: 0.76rem !important;
            font-weight: 800 !important;
            line-height: 1.35 !important;
        }

        .ai-summary-chip span,
        .detail-summary-chip span {
            display: block;
            color: var(--az-ink-3);
            font-size: 0.72rem;
            font-weight: 760;
            letter-spacing: -0.01em;
        }

        .ai-summary-chip strong,
        .detail-summary-chip strong {
            display: block;
            margin-top: 0.25rem;
            color: var(--az-ink) !important;
            font-size: 1.08rem;
            line-height: 1.22;
            font-weight: 880 !important;
            letter-spacing: -0.035em;
        }

        .ai-summary-chip.is-primary strong,
        .detail-summary-chip.is-primary strong {
            color: var(--az-match) !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.similarity-card-marker) {
            margin-bottom: 0.85rem !important;
            border-radius: 18px !important;
            border: 1px solid var(--az-line) !important;
            background: #FFFFFF !important;
            box-shadow: var(--az-card-shadow) !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.similarity-card-marker.best) {
            border-color: rgba(15, 143, 99, 0.40) !important;
            box-shadow: 0 12px 30px rgba(15, 143, 99, 0.10) !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.similarity-card-marker.best)::before {
            content: "최고 유사 사례" !important;
            display: inline-flex !important;
            position: absolute !important;
            top: 0 !important;
            left: auto !important;
            right: 0 !important;
            padding: 0.36rem 0.9rem 0.42rem 0.9rem !important;
            border-bottom-left-radius: 12px !important;
            border-bottom-right-radius: 0 !important;
            background: var(--az-match) !important;
            color: #fff !important;
            font-size: 0.74rem !important;
            font-weight: 850 !important;
            letter-spacing: -0.01em !important;
            z-index: 10 !important;
        }

        .similarity-card-marker { height: 0 !important; }

        .result-rank-badge {
            width: 48px !important;
            height: 48px !important;
            margin: 0.15rem auto !important;
            border-radius: 14px !important;
            background: #F4F7FA !important;
            color: #3E5063 !important;
            border: 1px solid var(--az-line-soft) !important;
            box-shadow: none !important;
            font-size: 1rem !important;
            font-weight: 880 !important;
        }

        .result-rank-badge.best {
            background: var(--az-match-soft) !important;
            color: var(--az-match) !important;
            border-color: rgba(15,143,99,0.25) !important;
            box-shadow: none !important;
        }

        .result-patient-title {
            margin: 0 !important;
            color: var(--az-ink) !important;
            font-size: clamp(1.2rem, 1.55vw, 1.55rem) !important;
            line-height: 1.22 !important;
            font-weight: 860 !important;
            letter-spacing: -0.04em !important;
        }

        .result-patient-subtitle {
            margin-top: 0.22rem;
            color: var(--az-ink-3);
            font-size: 0.8rem;
            font-weight: 680;
        }

        .result-meta-chip-row.compact {
            display: grid !important;
            grid-template-columns: repeat(2, minmax(0, 180px));
            gap: 0.5rem !important;
            margin-top: 0.65rem !important;
        }

        .result-meta-chip {
            display: block !important;
            padding: 0.55rem 0.68rem !important;
            border-radius: 12px !important;
            background: #F8FAFC !important;
            border: 1px solid var(--az-line-soft) !important;
            box-shadow: none !important;
            color: var(--az-ink-3) !important;
            font-size: 0.72rem !important;
            font-weight: 760 !important;
            line-height: 1.28 !important;
        }

        .result-meta-chip b {
            display: block;
            margin-top: 0.18rem;
            color: var(--az-ink) !important;
            font-size: 0.92rem;
            font-weight: 860 !important;
            letter-spacing: -0.025em;
        }

        .result-score-pill {
            max-width: 116px !important;
            min-height: 62px !important;
            margin: 0.12rem auto 0.35rem auto !important;
            padding: 0.65rem 0.7rem !important;
            border-radius: 16px !important;
            background: var(--az-match-soft) !important;
            border: 1px solid rgba(15,143,99,0.18) !important;
            color: var(--az-match) !important;
            box-shadow: none !important;
        }

        .result-score-pill strong {
            font-size: 1.34rem !important;
            font-weight: 900 !important;
        }

        .result-score-pill span {
            color: #527469 !important;
            font-size: 0.72rem !important;
            font-weight: 820 !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.similarity-card-marker) .stButton > button {
            min-height: 44px !important;
            border-radius: 12px !important;
            background: var(--az-ink) !important;
            color: #FFFFFF !important;
            border: 1px solid var(--az-ink) !important;
            box-shadow: none !important;
            font-size: 0.86rem !important;
            font-weight: 820 !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.similarity-card-marker) .stButton > button:hover {
            transform: none !important;
            background: #0B1220 !important;
            border-color: #0B1220 !important;
            color: #FFFFFF !important;
        }

        .detail-topbar {
            margin: 0.65rem 0 0.55rem 0 !important;
            color: var(--az-ink-3) !important;
            font-size: 0.82rem !important;
            font-weight: 760 !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.detail-card-marker),
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.report-section-marker),
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.fmri-thumb-marker) {
            border-radius: 18px !important;
            border: 1px solid var(--az-line) !important;
            background: #FFFFFF !important;
            box-shadow: var(--az-card-shadow) !important;
        }

        .section-title-row {
            display: flex !important;
            justify-content: flex-start !important;
            align-items: center !important;
            gap: 0.7rem !important;
            margin: 0.05rem 0 1rem 0 !important;
            padding-bottom: 0.78rem;
            border-bottom: 1px solid var(--az-line-soft);
        }

        .section-title-row .section-num {
            width: 34px !important;
            height: 34px !important;
            min-width: 34px !important;
            border-radius: 10px !important;
            background: #F2F6FA !important;
            color: #44566A !important;
            font-size: 0.78rem !important;
            font-weight: 900 !important;
            letter-spacing: 0.01em;
        }

        .section-title-row h3 {
            margin: 0 !important;
            color: var(--az-ink) !important;
            font-size: 1.24rem !important;
            font-weight: 860 !important;
            letter-spacing: -0.04em !important;
            text-align: left !important;
        }

        .profile-compare-grid.refined {
            grid-template-columns: minmax(0, 1fr) 42px minmax(0, 1fr) !important;
            gap: 0.85rem !important;
            align-items: stretch !important;
        }

        .profile-panel {
            border-radius: 16px !important;
            border: 1px solid var(--az-line-soft) !important;
            background: #FFFFFF !important;
            overflow: hidden !important;
        }

        .profile-panel-head {
            padding: 0.75rem 0.95rem !important;
            background: #F8FAFC !important;
            border-bottom: 1px solid var(--az-line-soft);
            color: var(--az-ink) !important;
            font-size: 0.9rem !important;
            font-weight: 860 !important;
            text-align: left !important;
        }

        .profile-panel.similar .profile-panel-head {
            background: #F3FBF7 !important;
            color: #0C6B4E !important;
        }

        .profile-row {
            min-height: 64px !important;
            padding: 0.82rem 0.95rem !important;
            gap: 0.75rem !important;
            border-top: 1px solid var(--az-line-soft) !important;
            background: #FFFFFF !important;
        }

        .profile-row:first-of-type {
            border-top: none !important;
        }

        .profile-row-icon {
            width: 42px !important;
            min-width: 42px !important;
            height: 42px !important;
            border-radius: 12px !important;
            background: #F4F7FA !important;
            color: #55677A !important;
            border: 1px solid #E4EBF2 !important;
            font-size: 0.72rem !important;
            font-weight: 900 !important;
            letter-spacing: -0.02em !important;
        }

        .profile-row span:not(.profile-row-icon) {
            color: var(--az-ink-3) !important;
            font-size: 0.75rem !important;
            font-weight: 760 !important;
        }

        .profile-row strong {
            margin-top: 0.12rem !important;
            color: var(--az-ink) !important;
            font-size: 1.03rem !important;
            font-weight: 860 !important;
            letter-spacing: -0.03em !important;
        }

        .profile-vs {
            width: 42px !important;
            height: 42px !important;
            border-radius: 999px !important;
            background: #FFFFFF !important;
            border: 1px solid var(--az-line) !important;
            color: var(--az-ink-3) !important;
            font-size: 0.78rem !important;
            font-weight: 900 !important;
            box-shadow: none !important;
        }

        .symptom-callout {
            display: flex !important;
            align-items: flex-start !important;
            gap: 0.9rem !important;
            padding: 1rem 1.1rem !important;
            border-radius: 16px !important;
            background: #F7FCFA !important;
            border: 1px solid rgba(15,143,99,0.20) !important;
            box-shadow: none !important;
        }

        .symptom-callout-icon {
            width: 44px !important;
            min-width: 44px !important;
            height: 44px !important;
            border-radius: 12px !important;
            background: var(--az-match) !important;
            color: #FFFFFF !important;
            font-size: 0 !important;
            box-shadow: none !important;
        }

        .symptom-callout-icon::after {
            content: "공통";
            font-size: 0.74rem;
            font-weight: 900;
        }

        .symptom-callout span {
            color: var(--az-ink-3) !important;
            font-size: 0.83rem !important;
            font-weight: 760 !important;
        }

        .symptom-callout strong {
            display: block !important;
            margin-top: 0.25rem !important;
            color: #0C6B4E !important;
            font-size: 1.12rem !important;
            line-height: 1.45 !important;
            font-weight: 880 !important;
            letter-spacing: -0.02em !important;
        }

        .chart-caption,
        .fmri-caption {
            margin: -0.35rem 0 0.85rem 0 !important;
            color: var(--az-ink-3) !important;
            font-size: 0.88rem !important;
            line-height: 1.5 !important;
            font-weight: 520 !important;
        }

        .fmri-sequence-grid {
            display: grid !important;
            grid-template-columns: repeat(auto-fit, minmax(156px, 1fr)) !important;
            gap: 0.8rem !important;
            margin-top: 0.35rem !important;
        }

        .fmri-sequence-card {
            min-height: 188px !important;
            padding: 0.75rem !important;
            border-radius: 16px !important;
            background: #FFFFFF !important;
            border: 1px solid var(--az-line-soft) !important;
            box-shadow: 0 6px 16px rgba(16,24,40,0.035) !important;
        }

        .fmri-sequence-card.matched {
            border-color: rgba(15,143,99,0.40) !important;
            background: #F5FCF8 !important;
            box-shadow: 0 8px 22px rgba(15,143,99,0.08) !important;
        }

        .fmri-sequence-card .fmri-match-badge {
            width: 100% !important;
            padding: 0.32rem 0.5rem !important;
            border-radius: 10px !important;
            background: var(--az-match) !important;
            color: #FFFFFF !important;
            font-size: 0.72rem !important;
            font-weight: 860 !important;
            letter-spacing: -0.01em !important;
            text-align: center;
        }

        .fmri-match-spacer {
            height: 1.7rem !important;
        }

        .fmri-mini-image,
        .fmri-mini-placeholder {
            max-width: 142px !important;
            border-radius: 12px !important;
        }

        .fmri-sequence-label {
            color: var(--az-ink-3) !important;
            font-size: 0.82rem !important;
            font-weight: 800 !important;
        }

        .fmri-sequence-card.matched .fmri-sequence-label {
            color: var(--az-match) !important;
            font-weight: 880 !important;
        }

        .current-fmri-grid {
            grid-template-columns: minmax(230px, 0.36fr) minmax(0, 1fr) !important;
            gap: 0.9rem !important;
            margin-top: 0.9rem !important;
        }

        .current-fmri-card {
            border-radius: 16px !important;
            border: 1px solid var(--az-line-soft) !important;
            background: #FFFFFF !important;
            padding: 0.75rem !important;
        }

        .current-fmri-note {
            justify-content: center !important;
            border: 1px solid var(--az-line-soft);
            border-radius: 16px;
            background: #F8FAFC;
            padding: 1rem 1.1rem !important;
        }

        .current-fmri-note strong {
            color: var(--az-ink) !important;
            font-size: 1rem !important;
            font-weight: 860 !important;
        }

        .current-fmri-note span {
            margin-top: 0.32rem;
            color: var(--az-ink-3) !important;
            font-size: 0.9rem !important;
            line-height: 1.55 !important;
        }

        .report-disclaimer {
            display: flex !important;
            gap: 0.65rem !important;
            align-items: flex-start !important;
            margin-top: 1rem !important;
            padding: 0.9rem 1rem !important;
            border-radius: 14px !important;
            background: #FFFDF7 !important;
            border: 1px solid #F2E4BC !important;
            color: #6B5A2F !important;
            font-size: 0.86rem !important;
            line-height: 1.55 !important;
            font-weight: 650 !important;
        }

        .report-disclaimer span:first-child {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 42px;
            height: 26px;
            border-radius: 999px;
            background: #FFF4D6;
            color: #8A5A00;
            font-size: 0.75rem;
            font-weight: 900;
        }

        @media screen and (max-width: 1024px) {
            .ai-summary-chip-row,
            .detail-summary-strip,
            .ai-flow-strip {
                grid-template-columns: 1fr 1fr !important;
            }

            .profile-compare-grid.refined {
                grid-template-columns: 1fr !important;
            }

            .profile-vs {
                margin: 0.1rem auto !important;
            }
        }

        @media screen and (max-width: 760px) {
            .ai-results-head,
            .detail-report-head {
                align-items: flex-start !important;
            }

            .ai-summary-chip-row,
            .detail-summary-strip,
            .ai-flow-strip,
            .result-meta-chip-row.compact,
            .current-fmri-grid {
                grid-template-columns: 1fr !important;
            }
        }


        /* -----------------------------
           후보 3명 카드 피드백 반영
           - 상세 리포트 버튼 한 줄 유지
           - 매칭 시점 / 보정 MMSE 정보 카드 구분감과 내부 여백 개선
        ----------------------------- */
        .result-meta-chip-row.compact {
            grid-template-columns: repeat(2, minmax(136px, 190px)) !important;
            gap: 0.62rem !important;
            margin-top: 0.72rem !important;
            /* 내부 정보 카드와 후보 카드의 바깥 하단 윤곽선 사이 여백 확보 */
            padding-bottom: 0.9rem !important;
        }

        .result-meta-chip {
            position: relative;
            min-height: 68px !important;
            padding: 0.72rem 0.82rem 0.98rem 0.9rem !important;
            border-radius: 14px !important;
            background: linear-gradient(180deg, #FFFFFF 0%, #F6FAFD 100%) !important;
            border: 1px solid #D4DEE9 !important;
            box-shadow:
                inset 0 1px 0 rgba(255, 255, 255, 0.92),
                0 8px 18px rgba(16, 24, 40, 0.045) !important;
            color: #526173 !important;
            line-height: 1.26 !important;
        }

        .result-meta-chip::before {
            content: "";
            position: absolute;
            left: 0;
            top: 11px;
            bottom: 11px;
            width: 3px;
            border-radius: 999px;
            background: linear-gradient(180deg, var(--az-brand), var(--az-match));
            opacity: 0.72;
        }

        .result-meta-chip b {
            margin-top: 0.26rem !important;
            color: #172033 !important;
            font-size: 0.96rem !important;
            line-height: 1.18 !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.similarity-card-marker) .stButton > button {
            min-height: 48px !important;
            padding: 0.68rem 0.88rem !important;
            white-space: nowrap !important;
            word-break: keep-all !important;
            line-height: 1.1 !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.similarity-card-marker) .stButton > button * {
            white-space: nowrap !important;
            word-break: keep-all !important;
            overflow-wrap: normal !important;
        }

        @media screen and (max-width: 760px) {
            .result-meta-chip-row.compact {
                grid-template-columns: 1fr !important;
            }

            div[data-testid="stVerticalBlockBorderWrapper"]:has(.similarity-card-marker) .stButton > button {
                white-space: normal !important;
            }

            div[data-testid="stVerticalBlockBorderWrapper"]:has(.similarity-card-marker) .stButton > button * {
                white-space: normal !important;
            }
        }


        /* -----------------------------
           상세 리포트 공통 증상 매칭 카드 피드백 반영
           - 공통 증상 내부 카드와 섹션 카드의 바깥 하단 윤곽선 사이 여백 확보
        ----------------------------- */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.detail-card-marker):has(.symptom-callout) {
            padding-bottom: 0.9rem !important;
        }

        .symptom-callout {
            margin-bottom: 0.9rem !important;
        }

        /* -----------------------------
           상세 리포트 환자 프로필 비교 피드백 반영
           - 비교 섹션의 존재감을 강화하고, 사례 일치율은 AI 분석 결과로 분리합니다.
           - EDU/MMSE/% placeholder처럼 보이던 요소는 의미형 텍스트 배지로 정리합니다.
        ----------------------------- */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.profile-compare-report-marker) {
            padding-bottom: 1rem !important;
            border: 1px solid rgba(20, 75, 116, 0.26) !important;
            background:
                radial-gradient(circle at 10% 0%, rgba(11, 111, 184, 0.09), transparent 30%),
                linear-gradient(180deg, #FFFFFF 0%, #F7FAFD 100%) !important;
            box-shadow: 0 18px 46px rgba(15, 23, 42, 0.105) !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.profile-compare-report-marker)::after {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            height: 5px;
            background: linear-gradient(90deg, var(--az-brand), var(--az-match));
            z-index: 2;
        }

        .profile-compare-report {
            display: flex !important;
            flex-direction: column !important;
            gap: 0.95rem !important;
            margin-bottom: 0.95rem !important;
        }

        .profile-match-summary {
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            gap: 1rem !important;
            padding: 1rem 1.15rem !important;
            border-radius: 18px !important;
            background:
                linear-gradient(135deg, rgba(8, 80, 137, 0.98) 0%, rgba(15, 143, 99, 0.92) 100%) !important;
            border: 1px solid rgba(9, 73, 119, 0.22) !important;
            box-shadow: 0 14px 30px rgba(7, 71, 113, 0.16) !important;
            color: #FFFFFF !important;
        }

        .profile-match-copy span {
            display: inline-flex !important;
            align-items: center !important;
            width: fit-content !important;
            margin-bottom: 0.3rem !important;
            padding: 0.24rem 0.5rem !important;
            border-radius: 999px !important;
            background: rgba(255, 255, 255, 0.16) !important;
            border: 1px solid rgba(255, 255, 255, 0.24) !important;
            color: rgba(255, 255, 255, 0.90) !important;
            font-size: 0.73rem !important;
            font-weight: 860 !important;
            letter-spacing: -0.01em !important;
        }

        .profile-match-copy strong {
            display: block !important;
            color: #FFFFFF !important;
            font-size: 1.05rem !important;
            font-weight: 900 !important;
            letter-spacing: -0.035em !important;
        }

        .profile-match-copy p {
            margin: 0.25rem 0 0 0 !important;
            color: rgba(255, 255, 255, 0.78) !important;
            font-size: 0.83rem !important;
            line-height: 1.48 !important;
            font-weight: 560 !important;
            word-break: keep-all !important;
        }

        .profile-match-score {
            min-width: 118px !important;
            padding: 0.72rem 0.9rem !important;
            border-radius: 18px !important;
            background: rgba(255, 255, 255, 0.96) !important;
            color: #0C6B4E !important;
            text-align: center !important;
            font-size: 1.55rem !important;
            line-height: 1 !important;
            font-weight: 950 !important;
            letter-spacing: -0.05em !important;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.95), 0 10px 22px rgba(4, 43, 72, 0.16) !important;
        }

        .profile-compare-report .profile-compare-grid.refined {
            grid-template-columns: minmax(0, 1fr) 48px minmax(0, 1fr) !important;
            gap: 0.95rem !important;
        }

        .profile-compare-report .profile-panel {
            border-radius: 18px !important;
            border: 1px solid #CAD8E6 !important;
            background: #FFFFFF !important;
            box-shadow: 0 10px 24px rgba(16, 24, 40, 0.055) !important;
        }

        .profile-compare-report .profile-panel.similar {
            border-color: rgba(15, 143, 99, 0.30) !important;
        }

        .profile-compare-report .profile-panel-head {
            padding: 0.84rem 1rem !important;
            background: linear-gradient(180deg, #EFF6FC 0%, #F8FBFE 100%) !important;
            border-bottom: 1px solid #D6E1EC !important;
            color: #163A5C !important;
            font-size: 0.92rem !important;
            font-weight: 900 !important;
            letter-spacing: -0.025em !important;
            text-align: left !important;
        }

        .profile-compare-report .profile-panel.similar .profile-panel-head {
            background: linear-gradient(180deg, #EAF8F1 0%, #F6FCF9 100%) !important;
            border-bottom-color: rgba(15, 143, 99, 0.20) !important;
            color: #075E43 !important;
        }

        .profile-compare-report .profile-row {
            min-height: 70px !important;
            padding: 0.92rem 1rem !important;
            gap: 0.82rem !important;
            border-top: 1px solid #E1E9F1 !important;
            background: #FFFFFF !important;
        }

        .profile-compare-report .profile-row:first-of-type {
            border-top: none !important;
        }

        .profile-compare-report .profile-row .profile-field-badge {
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 46px !important;
            min-width: 46px !important;
            height: 30px !important;
            border-radius: 999px !important;
            background: #EAF2FA !important;
            color: #23506F !important;
            border: 1px solid #D3E0EB !important;
            font-size: 0.76rem !important;
            font-weight: 900 !important;
            letter-spacing: -0.025em !important;
        }

        .profile-compare-report .profile-row .profile-field-badge.cognitive {
            background: #EEF8F4 !important;
            color: #0A6A4C !important;
            border-color: rgba(15, 143, 99, 0.22) !important;
        }

        .profile-compare-report .profile-row span:not(.profile-field-badge) {
            color: #5C6B7D !important;
            font-size: 0.77rem !important;
            font-weight: 780 !important;
        }

        .profile-compare-report .profile-row strong {
            margin-top: 0.16rem !important;
            color: #172033 !important;
            font-size: 1.08rem !important;
            font-weight: 900 !important;
            letter-spacing: -0.035em !important;
        }

        .profile-compare-report .profile-vs {
            align-self: center !important;
            width: 48px !important;
            height: 48px !important;
            background: #172033 !important;
            border: 3px solid #FFFFFF !important;
            color: #FFFFFF !important;
            box-shadow: 0 10px 22px rgba(16, 24, 40, 0.18) !important;
        }

        @media screen and (max-width: 1024px) {
            .profile-compare-report .profile-compare-grid.refined {
                grid-template-columns: 1fr !important;
            }

            .profile-match-summary {
                align-items: flex-start !important;
                flex-direction: column !important;
            }

            .profile-match-score {
                width: 100% !important;
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
    """화면 이동을 처리합니다.

    상세 리포트는 특정 환자/진단 결과에 종속되므로, 화면을 이동할 때
    이전 페이지에서 열려 있던 상세 분석 상태가 다음 화면에 남지 않도록 초기화합니다.
    """
    st.session_state["page"] = page

    if patient_id is not None:
        st.session_state["selected_patient_id"] = patient_id

    if clear_latest_result:
        st.session_state["latest_diagnosis_result"] = None
        st.session_state["latest_diagnosis_patient_id"] = None

    st.session_state["selected_detail"] = None
    st.session_state["selected_detail_patient_id"] = None
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
        account_id = st.text_input("아이디", placeholder="아이디를 입력하세요", key="login_account_id")
        password = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요", key="login_password")
        submitted = st.form_submit_button(
            "로그인",
            width="stretch",
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
    if st.button("의료진 계정 생성하기", width="stretch", key="go_to_signup_page"):
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
            if st.button("의료진 코드 승인", width="stretch", type="primary", key="approve_clinician_code"):
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
        if st.button("코드 다시 입력", width="stretch", key="reset_signup_code"):
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

    if st.button("계정 생성", width="stretch", type="primary", key="create_clinician_account"):
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
        if st.button("← 로그인으로 돌아가기", width="stretch", key="back_to_login_page"):
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
        if st.button("＋ 프로필 추가", width="stretch", type="primary", key="main_add_patient_button"):
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

            if cols[3].button("상세 보기", key=f"detail_{patient['id']}", width="stretch"):
                navigate("patient_detail", patient["id"])

            if cols[4].button("AI 진단", key=f"diagnosis_{patient['id']}", width="stretch", type="primary"):
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

            submitted = st.form_submit_button("저장", width="stretch", type="primary")

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
        if st.button("← 환자 상세로 돌아가기", width="stretch", key=f"edit_back_detail_{patient['id']}"):
            navigate("patient_detail", patient["id"], clear_latest_result=False)
    with col_detail:
        if st.button("환자 목록", width="stretch", key="edit_back_to_main"):
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

            submitted = st.form_submit_button("변경사항 저장", width="stretch", type="primary")

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

    # 과거 진단 이력에서 상세 리포트를 다시 열 때도 현재 환자의 프로필을
    # 상세 리포트 컴포넌트가 참조할 수 있도록 항상 동기화합니다.
    st.session_state["patient_profile"] = {
        "id": patient["id"],
        "name": patient["name"],
        "birthdate": format_date(patient["birthdate"]),
        "gender": patient["gender"],
        "education": patient["education"],
    }

    show_hero(
        "환자 상세 정보",
        "환자의 기본 프로필과 과거 AI 진단 지원 이력을 확인합니다.",
    )

    if st.session_state.get("patient_updated_flash"):
        st.success("환자 기본정보가 수정되었습니다.")
        st.session_state["patient_updated_flash"] = False

    col_back, col_diag, col_edit, col_delete = st.columns([1, 1, 1, 1])
    with col_back:
        if st.button("← 환자 목록", width="stretch", key=f"diagnosis_back_main_{patient['id']}"):
            navigate("main")
    with col_diag:
        if st.button("AI 진단 실행", width="stretch", type="primary", key=f"detail_ai_diagnosis_{patient['id']}"):
            navigate("ai_diagnosis", patient["id"])
    with col_edit:
        if st.button("기본정보 수정", width="stretch", key=f"edit_profile_{patient['id']}"):
            navigate("edit_patient", patient["id"], clear_latest_result=False)
    with col_delete:
        if st.button("프로필 삭제", width="stretch", key=f"request_delete_{patient['id']}"):
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
                if st.button("삭제 취소", width="stretch", key=f"cancel_delete_{patient['id']}"):
                    st.session_state["delete_confirm_patient_id"] = None
                    st.rerun()
            with delete_col:
                if st.button("프로필 영구 삭제", width="stretch", key=f"delete_patient_{patient['id']}"):
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
                st.dataframe(df_summary, width="stretch", hide_index=True)
                
                # 상세 분석 결과가 있다면 다시 보기 버튼 제공
                if st.button("이 결과 상세 분석 다시 보기", key=f"hist_review_{patient['id']}_{idx}"):
                    # 과거 이력에서도 AI 진단 직후와 동일한 상세 리포트 컴포넌트를 재사용합니다.
                    # 이때 현재 환자 프로필과 선택된 상세 결과의 소유 환자 ID를 함께 저장해야
                    # 리런 이후에도 올바른 환자 기준으로 리포트가 다시 렌더링됩니다.
                    st.session_state["patient_profile"] = {
                        "id": patient["id"],
                        "name": patient["name"],
                        "birthdate": format_date(patient["birthdate"]),
                        "gender": patient["gender"],
                        "education": patient["education"],
                    }
                    st.session_state["selected_detail"] = similar_patients[0]
                    st.session_state["selected_detail_patient_id"] = patient["id"]
                    st.rerun()

    selected_detail = st.session_state.get("selected_detail")
    selected_detail_patient_id = st.session_state.get("selected_detail_patient_id")

    if selected_detail is not None and selected_detail_patient_id == patient["id"]:
        render_detail_view(selected_detail)

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
        if st.button("← 환자 목록", width="stretch", key=f"diagnosis_back_main_{patient['id']}"):
            navigate("main")
    with col_detail:
        if st.button("환자 상세 보기", width="stretch", key=f"diagnosis_patient_detail_{patient['id']}"):
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
            st.image(fmri_file, caption=f"업로드된 fMRI 이미지: {fmri_file.name}", width="stretch")

        if st.button("진단 실행", type="primary", width="stretch", key=f"run_diagnosis_{patient['id']}"):
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
            st.session_state["selected_detail"] = None
            st.session_state["selected_detail_patient_id"] = None

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
def _display_value(value, fallback="-"):
    """None/빈 값이 화면에 그대로 노출되지 않도록 표시값을 정리합니다."""
    if value is None:
        return fallback
    if isinstance(value, float) and pd.isna(value):
        return fallback
    text_value = str(value).strip()
    return text_value if text_value else fallback


def _to_float(value, fallback=0.0):
    """문자/숫자 혼합 입력을 안전하게 float로 변환합니다."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def _format_similarity(value):
    """일치율 값을 소수점 한 자리 퍼센트 문자열로 통일합니다."""
    return f"{_to_float(value):.1f}%"


def _education_label(level):
    """AI 엔진의 학력 레벨 숫자를 사용자 표시용 문자열로 변환합니다."""
    if level == 2:
        return "고"
    if level == 1:
        return "중"
    return "저"


def _join_symptoms(symptoms, fallback="공통 증상 없음"):
    """증상 코드 리스트를 화면 표시 문자열로 변환합니다."""
    if not symptoms:
        return fallback
    return ", ".join(str(symptom) for symptom in symptoms)


def _image_exists(path):
    """로컬 이미지 경로가 실제로 존재하는지 확인합니다."""
    if not path:
        return False
    try:
        return Path(str(path)).exists()
    except (TypeError, OSError):
        return False


def _image_data_uri(path):
    """로컬 이미지 파일을 HTML img 태그에서 사용할 수 있는 data URI로 변환합니다."""
    if not _image_exists(path):
        return None
    try:
        image_path = Path(str(path))
        suffix = image_path.suffix.lower()
        mime_type = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
        }.get(suffix, "image/png")
        encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
        return f"data:{mime_type};base64,{encoded}"
    except Exception:
        return None


def _fmri_image_html(path, label, class_name="fmri-mini-image"):
    """fMRI 이미지를 HTML 카드 내부에 안정적으로 삽입합니다."""
    data_uri = _image_data_uri(path)
    if data_uri:
        return f'<img src="{data_uri}" alt="{safe_text(label)}" class="{safe_text(class_name)}" />'
    return (
        f'<div class="fmri-mini-placeholder">{safe_text(label)}<br/>'
        '<span style="font-size:0.68rem; font-weight:700;">이미지 없음</span></div>'
    )


def _render_image_or_placeholder(path, label="fMRI 이미지"):
    """fMRI 이미지가 없는 개발/검수 환경에서도 화면이 깨지지 않도록 대체 카드를 표시합니다."""
    if _image_exists(path):
        st.image(str(path), width="stretch")
    else:
        st.markdown(
            f"""
            <div class="fmri-placeholder">
                {safe_text(label)}<br/>
                <span style="font-size:0.76rem; font-weight:700;">이미지 경로를 확인할 수 없습니다.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_section_title(number, title, icon=""):
    """상세 리포트 섹션 타이틀을 통일된 스타일로 렌더링합니다."""
    st.markdown(
        f"""
        <div class="section-title-row">
            <span class="section-num">{safe_text(str(number).zfill(2))}</span>
            <h3>{safe_text(title)}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_diagnosis_result(results_data):
    """
    AI 진단 직후의 유사 사례 결과 리스트를 렌더링합니다.
    기존 상세 분석 이동 기능은 유지하면서 카드 간격과 정보 위계를 더 안정적으로 정리했습니다.
    """
    results = results_data.get("similar_patients", [])
    diagnosis_datetime = results_data.get("diagnosis_datetime", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    if not results:
        st.warning("유사한 환자 사례를 찾을 수 없습니다.")
        return

    max_similarity = max(
        (_to_float(item.get("summary", {}).get("similarity")) for item in results),
        default=0.0,
    )

    st.markdown(
        f"""
        <div class="ai-results-head">
            <div class="ai-head-icon">AI</div>
            <div>
                <div class="ai-eyebrow">AI Similarity Matching</div>
                <h2>유사 사례 분석 결과</h2>
                <p>현재 환자의 입력 정보를 기준으로 가장 유사한 기존 사례를 정렬했습니다. 상세 리포트에서 근거 데이터를 확인할 수 있습니다.</p>
            </div>
        </div>
        <div class="ai-flow-strip">
            <div class="ai-flow-step" data-step="01"><b>입력 정보 확인</b><span>증상, MMSE, fMRI 입력값 저장</span></div>
            <div class="ai-flow-step active" data-step="02"><b>유사 사례 매칭</b><span>일치율 기준으로 후보 사례 정렬</span></div>
            <div class="ai-flow-step" data-step="03"><b>상세 리포트 확인</b><span>프로필, 증상, 추이, fMRI 대조</span></div>
        </div>
        <div class="ai-summary-chip-row">
            <div class="ai-summary-chip"><span>매칭 후보</span><strong>{len(results)}건</strong></div>
            <div class="ai-summary-chip is-primary"><span>최고 일치율</span><strong>{max_similarity:.1f}%</strong></div>
            <div class="ai-summary-chip"><span>분석 완료</span><strong>{safe_text(diagnosis_datetime)}</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for idx, item in enumerate(results):
        summary = item.get("summary", {})
        symptoms = item.get("symptoms", {})
        ptid = _display_value(summary.get("ptid"), "Unknown")
        similarity_text = _format_similarity(summary.get("similarity"))
        matched_month = _display_value(summary.get("matched_month"))
        mmse = _display_value(summary.get("mmse"))
        is_best = idx == 0

        with st.container(border=True):
            st.markdown(
                f"<span class='similarity-card-marker {'best' if is_best else ''}'></span>",
                unsafe_allow_html=True,
            )
            rank_col, info_col, score_col, action_col = st.columns([0.62, 4.05, 0.95, 1.32], gap="medium")

            with rank_col:
                st.markdown(
                    f"""
                    <div class="result-rank-badge {'best' if is_best else ''}">{idx + 1}</div>
                    """,
                    unsafe_allow_html=True,
                )

            with info_col:
                st.markdown(
                    f"""
                    <div class="result-patient-title">환자 {safe_text(ptid)}</div>
                    <div class="result-patient-subtitle">유사 사례 후보 #{idx + 1}</div>
                    <div class="result-meta-chip-row compact">
                        <span class="result-meta-chip">매칭 시점 <b>{safe_text(matched_month)}개월 차</b></span>
                        <span class="result-meta-chip">보정 MMSE <b>{safe_text(mmse)}점</b></span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with score_col:
                st.markdown(
                    f"""
                    <div class="result-score-pill">
                        <strong>{safe_text(similarity_text)}</strong>
                        <span>일치율</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with action_col:
                unique_key = f"detail_{idx}_{ptid}"
                if st.button("상세 리포트 보기", key=unique_key, width="stretch"):
                    st.session_state["selected_detail"] = item
                    st.session_state["selected_detail_patient_id"] = (
                        st.session_state.get("latest_diagnosis_patient_id")
                        or st.session_state.get("selected_patient_id")
                    )
                    st.rerun()

    selected_detail = st.session_state.get("selected_detail")
    selected_detail_patient_id = st.session_state.get("selected_detail_patient_id")
    current_patient_id = st.session_state.get("latest_diagnosis_patient_id") or st.session_state.get("selected_patient_id")

    if selected_detail is not None and selected_detail_patient_id == current_patient_id:
        render_detail_view(selected_detail)


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
            width="stretch",
            type="primary" if current_page == "main" else "secondary",
            key="sidebar_main",
        ):
            navigate("main")

        if st.button(
            "프로필 추가",
            width="stretch",
            type="primary" if current_page == "add_patient" else "secondary",
            key="sidebar_add_patient",
        ):
            navigate("add_patient")

        

        if st.button("로그아웃", width="stretch", key="sidebar_logout"):
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
    기존 정보와 동작은 유지하고, 좁은 카드 중첩을 줄여 가독성을 높였습니다.
    """
    if res is None:
        return

    summary = res.get("summary", {})
    symptoms = res.get("symptoms", {})
    mmse_chart = res.get("mmse_chart", {})
    fmri_display = res.get("fmri_display", {})

    ptid = _display_value(summary.get("ptid"), "Unknown")
    similarity_text = _format_similarity(summary.get("similarity"))
    matched_month = _display_value(summary.get("matched_month"))
    similar_mmse = _display_value(summary.get("mmse"))
    similar_education = _education_label(summary.get("edu_level"))
    common_text = _join_symptoms(symptoms.get("common", []))
    input_profile = st.session_state.get("patient_profile", {})
    input_education = _display_value(input_profile.get("education"), "미설정")
    input_mmse = _display_value(mmse_chart.get("input_patient_score"))

    st.markdown("---")

    top_left, top_right = st.columns([5.2, 1])
    with top_left:
        st.markdown("<div class='detail-topbar'>← 유사 사례 분석 결과</div>", unsafe_allow_html=True)
    with top_right:
        if st.button("리포트 닫기", width="stretch", key=f"close_detail_{ptid}"):
            st.session_state["selected_detail"] = None
            st.session_state["selected_detail_patient_id"] = None
            st.rerun()

    st.markdown(
        f"""
        <div class="detail-report-head">
            <div class="detail-head-icon">RPT</div>
            <div>
                <div class="detail-eyebrow">Case Analysis Report</div>
                <h2>환자 {safe_text(ptid)} 사례 상세 분석 리포트</h2>
                <p>진단 중인 환자와 선택된 유사 사례의 프로필, 공통 증상, 인지 기능 변화, fMRI 정보를 동일한 흐름으로 대조합니다.</p>
            </div>
        </div>
        <div class="detail-summary-strip">
            <div class="detail-summary-chip is-primary"><span>사례 일치율</span><strong>{safe_text(similarity_text)}</strong></div>
            <div class="detail-summary-chip"><span>매칭 시점</span><strong>{safe_text(matched_month)}개월 차</strong></div>
            <div class="detail-summary-chip"><span>보정 MMSE</span><strong>{safe_text(similar_mmse)}점</strong></div>
            <div class="detail-summary-chip"><span>공통 증상</span><strong>{safe_text(common_text)}</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown("<span class='detail-card-marker profile-compare-report-marker'></span>", unsafe_allow_html=True)
        _render_section_title("1", "환자 프로필 비교")
        st.markdown(
            f"""
            <div class="profile-compare-report">
                <div class="profile-match-summary">
                    <div class="profile-match-copy">
                        <span>AI 분석 결과</span>
                        <strong>사례 일치율</strong>
                        <p>두 환자의 프로필·증상·매칭 시점 정보를 종합해 계산한 유사도입니다.</p>
                    </div>
                    <div class="profile-match-score">{safe_text(similarity_text)}</div>
                </div>
                <div class="profile-compare-grid refined">
                    <div class="profile-panel">
                        <div class="profile-panel-head">진단 중인 환자</div>
                        <div class="profile-row">
                            <span class="profile-field-badge">학력</span>
                            <div><span>학력 수준</span><strong>{safe_text(input_education)}</strong></div>
                        </div>
                        <div class="profile-row">
                            <span class="profile-field-badge cognitive">인지</span>
                            <div><span>보정 MMSE</span><strong>{safe_text(input_mmse)}점</strong></div>
                        </div>
                    </div>
                    <div class="profile-vs">VS</div>
                    <div class="profile-panel similar">
                        <div class="profile-panel-head">유사 환자 {safe_text(ptid)}</div>
                        <div class="profile-row">
                            <span class="profile-field-badge">학력</span>
                            <div><span>학력 수준</span><strong>{safe_text(similar_education)}</strong></div>
                        </div>
                        <div class="profile-row">
                            <span class="profile-field-badge cognitive">인지</span>
                            <div><span>매칭 시점 MMSE</span><strong>{safe_text(similar_mmse)}점</strong></div>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with st.container(border=True):
        st.markdown("<span class='detail-card-marker'></span>", unsafe_allow_html=True)
        _render_section_title("2", "공통 증상 매칭")
        if symptoms.get("common", []):
            st.markdown(
                f"""
                <div class="symptom-callout">
                    <div class="symptom-callout-icon">공통</div>
                    <div>
                        <span>두 환자에게서 공통으로 나타나는 주요 증상</span>
                        <strong>{safe_text(common_text)}</strong>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.info("공통으로 나타나는 신체/행동 증상이 없습니다.")

    with st.container(border=True):
        st.markdown("<span class='report-section-marker'></span>", unsafe_allow_html=True)
        _render_section_title("3", "인지 기능 진행 추이 (MMSE)")
        st.markdown(
            "<p class='chart-caption'>유사 환자의 전체 방문 이력 중 현재 환자와 가장 일치하는 시점을 표시합니다.</p>",
            unsafe_allow_html=True,
        )

        history_data = mmse_chart.get("similar_patient_history", [])
        df_history = pd.DataFrame(history_data)
        if not df_history.empty:
            rename_map = {
                "MONTHS": "Month",
                "ADJUSTED_MMSE": "MMSE",
                "months": "Month",
                "mmse": "MMSE",
            }
            df_history = df_history.rename(columns=rename_map)

        if df_history.empty or not {"Month", "MMSE"}.issubset(df_history.columns):
            st.info("MMSE 진행 추이 데이터가 없습니다.")
        else:
            df_history = df_history[["Month", "MMSE"]].sort_values("Month")
            try:
                import altair as alt

                base = alt.Chart(df_history).encode(
                    x=alt.X("Month:Q", title="경과 시간 (개월)", axis=alt.Axis(labelFlush=False)),
                    y=alt.Y("MMSE:Q", title="MMSE (점)", scale=alt.Scale(domain=[0, 35])),
                )
                line = base.mark_line(point=True, strokeWidth=3).encode(
                    tooltip=[
                        alt.Tooltip("Month:Q", title="개월"),
                        alt.Tooltip("MMSE:Q", title="MMSE"),
                    ]
                )
                labels = base.mark_text(dy=-14, fontSize=12, fontWeight="bold").encode(text="MMSE:Q")
                matched_df = df_history[df_history["Month"] == _to_float(summary.get("matched_month"), -1)]
                chart = line + labels
                if not matched_df.empty:
                    matched_rule = alt.Chart(matched_df).mark_rule(strokeDash=[5, 5]).encode(x="Month:Q")
                    matched_point = alt.Chart(matched_df).mark_point(size=150, filled=True).encode(
                        x="Month:Q",
                        y="MMSE:Q",
                        tooltip=[
                            alt.Tooltip("Month:Q", title="매칭 시점"),
                            alt.Tooltip("MMSE:Q", title="MMSE"),
                        ],
                    )
                    chart = chart + matched_rule + matched_point

                st.altair_chart(chart.properties(height=300), width="stretch")
            except Exception:
                st.line_chart(df_history.set_index("Month"))

    with st.container(border=True):
        st.markdown("<span class='report-section-marker'></span>", unsafe_allow_html=True)
        _render_section_title("4", "fMRI 시각적 유사성 대조")
        st.markdown(
            "<p class='fmri-caption'>유사 환자의 상태 변화 이미지와 진단 환자의 현재 영상을 대조합니다.</p>",
            unsafe_allow_html=True,
        )

        sequence = fmri_display.get("sequence", {}) or {}
        paths = sequence.get("paths", []) or []
        months = sequence.get("months", []) or []
        matched_idx = sequence.get("matched_idx", None)
        input_fmri = fmri_display.get("input_fmri")

        if not paths:
            st.info("유사 환자의 fMRI 시퀀스 데이터가 없습니다.")
        else:
            cards = []
            for i, path in enumerate(paths):
                month_label = months[i] if i < len(months) else "-"
                is_matched = i == matched_idx
                badge = "<div class='fmri-match-badge'>최대 유사 지점</div>" if is_matched else "<div class='fmri-match-spacer'></div>"
                matched_class = " matched" if is_matched else ""
                cards.append(
                    f'<div class="fmri-sequence-card{matched_class}">'
                    f'{badge}'
                    f'{_fmri_image_html(path, f"유사환자 ({month_label}m)")}'
                    f'<div class="fmri-sequence-label">유사환자 ({safe_text(month_label)}m)</div>'
                    f'</div>'
                )

            current_img_html = _fmri_image_html(input_fmri, "현재 진단 환자", "current-fmri-image")
            fmri_html = (
                '<div class="fmri-sequence-grid">'
                + ''.join(cards)
                + '</div>'
                + '<div class="current-fmri-grid">'
                + '<div class="current-fmri-card">'
                + current_img_html
                + '<div class="fmri-sequence-label current">현재 진단 환자</div>'
                + '</div>'
                + '<div class="current-fmri-note">'
                + '<strong>현재 진단 환자</strong>'
                + f'<span>유사 환자의 {safe_text(matched_month)}개월 차 시점과 가장 높은 시각적 유사성을 보입니다.</span>'
                + '</div>'
                + '</div>'
            )
            st.markdown(fmri_html, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="report-disclaimer">
            <span>주의</span>
            <span>본 리포트는 인공지능 기반 분석 결과로, 임상적 판단은 반드시 전문의의 종합적인 평가를 통해 이루어져야 합니다.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
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

    if 'selected_detail_patient_id' not in st.session_state:
        st.session_state['selected_detail_patient_id'] = None
        
    init_session_state()
    apply_custom_css()

    if not st.session_state["logged_in"]:
        login_page()
        return

    render_authenticated_page()


if __name__ == "__main__":
    main()
