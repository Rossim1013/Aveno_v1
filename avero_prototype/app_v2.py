"""
AVERO prototype application version 2.

This version contains all of the premium MVP features discussed earlier:

* Multi‑tab dashboard with summary metrics, line charts and raw data table.
* Scheduling tab where users can add appointments and view upcoming ones.
* Task board to manage tasks with estimated/actual dates and completion status.
* AI assistant tab with a simple summary function and optional text‑to‑speech
  output via gTTS when available.

The AVERO logo is embedded as a base64‑encoded PNG (64×64 pixels) so no
external files are required. To update the logo, regenerate the base64
string and replace the ``LOGO_BASE64`` constant below.

This code is designed to run quickly on Streamlit and should be
responsive on tablets and desktop devices.
"""

from pathlib import Path
from datetime import datetime
import base64
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

try:
    from gtts import gTTS  # type: ignore
except ImportError:
    gTTS = None  # type: ignore


# Base64‑encoded 64×64 AVERO logo (PNG). This smaller version keeps the
# source code compact while still providing a clear icon for the header.
LOGO_BASE64: str = (
    "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAIAAAAlC+aJAAAQZ0lEQVR4nJVaeZhU1ZU/5963VFVv1XQ13TRoA4rsgg1BNkFRRP0G"
    "lMzOQnKMTUE9Ge7TB9x6m04KvRtt0fO/5qI+7e+jYCaE9f+mc/d9vDffoe/fCw7d3fv7rl33s89/fnryrc/uW/69G4888H7"
    "PP7zd9uz55771/d966N3f+c7PvzCD+93vuXv3zm235fH//6e+//fTDNz7/h+96Yz4/cWGf+eNw2/Gn90Zb3P/z72+8WXbr13c"
    "7++b9eoxrWcZ77n5y/xt/v23D79g/nYzfemXzy4o9332Xvvv5Y7/6v/++/u/eMPveP3FH797DO9PVmt7/SZKf2+9+b8vPn5Pnf"
    "n27vbPX1/Pd+y+b5qVVfmmyNnd7DWfcPTW56++8Nv5+9Z882cFcMzRo9pvU2vi7q9444XjcWN2z/w4C/MxfNvUvszAzj2sPAz"
    "ggSiJCIByw+/lF+YlK6nMKcQ95lShprDzTrX4TEU0yofUK+adXj1ZOsk6Yv3LObWyMlKlxXoHgkEs22LPCvw4gm9qH1AmW"
    "AbvtX8+9y5JSGztUJFkg1A7++rSflpXo8rkUVb3PpiXq3vdK1QBVmtW9ROaKG/J2mB7jw74mboL5xfd4AS0Z63f5Nsk3wU9"
    "EyZEGScxU8/Y/0QBWh+icxrg6ImJyAtVWjRGGZBKpvNEBFVt1T17+38P50tjA3VSIerZwrtBlYHsf0HMcPqmo36ABbDQgAB"
    "p7aTUfsRjzsKhrdnvsoh5cjQOXkspX1cx2ZlscRh6EQqupSxh81r6r45uGVipsF8F4qH0413U96XZApKZgZxmhA5HoimAAe"
    "srs/w9KAAIszVwtlfzLTVhB6Pd+C0AGslXM3SDh0w11p3EZn0sKcElFhnlpo+dEiY22NkpszmuQkiEAJ8jNzHIzgAZUrmfg"
    "qAK1FAvuyk4rhGI+gROLQTHq3M0iUfcRHxmM2g9BWMyDxmzQ/Z2xNsuRmROXiMs9KKGx2C4xieBvmCTsHIIN3SZfaW2alVMa"
    "pjgBjDcb8FYXz2icwWRELHMYFcEGgROAyhMxzYxYmxQFgM8gG9RU0ZIQJkKYkkeROGs8gyxHA5sVlh4UFT7vmPlK+TRsOLXa"
    "I8OQvDX9FQ/A8HqQSpEAKuEKRlq3zdSN6+y1kdnOldx7yCB81hE1rptcrsOdG4ORkZzjGbIVwoLl2s3q5tmjeUN2MM6vymwJ"
    "wkpXgnlCzjoANmsUKmYkYZ9VgMRoTIzqZzYMsXz8HofSGyPA+WAzSJ9jgxr6UDi7eHRKtN67OaOkA3akqduvD6czFkG5Mg5W"
    "NGL5c5q1dRUTJk47YPTxwzhWmMbmZTymVWwWFMKyOmGvALQKzQ0sRvgDMSTomIMAtKQIMRuGv9PYLbSMPZGdRMwIyMUMTQzU"
    "fI1LIoCqgiXp6jYOT0rIGfZNHqItYJkeT6QQRRFzc5JHIJiGCtJgMxoiiRJCaYQq5A1UCiIgkkk3kKEcCBIkyghIhgURJLPD"
    "AQBYB27xCOTZN8zPiBNDG3BsmSU4xj4n6rdwBS3EHEQtHMAI6jq1hp8AgjZ5K9KoFQB6PFWSzGd3mMwWiYCok9qk4k3qmwHR"
    "RVaA5dEaQ8BjbsC8lJZRiOtQYwe6MF6Ig5uY8JL2XeXR4lgUCI16ImSDDWwRkisLYcMk+nAhGKMAxLl+7ztR7E70dNJtUlMM"
    "iomdRR/nRoAcY/jxQMGIGmRRWxhiGCZNfLlYxIw8WGDrK4nGFxnfBGFpjOB4X4byZwxJMfPcvQF5I0iE8YeuYI9HLVmC4cMb"
    "EYioycyY8PiMFohziCCQjYLTgBWKJMkAnxyo/NiDhQEwWCSDK8Ayk5UDr1IERWVkqhFVig6XEhwC6QlOwttCKb4f4QX4mXaz"
    "MiUTJLqZYdS3IUkSdTwVm9GmM0ZGi2YNM8wbvGcYEsMjPnj3O5c8t4wxlY6KeHNyQbmYnhXkq9ME0EklEfljmcUlQ9PEhFZp"
    "csGq4R4bTuoZ1KzZOCn3OdXnMImkyxvCe+c8072NM44/s7xd1lc6fl/QPI6UoBEvLWUxq9lCwNxwIgn4r3PDsJzEO8zdo2u27"
    "peYj08LE+f5dfvOcM5dw7yU6+K8EU5VBGclMl4ojCHEOFM8ZAqYSKIKKAjBEqpMUM0osligigjSiKEEUpEIQIQIpZCCKEIhAk"
    "olBEFpYRZVHLbftZPXV6LfPTd/3k1y76ow4JFw1SmVrE8Qk5jMlEelotSjE/SiaYMzjA8XiUHkcgaimRF0ZXp+Um82VQ5NsaB"
    "iZwmlqalNomAYVSOmSYZ5W+jn0tj/DoMddKRTzZKsKoaq07p+YhbDzq77RmVJV6s+XbM8ZRlLmtVMqKMbChY2qMDNuwAcUl/4"
    "YBduvlf3/++abNkJl0E22LP3f/OO/p78dQLJy3dvX/v3753/DFcpn+zcV3NDx5cd5zth/30Y8+nv/8vz/vfrvn7zP3D/+UirT"
    "G9I9dw9OOveC++98zs99+VP9uVdPPvu57vmPXf3mt3kD1r++PU6+UoKTNI0qB3b9kIHjgzBw7vTkX5deUoZpq1hu+iEdURDQf"
    "69jCM45RgDAACCCK/hSklBKbQkVgAAAABJRU5ErkJggg=="
)


