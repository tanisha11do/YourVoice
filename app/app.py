
import streamlit as st
from datetime import datetime

from supabase_client import create_supabase_client
from calle_client import start_call, process_completed_call


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="YourVoice",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# STYLING
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: #f4f0e8;
        color: #25272b;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #f8f5ee;
        border-right: 1px solid #e7e0d4;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.2rem;
    }

    .brand {
        font-size: 21px;
        font-weight: 700;
        padding: 0.4rem 0 1.5rem 0.4rem;
        color: #202226;
    }

    .brand-dot {
        display: inline-flex;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background: #24272b;
        color: #ffd83d;
        align-items: center;
        justify-content: center;
        margin-right: 9px;
        font-size: 15px;
    }

    .sidebar-label {
        color: #99958d;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin: 1.2rem 0 0.5rem 0.4rem;
    }

    /* Hide Streamlit chrome */
    #MainMenu, footer {
        visibility: hidden;
    }

    .block-container {
        max-width: 1450px;
        padding: 2rem 3rem 3rem 2rem;
    }

    /* Top header */
    .top-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.5rem;
    }

    .greeting {
        font-size: 29px;
        font-weight: 700;
        color: #222428;
        line-height: 1.1;
    }

    .sub-greeting {
        margin-top: 6px;
        color: #8e8a83;
        font-size: 13px;
    }

    /* Cards */
    .card {
        background: #fffdf9;
        border-radius: 22px;
        padding: 22px;
        border: 1px solid #ece5d9;
        box-shadow: 0 3px 14px rgba(50, 45, 35, 0.035);
        min-height: 130px;
    }

    .dark-card {
        background: #272a2f;
        color: white;
        border-radius: 22px;
        padding: 23px;
        min-height: 130px;
    }

    .cream-card {
        background: #d8d0be;
        border-radius: 22px;
        padding: 25px;
        min-height: 250px;
    }

    .card-title {
        font-size: 13px;
        font-weight: 600;
        color: #67635c;
        margin-bottom: 12px;
    }

    .dark-card .card-title {
        color: #d5d5d2;
    }

    .big-number {
        font-size: 34px;
        font-weight: 700;
        color: #25272b;
    }

    .dark-card .big-number {
        color: white;
    }

    .metric-caption {
        color: #99958d;
        font-size: 11px;
        margin-top: 5px;
    }

    .pill {
        display: inline-block;
        padding: 5px 9px;
        border-radius: 999px;
        font-size: 10px;
        font-weight: 600;
        background: #f0eee8;
        color: #6e6a63;
    }

    .yellow {
        background: #ffd83d;
        color: #25272b;
    }

    .coral {
        background: #ff7e69;
        color: white;
    }

    .green {
        background: #c8dfb7;
        color: #34522d;
    }

    /* Section headings */
    .section-heading {
        font-size: 17px;
        font-weight: 700;
        margin: 0.2rem 0 0.75rem 0;
        color: #25272b;
    }

    .section-sub {
        color: #96918a;
        font-size: 11px;
        margin-top: -5px;
        margin-bottom: 12px;
    }

    /* Issue rows */
    .issue-row {
        display: flex;
        align-items: center;
        gap: 12px;
        background: #fffdf9;
        border: 1px solid #eee8df;
        border-radius: 15px;
        padding: 12px 14px;
        margin-bottom: 8px;
    }

    .issue-icon {
        width: 35px;
        height: 35px;
        border-radius: 50%;
        background: #f1eee6;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
    }

    .issue-name {
        font-size: 12px;
        font-weight: 600;
    }

    .issue-detail {
        color: #96918a;
        font-size: 10px;
    }

    .severity-high {
        color: #d95445;
        background: #ffe1db;
        padding: 4px 8px;
        border-radius: 999px;
        font-size: 9px;
        font-weight: 700;
    }

    .severity-medium {
        color: #927400;
        background: #fff1b6;
        padding: 4px 8px;
        border-radius: 999px;
        font-size: 9px;
        font-weight: 700;
    }

    .severity-low {
        color: #43703a;
        background: #dcefd3;
        padding: 4px 8px;
        border-radius: 999px;
        font-size: 9px;
        font-weight: 700;
    }

    /* Call panel */
    .call-panel {
        background: #fffdf9;
        border-radius: 22px;
        padding: 22px;
        border: 1px solid #ece5d9;
    }

    /* Progress */
    .progress-bg {
        height: 7px;
        background: #ebe7de;
        border-radius: 20px;
        overflow: hidden;
        margin-top: 8px;
    }

    .progress-fill {
        height: 100%;
        border-radius: 20px;
        background: #ff7e69;
    }

    /* Streamlit buttons */
    .stButton > button {
        border-radius: 999px;
        border: none;
        background: #272a2f;
        color: white;
        font-weight: 600;
        padding: 0.55rem 1.15rem;
    }

    .stButton > button:hover {
        background: #3a3d42;
        color: white;
    }

    /* Inputs */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        border-radius: 12px !important;
        background: #fffdf9 !important;
        border-color: #e6dfd4 !important;
    }

    /* Tables */
    [data-testid="stDataFrame"] {
        border-radius: 15px;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_resource
def get_supabase():
    return create_supabase_client()


def get_campaigns(client):
    response = (
        client
        .table("campaigns")
        .select("id,name")
        .order("name")
        .execute()
    )
    return response.data or []


def get_calls(client, campaign_id=None):
    query = (
        client
        .table("calls")
        .select("*")
        .order("created_at", desc=True)
        .limit(100)
    )

    if campaign_id:
        query = query.eq("campaign_id", campaign_id)

    return query.execute().data or []


def get_issues(client, call_ids=None):
    query = (
        client
        .table("issues")
        .select("*")
        .limit(500)
    )

    if call_ids:
        query = query.in_("call_id", call_ids)

    return query.execute().data or []


supabase = get_supabase()

try:
    campaigns = get_campaigns(supabase)
except Exception as e:
    campaigns = []
    st.error(f"Could not load campaigns: {e}")



with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <span class="brand-dot">◉</span>YourVoice
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-label">Workspace</div>', unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["Overview", "Campaigns", "Calls", "Issues"],
        label_visibility="collapsed",
    )

    st.markdown('<div class="sidebar-label">Actions</div>', unsafe_allow_html=True)

    if st.button("＋  Start new call", use_container_width=True):
        st.session_state["show_call_form"] = True

    st.markdown("<br>", unsafe_allow_html=True)

    st.caption("YourVoice")
    st.caption("Community needs assessment")


