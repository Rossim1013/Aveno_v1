# Avero Prototype

This repository contains a simple prototype for **Avero**, an AI‑assisted analytics platform originally conceived during the “AI‑Driven $1M Strategy” planning sessions.  The goal of Avero is to give small‑ to mid‑sized businesses an easy way to view key performance indicators (KPIs) and drill down into their data without hiring a team of data scientists.

## Features

* **Multiple sample datasets** – The prototype ships with three example data sets (`therapist`, `spa`, and `roofing`) that demonstrate how different types of businesses might use the dashboard.
* **Dashboard view** – A responsive dashboard displays aggregate metrics (revenue, bookings, expenses and client count) and line charts for each metric.  It looks great on tablets and desktops and is perfect for field demos.
* **Dataset selector** – Users can choose which sample data set to explore via a sidebar dropdown.
* **Scheduling** – A dedicated Scheduling tab lets you enter appointments (date, time, description and assignee).  Appointments are listed in a table so you can see upcoming commitments.
* **Task board** – The Task Board tab allows you to create tasks with estimated and actual start/finish dates.  Tasks can be assigned to team members and marked complete via a checkbox.
* **Drill‑down details** – The dashboard includes a data table so users can verify where each KPI comes from.
* **AI insights placeholder** – An AI Assistant tab contains a text input box where users can ask questions about the data.  In this prototype the AI response is a generated summary of the selected data; you can easily replace it with an actual call to OpenAI or another LLM once an API key is provided.  Voice input and audio output are on the roadmap.

## Getting Started

1. Install the required Python packages.  From the root of the repository run:

   ```bash
   pip install -r requirements.txt
   ```

2. Launch the Streamlit application:

   ```bash
   streamlit run app.py
   ```

3. A browser window should open automatically.  Choose a sample data set from the sidebar and explore the dashboard.

## Project Structure

```
avero_prototype/
├── app.py             # Streamlit application
├── avero_logo.png      # Logo used in the header (referenced by app.py)
├── requirements.txt   # Python dependencies
├── data/
│   ├── roofing.csv    # Sample data for a roofing company
│   ├── spa.csv        # Sample data for a spa
│   └── therapist.csv  # Sample data for a therapist practice
└── README.md          # Project overview and instructions
```

## Notes & Next Steps

* **AI integration** – The `ask_ai` function in `app.py` currently returns a rudimentary summary of the selected data.  To connect a real large language model you can replace that function with an API call to OpenAI, Gemini, Claude, etc.  Make sure to store your API key in an environment variable and never commit it to version control.
* **Scaling to enterprise** – While this prototype uses Streamlit for simplicity, the architecture can be migrated to a more scalable stack (e.g., React + FastAPI on Kubernetes) when targeting large clients.  The data models and user flows defined in this project will still apply.
* **Additional features** – Alerts, goal tracking, role‑based access control and integrations with services like QuickBooks, Stripe, Jira and ServiceNow are out of scope for this simple prototype but are highlighted in the planning conversation.  They can be added iteratively as the product matures.

Feel free to fork and extend this prototype to suit your needs.  Pull requests and feedback are welcome!
