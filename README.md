# Study Log Flask App

This project is a Flask web application designed to analyze and visualize study log data. It provides insights into study hours, focus levels, and trends over time.

## Project Structure

```
study-log-flask-app
├── app
│   ├── __init__.py          # Initializes the Flask application
│   ├── routes.py            # Defines the application routes
│   ├── analysis.py          # Contains analysis functions for study log data
│   └── templates            # HTML templates for rendering views
│       ├── index.html       # Homepage template
│       ├── summary.html     # Summary of study hours and focus statistics
│       └── heatmap.html     # Heatmap visualization of study hours
├── static
│   └── plots                # Directory for storing generated plots
├── study_log.csv            # CSV file containing study log data
├── requirements.txt         # Lists project dependencies
└── README.md                # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd study-log-flask-app
   ```

2. **Install dependencies:**
   It is recommended to use a virtual environment. You can create one using:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
   Then install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. **Run the application:**
   Start the Flask application with:
   ```
   flask run
   ```
   By default, the application will be accessible at `http://127.0.0.1:5000/`.

## Usage

- Navigate to the homepage to view an overview of the study log analysis.
- Access the summary page to see detailed statistics on study hours and focus levels.
- View the heatmap to analyze study time distribution across subjects and days.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.