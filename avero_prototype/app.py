"""
Streamlit prototype application for Avero.

This app demonstrates a simple analytics dashboard for small businesses.  Users can
select from one of several sample data sets, view key metrics and trends,
inspect the raw data and ask a question about the selected data set.  The
`ask_ai` function currently returns a basic summary; replace it with a call to
your preferred language model API for more sophisticated insights.
"""

from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np


def load_data(dataset_name: str) -> pd.DataFrame:
    """Load a sample data set from the data directory.

    Args:
        dataset_name: Name of the CSV file (without extension) to load.

    Returns:
        A pandas DataFrame with a parsed date column.
    """
    data_dir = Path(__file__).parent / "data"
    file_path = data_dir / f"{dataset_name}.csv"
    df = pd.read_csv(file_path, parse_dates=["date"])
    return df


@st.cache_data
def compute_summary(df: pd.DataFrame) -> dict:
    """Compute high‑level metrics for a data set.

    Returns a dictionary containing sums of revenue, bookings, expenses and
    clients.  Using `@st.cache_data` ensures that this computation is only
    performed once per unique DataFrame.

    Args:
        df: DataFrame containing at least the columns revenue, bookings,
            expenses and clients.

    Returns:
        Dict of aggregated metrics.
    """
    return {
        "Revenue": float(df["revenue"].sum()),
        "Bookings": int(df["bookings"].sum()),
        "Expenses": float(df["expenses"].sum()),
        "Clients": int(df["clients"].sum()),
    }


def ask_ai(question: str, df: pd.DataFrame) -> str:
    """Generate a simple natural language response based on the data.

    This placeholder implementation returns a static summary of the selected
    data set.  Replace this function with an API call to a real language
    model (e.g., OpenAI, Anthropic, Gemini) to produce dynamic answers.

    Args:
        question: The user’s question about the data (currently unused).
        df: The DataFrame representing the current data set.

    Returns:
        A string containing a generated answer.
    """
    start_date = df["date"].min().date()
    end_date = df["date"].max().date()
    total_revenue = df["revenue"].sum()
    total_clients = df["clients"].sum()
    average_booking = df["bookings"].mean()
    response = (
        f"The data covers {start_date} through {end_date}. "
        f"Total revenue was ${total_revenue:,.0f} with {total_clients:,} clients. "
        f"On average there were {average_booking:.1f} bookings per period."
    )
    return response


def main() -> None:
    """Run the Streamlit application."""
    st.set_page_config(page_title="Avero Prototype Dashboard", layout="wide")
    st.title("Avero Prototype Dashboard")

    # Sidebar: select data set
    st.sidebar.header("Settings")
    dataset = st.sidebar.selectbox(
        "Select a sample data set", ("therapist", "spa", "roofing"), index=0
    )

    # Load and summarise data
    df = load_data(dataset)
    summary = compute_summary(df)

    # Display key metrics
    st.subheader("Key Metrics")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue", f"${summary['Revenue']:,.0f}")
    c2.metric("Total Bookings", f"{summary['Bookings']:,}")
    c3.metric("Total Expenses", f"${summary['Expenses']:,.0f}")
    c4.metric("Total Clients", f"{summary['Clients']:,}")

    # Charts
    st.subheader("Revenue Over Time")
    revenue_chart_data = df.set_index("date")["revenue"]
    st.line_chart(revenue_chart_data)

    st.subheader("Bookings Over Time")
    bookings_chart_data = df.set_index("date")["bookings"]
    st.line_chart(bookings_chart_data)

    st.subheader("Expenses Over Time")
    expenses_chart_data = df.set_index("date")["expenses"]
    st.line_chart(expenses_chart_data)

    # Raw data table
    st.subheader("Data Table")
    st.dataframe(df)

    # AI assistant section
    st.subheader("Ask the AI about this data")
    user_question = st.text_input("Question")
    if user_question:
        answer = ask_ai(user_question, df)
        st.markdown("**AI Response:**")
        st.write(answer)


if __name__ == "__main__":
    main()