# ---------------------------------------------------------
# CAMPAIGN SELECTION
# ---------------------------------------------------------

campaign_options = {c["name"]: c["id"] for c in campaigns}

if campaign_options:
    selected_campaign_name = st.selectbox(
        "Campaign",
        list(campaign_options.keys()),
        label_visibility="collapsed",
    )
    selected_campaign_id = campaign_options[selected_campaign_name]
else:
    selected_campaign_name = None
    selected_campaign_id = None


try:
    calls = get_calls(supabase, selected_campaign_id)
    call_ids = [c["id"] for c in calls if c.get("id")]
    issues = get_issues(supabase, call_ids)
except Exception as e:
    calls = []
    issues = []
    st.error(f"Could not load dashboard data: {e}")


completed_calls = [c for c in calls if c.get("status") == "completed"]
followups = [c for c in calls if str(c.get("follow_up_requested")).lower() == "yes"]
people_needing_help = [c for c in calls if str(c.get("needs_help")).lower() == "yes"]

completion_rate = (
    round((len(completed_calls) / len(calls)) * 100)
    if calls else 0
)



col_header, col_search, col_action = st.columns([4, 2, 1])

with col_header:
    st.markdown(
        """
        <div class="greeting">Hi, YourVoice 👋</div>
        <div class="sub-greeting">
            Let's take a look at your community outreach today
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_search:
    st.text_input(
        "Search",
        placeholder="⌕  Search calls or issues",
        label_visibility="collapsed",
    )

with col_action:
    st.write("")
    if st.button("＋ New call"):
        st.session_state["show_call_form"] = True


if st.session_state.get("show_call_form", False):
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="call-panel">
            <div class="section-heading">Start community outreach</div>
            <div class="section-sub">
                Select a campaign and enter the recipient's phone number.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([2, 2, 1])

    with c1:
        call_campaign_name = st.selectbox(
            "Campaign",
            list(campaign_options.keys()) if campaign_options else [],
            key="call_campaign",
        )

    with c2:
        phone_number = st.text_input(
            "Phone number",
            placeholder="+91XXXXXXXXXX",
        )

    with c3:
        st.write("")
        st.write("")
        if st.button("Start call", type="primary"):
            if not phone_number:
                st.warning("Enter a phone number.")
            elif not campaign_options:
                st.warning("No campaign is available.")
            else:
                selected_id = campaign_options[call_campaign_name]

                try:
                    response = start_call(
                        phone_number=phone_number,
                        campaign_id=selected_id,
                    )

                    call_id = response.get("id") if isinstance(response, dict) else None

                    st.success("CALL-E outreach started.")

                    if call_id:
                        st.code(call_id, language="text")

                    st.session_state["show_call_form"] = False

                except Exception as e:
                    st.error(f"Could not start the call: {e}")



st.markdown("<br>", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">Calls today</div>
            <div class="big-number">{len(calls)}</div>
            <div class="metric-caption">Total calls in selected campaign</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m2:
    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">Issues reported</div>
            <div class="big-number">{len(issues)}</div>
            <div class="metric-caption">Across completed calls</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m3:
    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">Follow-ups</div>
            <div class="big-number">{len(followups)}</div>
            <div class="metric-caption">Community members requesting follow-up</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m4:
    st.markdown(
        f"""
        <div class="dark-card">
            <div class="card-title">Completion rate</div>
            <div class="big-number">{completion_rate}%</div>
            <div class="progress-bg">
                <div class="progress-fill" style="width:{completion_rate}%"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )



st.markdown("<br>", unsafe_allow_html=True)

left, right = st.columns([1.35, 1])

with left:
    st.markdown('<div class="section-heading">Outreach overview</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">A quick view of the selected campaign</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="cream-card">
            <div style="font-size:13px;font-weight:600;color:#625d54;">
                Selected campaign
            </div>

            <div style="font-size:25px;font-weight:700;margin-top:15px;color:#25272b;">
                {selected_campaign_name or "No campaign selected"}
            </div>

            <div style="margin-top:28px;display:flex;gap:45px;">
                <div>
                    <div style="font-size:25px;font-weight:700;">{len(completed_calls)}</div>
                    <div style="font-size:10px;color:#777168;">Completed</div>
                </div>
                <div>
                    <div style="font-size:25px;font-weight:700;">{len(people_needing_help)}</div>
                    <div style="font-size:10px;color:#777168;">Need help</div>
                </div>
                <div>
                    <div style="font-size:25px;font-weight:700;">{len(followups)}</div>
                    <div style="font-size:10px;color:#777168;">Follow-up</div>
                </div>
            </div>

            <div style="margin-top:30px;">
                <span class="pill yellow">LIVE CAMPAIGN</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with right:
    st.markdown('<div class="section-heading">Issue categories</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Most frequently reported community needs</div>',
        unsafe_allow_html=True,
    )

    category_counts = {}
    for issue in issues:
        category = issue.get("category", "other").title()
        category_counts[category] = category_counts.get(category, 0) + 1

    icons = {
        "Electricity": "⚡",
        "Water": "💧",
        "Employment": "💼",
        "Food": "🍚",
        "Housing": "⌂",
        "Transport": "🚌",
        "Other": "●",
    }

    if category_counts:
        for category, count in sorted(
            category_counts.items(),
            key=lambda x: x[1],
            reverse=True,
        ):
            icon = icons.get(category, "●")
            st.markdown(
                f"""
                <div class="issue-row">
                    <div class="issue-icon">{icon}</div>
                    <div style="flex:1">
                        <div class="issue-name">{category}</div>
                        <div class="issue-detail">{count} reported issue(s)</div>
                    </div>
                    <span class="pill">{count}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No issues reported yet.")



st.markdown("<br>", unsafe_allow_html=True)

st.markdown('<div class="section-heading">Recent outreach</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-sub">Latest community conversations</div>',
    unsafe_allow_html=True,
)

if calls:
    rows = []

    for call in calls[:8]:
        rows.append(
            {
                "Phone": call.get("phone", "—"),
                "Status": call.get("status", "—"),
                "Needs help": call.get("needs_help", "—"),
                "Follow-up": call.get("follow_up_requested", "—"),
                "Call-E ID": call.get("calle_call_id", "—"),
            }
        )

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True,
    )
else:
    st.markdown(
        """
        <div class="card">
            <div style="font-size:13px;font-weight:600;">
                No calls yet
            </div>
            <div class="metric-caption">
                Start your first community outreach call using “New call”.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown("<br>", unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="section-heading">High-priority issues</div>', unsafe_allow_html=True)

    high_issues = [
        i for i in issues
        if str(i.get("severity", "")).lower() == "high"
    ]

    if high_issues:
        for issue in high_issues[:6]:
            st.markdown(
                f"""
                <div class="issue-row">
                    <div class="issue-icon">!</div>
                    <div style="flex:1">
                        <div class="issue-name">
                            {str(issue.get("category", "Other")).title()}
                        </div>
                        <div class="issue-detail">
                            {issue.get("description", "No description")}
                        </div>
                    </div>
                    <span class="severity-high">HIGH</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No high-priority issues.")


with c2:
    st.markdown('<div class="section-heading">Follow-up requested</div>', unsafe_allow_html=True)

    if followups:
        for call in followups[:6]:
            st.markdown(
                f"""
                <div class="issue-row">
                    <div class="issue-icon">↗</div>
                    <div style="flex:1">
                        <div class="issue-name">
                            {call.get("phone", "Unknown")}
                        </div>
                        <div class="issue-detail">
                            Community member requested NGO follow-up
                        </div>
                    </div>
                    <span class="severity-medium">PENDING</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No follow-ups requested.")


st.markdown("<br>", unsafe_allow_html=True)

with st.expander("Process a completed CALL-E call"):
    process_call_id = st.text_input(
        "CALL-E call ID",
        placeholder="call_...",
    )

    if st.button("Save completed call"):
        if not process_call_id:
            st.warning("Enter a CALL-E call ID.")
        else:
            try:
                saved_id = process_completed_call(
                    process_call_id,
                    supabase,
                )

                st.success(
                    f"Call saved to Supabase: {saved_id}"
                )
                st.cache_data.clear()
                st.rerun()

            except Exception as e:
                st.error(f"Could not save completed call: {e}")
