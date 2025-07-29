"""
Streamlit prototype application for AVERO.

This application demonstrates a premium MVP for the AVERO analytics platform.
It includes a multi‑tab interface with a key metrics dashboard, scheduling and
task management tools, and an AI assistant placeholder. The design is kept
responsive so it works well on tablets and desktops, and the code is written
for clarity and extensibility. For production use, integrate the AI assistant
with a real language model API and back the appointment/task state with a
database.
"""

from pathlib import Path
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np


def load_data(dataset_name: str) -> pd.DataFrame:
    """Load a sample data set from the local data directory.

    Each CSV must contain a ``date`` column along with the numeric fields
    ``revenue``, ``bookings``, ``expenses`` and ``clients``.

    Args:
        dataset_name: File name (without the ``.csv`` extension).

    Returns:
        A pandas DataFrame with the ``date`` column parsed as datetime.
    """
    data_dir = Path(__file__).parent / "data"
    file_path = data_dir / f"{dataset_name}.csv"
    df = pd.read_csv(file_path, parse_dates=["date"])
    return df


@st.cache_data
def compute_summary(df: pd.DataFrame) -> dict:
    """Compute aggregate metrics for a data set.

    The sums are cast to native Python types so Streamlit can display them
    cleanly. This function is cached to avoid recomputation on each rerun.

    Args:
        df: A DataFrame with columns ``revenue``, ``bookings``, ``expenses`` and ``clients``.

    Returns:
        A dictionary containing the total revenue, bookings, expenses and clients.
    """
    return {
        "Revenue": float(df["revenue"].sum()),
        "Bookings": int(df["bookings"].sum()),
        "Expenses": float(df["expenses"].sum()),
        "Clients": int(df["clients"].sum()),
    }


def ask_ai(question: str, df: pd.DataFrame) -> str:
    """Return a simple summary answer based on the provided data.

    This stub illustrates how natural‑language queries might work. Replace this
    implementation with a call to an AI provider (e.g. OpenAI, Claude) to
    generate richer insights or forecasts. For now it summarises the date
    range, total revenue and average bookings.

    Args:
        question: A question posed by the user (currently unused).
        df: The DataFrame to summarise.

    Returns:
        A human‑readable answer string.
    """
    if df.empty:
        return "No data available to analyse."
    start_date = df["date"].min().date()
    end_date = df["date"].max().date()
    total_revenue = df["revenue"].sum()
    total_clients = df["clients"].sum()
    average_booking = df["bookings"].mean()
    return (
        f"Your data spans {start_date} through {end_date}. "
        f"Total revenue was ${total_revenue:,.0f} across {total_clients:,} clients. "
        f"On average there were {average_booking:.1f} bookings per period."
    )


