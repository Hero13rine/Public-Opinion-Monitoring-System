# Sensitive Content Evaluator

A Flask-based web application designed to evaluate sensitive content in text, classify its risk level, and provide real-time notifications for critical alerts. The application integrates a database for data storage and supports email notifications for flagged content.

---

## Features

- **Content Analysis**: Automatically evaluate text for sensitive words and classify their risk levels (e.g., Normal, Moderate, Major, Critical).
- **Email Notifications**: Sends real-time email alerts for sensitive content exceeding the defined risk threshold.
- **Database Integration**: Manages comments and analysis results with a MySQL database run database.sql.
- **Real-Time Controls**: Start and stop analysis dynamically through a user-friendly interface.
- **Configurable Risk Thresholds**: Easily adjust alert levels via the frontend.
- **Visualization**: Tabular views and dynamic charts for data visualization.
- **Automated Spiders**: Crawl and populate content from external sources (e.g., social media) for analysis.

---

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- MySQL server
- SMTP service for email notifications (e.g., Gmail, Outlook, etc.)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Hero13rine/Public-Opinion-Monitoring-System.git
   cd Public-Opinion-Monitoring-System

   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the application**
   - Update the configuration file located at `root/config/default.py` with:
     - Database connection details (`SQLALCHEMY_DATABASE_URI`)
     - SMTP server details for email notifications (`MAIL_SERVER`, `MAIL_PORT`, etc.)
     - Default risk threshold (`THRESHOLD`)
   
4. **Set the OpenAI API Key**
   - For Windows:
     ```bash
     setx API_KEY "your_api_key_here"
     ```
   - For Linux/Mac:
     ```bash
     export API_KEY="your_api_key_here"
     ```

5. **Initialize the database**
   - Create and migrate database tables:
     ```bash
     flask db init
     flask db migrate -m "Initial migration."
     flask db upgrade
     ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   - Open your browser and navigate to: `http://127.0.0.1:5000`

---

## Usage

### Frontend
- Submit text for analysis through the user interface.
- View results, including flagged content and risk levels.
- Adjust the risk threshold for notifications.
- Start and stop the automated analysis process dynamically.

### API Endpoints
#### **Analyze Text**
`POST /analyze`
- **Request Body**:
  ```json
  {
      "text": "Your content to analyze."
  }
  ```
- **Response**:
  ```json
  {
      "id": 1,
      "alert_level": "Major",
      "sensitive_words": [
          {"word": "example", "level": "Major"}
      ]
  }
  ```

#### **Start/Stop Automation**
`POST /automate`
- **Request Body**:
  ```json
  {"action": "start"}
  ```
  or
  ```json
  {"action": "stop"}
  ```

- **Response**:
  ```json
  {"message": "Analysis task started"}
  ```

---

## Directory Structure

```plaintext
.
├── app
│   ├── models.py          # Database models
│   ├── routes.py          # Application routes and logic
│   ├── services           # Email, evaluation, and spider logic
│   │   ├── email.py
│   │   ├── evaluation.py
│   │   ├── spider.py
│   └── templates          # HTML templates for the frontend
├── config
│   └── default.py         # Configuration file
├── migrations             # Database migration files
├── static                 # Static assets (CSS, JS)
├── tests                  # Unit tests
├── app.py                 # Main application entry point
├── requirements.txt       # Dependencies
└── README.md              # Project documentation
```

---

## Future Improvements

1. **Interface Optimization**
   - Improve the user interface with modern design frameworks.

2. **Remote Deployment**
   - Deploy the application on cloud platforms like AWS, Azure, or Heroku.

3. **Spiders Enhancement**
   - Expand crawling capabilities for more social media platforms.

4. **Real-Time Updates**
   - Implement WebSocket for instant updates to the frontend.

---

## Contribution

Contributions are welcome! Please fork the repository, make changes, and submit a pull request.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## Contact
For questions or support, please contact:
- Email: `zliu666@gmail.com`