def load_data(dataset_name: str) -> pd.DataFrame:
    """Load a sample CSV from the data folder.

    Each file must contain ``date`` plus ``revenue``, ``bookings``, ``expenses``
    and ``clients`` columns. The ``date`` column will be parsed into datetime.
    """
    data_dir = Path(__file__).parent / "data"
    df = pd.read_csv(data_dir / f"{dataset_name}.csv", parse_dates=["date"])
    return df


@st.cache_data
def compute_summary(df: pd.DataFrame) -> dict:
    """Compute totals for the four key metrics in the data frame."""
    return {
        "Revenue": float(df["revenue"].sum()),
        "Bookings": int(df["bookings"].sum()),
        "Expenses": float(df["expenses"].sum()),
        "Clients": int(df["clients"].sum()),
    }


def ask_ai(question: str, df: pd.DataFrame) -> str:
    """Return a simple summary of the supplied dataset.

    Replace this with a call to a real LLM for more sophisticated answers.
    """
    if df.empty:
        return "No data available."
    start = df["date"].min().date()
    end = df["date"].max().date()
    total_rev = df["revenue"].sum()
    total_clients = df["clients"].sum()
    avg_bookings = df["bookings"].mean()
    return (
        f"Data ranges from {start} to {end}. "
        f"Total revenue: ${total_rev:,.0f}. "
        f"Total clients: {total_clients}. "
        f"Average bookings per period: {avg_bookings:.1f}."
    )