def main() -> None:
    """Execute the Streamlit application."""
    st.set_page_config(page_title="AVERO Analytics Prototype", layout="wide")

    # Initialise session state containers for appointments and tasks
    if "appointments" not in st.session_state:
        st.session_state.appointments: list[dict] = []
    if "tasks" not in st.session_state:
        st.session_state.tasks: list[dict] = []

    # Header with logo and tagline. The logo must exist alongside this script
    # with the filename ``avero_logo.png`` (added to the repository). It will
    # appear at the top of the page. If the file is missing, a warning is
    # displayed instead of an error.
    logo_path = Path(__file__).parent / "avero_logo.png"
    if logo_path.exists():
        st.image(str(logo_path), width=160)
    else:
        st.warning(
            "Logo file not found: please ensure avero_logo.png is present in the repository."
        )
    st.markdown(
        "# AVERO\n"
        "### Revolutionize Enterprise Analytics\n"
        "One Platform. Infinite Insights.",
        unsafe_allow_html=True,
    )

    # Sidebar for dataset selection. Users can pick one of the bundled sample
    # data sets to explore. These correspond to the CSV files in the ``data`` folder.
    st.sidebar.header("Settings")
    dataset_choice = st.sidebar.selectbox(
        "Select a sample data set", ("therapist", "spa", "roofing"), index=0
    )

    # Load the selected data and compute high‑level statistics
    data = load_data(dataset_choice)
    summary = compute_summary(data)

    # Create tabbed layout: Dashboard, Scheduling, Task Board and AI Assistant
    dashboard_tab, scheduling_tab, tasks_tab, ai_tab = st.tabs(
        ["Dashboard", "Scheduling", "Task Board", "AI Assistant"]
    )

    # ---------------------- Dashboard Tab ----------------------
    with dashboard_tab:
        st.subheader("Key Metrics")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Revenue", f"${summary['Revenue']:,.0f}")
        c2.metric("Total Bookings", f"{summary['Bookings']:,}")
        c3.metric("Total Expenses", f"${summary['Expenses']:,.0f}")
        c4.metric("Total Clients", f"{summary['Clients']:,}")

        # Line charts for revenue, bookings and expenses over time
        st.subheader("Revenue Over Time")
        st.line_chart(data.set_index("date")["revenue"])

        st.subheader("Bookings Over Time")
        st.line_chart(data.set_index("date")["bookings"])

        st.subheader("Expenses Over Time")
        st.line_chart(data.set_index("date")["expenses"])

        # Raw data display for transparency
        st.subheader("Data Table")
        st.dataframe(data)

    # ---------------------- Scheduling Tab ----------------------
    with scheduling_tab:
        st.subheader("Scheduling")
        with st.form("appointment_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            appt_date = col1.date_input("Appointment Date")
            appt_time = col2.time_input("Appointment Time")
            description = st.text_input("Description")
            assignee = st.text_input("Assignee (optional)")
            submitted = st.form_submit_button("Add Appointment")
            if submitted:
                st.session_state.appointments.append(
                    {
                        "Date": appt_date,
                        "Time": appt_time.strftime("%H:%M"),
                        "Description": description,
                        "Assignee": assignee,
                    }
                )
                st.success("Appointment added!")
        if st.session_state.appointments:
            st.subheader("Upcoming Appointments")
            appt_df = pd.DataFrame(st.session_state.appointments)
            st.dataframe(appt_df)
        else:
            st.info("No appointments scheduled yet.")

    # ---------------------- Task Board Tab ----------------------
    with tasks_tab:
        st.subheader("Task Board")
        with st.form("task_form", clear_on_submit=True):
            name = st.text_input("Task Name")
            assignee_task = st.text_input("Assigned To (optional)")
            est_start = st.date_input("Estimated Start Date")
            est_finish = st.date_input("Estimated Finish Date")
            actual_start = st.date_input("Actual Start Date", value=est_start)
            actual_finish = st.date_input("Actual Finish Date", value=est_finish)
            task_submitted = st.form_submit_button("Add Task")
            if task_submitted:
                st.session_state.tasks.append(
                    {
                        "Task": name,
                        "Assignee": assignee_task,
                        "Est Start": est_start,
                        "Est Finish": est_finish,
                        "Actual Start": actual_start,
                        "Actual Finish": actual_finish,
                        "Complete": False,
                    }
                )
                st.success("Task added!")
        if st.session_state.tasks:
            st.subheader("Current Tasks")
            for idx, task in enumerate(st.session_state.tasks):
                cols = st.columns((3, 2, 2, 2, 2, 1))
                cols[0].text(task["Task"])
                cols[1].text(task["Assignee"])
                cols[2].text(task["Est Start"].strftime("%Y-%m-%d"))
                cols[3].text(task["Est Finish"].strftime("%Y-%m-%d"))
                cols[4].text(task["Actual Finish"].strftime("%Y-%m-%d"))
                # Completion checkbox updates the task in place
                done = cols[5].checkbox(
                    "Done",
                    value=task["Complete"],
                    key=f"task_done_{idx}",
                )
                st.session_state.tasks[idx]["Complete"] = done
        else:
            st.info("No tasks added yet.")

    # ---------------------- AI Assistant Tab ----------------------
    with ai_tab:
        st.subheader("AI Assistant")
        st.write(
            "Ask questions about your data or enter natural‑language requests. "
            "This assistant currently returns a simple summary of your data. "
            "Integrate it with your favourite LLM for dynamic answers."
        )
        user_question = st.text_input("Enter your question")
        if user_question:
            answer = ask_ai(user_question, data)
            st.markdown("**AI Response:**")
            st.write(answer)
        st.markdown(
            "---\\n"
            "*Voice input and audio responses will be supported in a future version.*"
        )


if __name__ == "__main__":
    main()
