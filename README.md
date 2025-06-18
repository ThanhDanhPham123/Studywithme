# Studywithme
# Study With Me

A web application to help students manage their study life, featuring a to-do list, AI study buddy, and more.

## Features

- **User Registration:** Users can register with a username, graduation year, and purpose.
- **To-Do List:** Add, view, and complete tasks with deadlines.
- **AI Study Buddy:** Chat with an AI for study help and motivation (powered by Google Gemini).
- **Session-based Authentication:** Simple login/logout system.
- **CSV Export:** Export user and to-do data to CSV files.
- **Progress tracker** (In development)
- **Document organization** (In development)

## Project Structure

```
.
├── main_app.py
├── db.py
├── auth.py
├── Exporter.py
├── todo_item.csv
├── user.csv
├── instance/
│   └── test.db
├── route/
│   └── features/
│       ├── chat_with_bot.py
│       └── todo.py
├── static/
│   └── css/
│       └── style.css
└── templates/
    ├── base.html
    ├── chat.html
    ├── home.html
    └── todo.html
```

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/study-with-me.git
   cd study-with-me
   ```

2. **Create a virtual environment and activate it:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install flask flask_sqlalchemy google-generativeai
   ```

4. **Set up the database:**
   - The database will be created automatically on first run.

5. **Run the application:**
   ```sh
   python main_app.py
   ```
   - Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

6. **Export data to CSV:**
   - Run `Exporter.py` to export user and to-do data to CSV files.

## Configuration

- **Google Gemini API Key:**  
  Replace the placeholder API key in `route/features/chat_with_bot.py` with your own Google Gemini API key.

- **Secret Key:**  
  Change `app.config['SECRET_KEY']` in `main_app.py` to a secure value for production.

## File Descriptions

- [`main_app.py`](main_app.py): Main Flask app, user model, routes, and blueprint registration.
- [`db.py`](db.py): SQLAlchemy database initialization.
- [`auth.py`](auth.py): Login-required decorator for route protection.
- [`Exporter.py`](Exporter.py): Script to export database tables to CSV.
- [`route/features/todo.py`](route/features/todo.py): To-do list blueprint and model.
- [`route/features/chat_with_bot.py`](route/features/chat_with_bot.py): AI chat blueprint.
- [`static/css/style.css`](static/css/style.css): App styling.
- [`templates/`](templates/): HTML templates for the app.

## License

MIT License

---
