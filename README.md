# Google Cloud DevConf 2026 Website

This is a Flask-based informational website for a 1-day technical conference.

## Features
- **Schedule View**: Full timeline of 8 talks + lunch break.
- **Search**: Filter talks by title, speaker, or category.
- **Responsive Design**: Premium dark-mode UI that works on all devices.
- **Data**: In-memory dummy data structure for easy modification.

## Tech Stack
- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, Google Fonts

## Setup & Running

1. **Prerequisites**: Ensure you have Python installed.

2. **Installation**:
   ```bash
   pip install flask
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Access the Site**:
   Open your browser and navigate to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Customization
- **Modify Data**: Edit `SPEAKERS` and `TALKS` lists in `app.py`.
- **Change Styles**: Edit `static/css/style.css`.