def main() -> None:
    """Run the Streamlit application."""
    st.set_page_config(page_title="AVERO v2", layout="wide")

    # Session state for appointments and tasks
    if "appointments" not in st.session_state:
        st.session_state.appointments: list[dict] = []
    if "tasks" not in st.session_state:
        st.session_state.tasks: list[dict] = []

    # Render logo
    try:
        logo_bytes = base64.b64decode(LOGO_BASE64)
        st.image(logo_bytes, width=140)
    except Exception:
        st.warning("Logo could not be displayed.")

    st.markdown(
        "# AVERO v2\n"
        "### Revolutionize Enterprise Analytics\n"
        "One Platform. Infinite Insights.",
        unsafe_allow_html=True,
    )

    # Sidebar dataset selector
    st.sidebar.header("Data")
    dataset = st.sidebar.selectbox(
        "Choose data set", ("therapist", "spa", "roofing"), index=0
    )
    data = load_data(dataset)
    summary = compute_summary(data)

    # Tabs
    dash_tab, sched_tab, tasks_tab, ai_tab = st.tabs(
        ["Dashboard", "Scheduling", "Task Board", "AI Assistant"]
    )

    # Dashboard tab
    with dash_tab:
        st.subheader("Key Metrics")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Revenue", f"${summary['Revenue']:,.0f}")
        c2.metric("Total Bookings", f"{summary['Bookings']:,}")
        c3.metric("Total Expenses", f"${summary['Expenses']:,.0f}")
        c4.metric("Total Clients", f"{summary['Clients']:,}")

        st.subheader("Revenue Over Time")
        st.line_chart(data.set_index("date")["revenue"])

        st.subheader("Bookings Over Time")
        st.line_chart(data.set_index("date")["bookings"])

        st.subheader("Expenses Over Time")
        st.line_chart(data.set_index("date")["expenses"])

        st.subheader("Raw Data")
        st.dataframe(data)

    # Scheduling tab
    with sched_tab:
        st.subheader("Add Appointment")
        with st.form("add_appointment", clear_on_submit=True):
            col1, col2 = st.columns(2)
            appt_date = col1.date_input("Date")
            appt_time = col2.time_input("Time")
            description = st.text_input("Description")
            assignee = st.text_input("Assignee (optional)")
            if st.form_submit_button("Add"):
                st.session_state.appointments.append(
                    {
                        "Date": appt_date,
                        "Time": appt_time.strftime("%H:%M"),
                        "Description": description,
                        "Assignee": assignee,
                    }
                )
                st.success("Appointment saved.")
        if st.session_state.appointments:
            st.subheader("Upcoming Appointments")
            st.dataframe(pd.DataFrame(st.session_state.appointments))
        else:
            st.info("No appointments scheduled.")

    # Task Board tab
    with tasks_tab:
        st.subheader("Add Task")
        with st.form("add_task", clear_on_submit=True):
            task_name = st.text_input("Task Name")
            assignee_t = st.text_input("Assignee (optional)")
            est_start = st.date_input("Estimated Start")
            est_finish = st.date_input("Estimated Finish")
            act_start = st.date_input("Actual Start", value=est_start)
            act_finish = st.date_input("Actual Finish", value=est_finish)
            if st.form_submit_button("Add Task"):
                st.session_state.tasks.append(
                    {
                        "Task": task_name,
                        "Assignee": assignee_t,
                        "Est Start": est_start,
                        "Est Finish": est_finish,
                        "Actual Start": act_start,
                        "Actual Finish": act_finish,
                        "Complete": False,
                    }
                )
                st.success("Task added.")
        if st.session_state.tasks:
            st.subheader("Task List")
            for idx, task in enumerate(st.session_state.tasks):
                cols = st.columns((3, 2, 2, 2, 2, 1))
                cols[0].text(task["Task"])
                cols[1].text(task["Assignee"])
                cols[2].text(task["Est Start"].strftime("%Y-%m-%d"))
                cols[3].text(task["Est Finish"].strftime("%Y-%m-%d"))
                cols[4].text(task["Actual Finish"].strftime("%Y-%m-%d"))
                done = cols[5].checkbox(
                    "Done", value=task["Complete"], key=f"task_{idx}"
                )
                st.session_state.tasks[idx]["Complete"] = done
        else:
            st.info("No tasks yet.")

    # AI Assistant tab
    with ai_tab:
        st.subheader("AI Assistant")
        st.write(
            "Ask a question about your data. The current implementation returns a simple summary."
        )
        question = st.text_input("Question")
        if question:
            response = ask_ai(question, data)
            st.markdown("**Response:**")
            st.write(response)
            if gTTS is not None:
                if st.button("Speak"):
                    try:
                        tts = gTTS(response)
                        buf = BytesIO()
                        tts.write_to_fp(buf)
                        buf.seek(0)
                        st.audio(buf.read(), format="audio/mp3")
                    except Exception as err:
                        st.error(f"Audio error: {err}")
            else:
                st.info("Install gTTS for audio playback.")
        st.markdown(
            "---\n"
            "*Voice input and more advanced AI responses will be supported in future versions.*"
        )


if __name__ == "__main__":
    main()
