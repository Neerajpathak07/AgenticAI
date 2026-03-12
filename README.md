# CityPulse AI: Location Intelligence & Chat Assistant

## Overview
AgenticAI is a web application that combines interactive map-based location scoring with a modern chat assistant. Users can click on a map to receive detailed scores for various location parameters (Safety, Connectivity, Rental Availability, etc.), powered by Google Maps data and custom Python logic. The chat sidebar provides instant, mirrored responses and can answer location-based queries using AI.

---

## Features
- **Interactive Map**: Click anywhere to get location scores and details.
- **Location Scoring**: Parameters like Safety, Connectivity, Rental Availability, Entertainment, Education, and more.
- **Google Maps Integration**: Uses Google Places API for real-time data.
- **Chat Assistant**: Sidebar chat with mirrored responses, avatars, timestamps, and zig-zag UI.
- **Dynamic UI**: Closable chat sidebar, floating button, and modern design.
- **Backend Intelligence**: Python/Flask backend with custom scoring logic and AI-powered chat.

---

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, Flask
- **APIs**: Google Maps JavaScript API, Google Places API
- **AI**: Gemini LLM (Google GenAI)
- **Environment**: dotenv for secrets, Flask-CORS for cross-origin requests

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Neerajpathak07/AgenticAI.git
cd AgenticAI
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root with the following keys:
```
SECRET_KEY=your_flask_secret_key
google_map_api=your_google_maps_js_api_key
google_place_api_key=your_google_places_api_key
FLASK_URL=http://localhost:5000
```

### 4. Run the Flask Server
```bash
python app.py
```

### 5. Open the App
Visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## File Structure
```
AgenticAI/
├── app.py                # Flask backend server
├── utils.py              # Location scoring and Google Maps logic
├── index.html            # Main frontend page
├── style.css             # Custom styles (may be in /static)
├── test.ipynb            # Jupyter notebook (optional)
├── __pycache__/          # Python cache
├── .env                  # Environment variables (not committed)
├── requirements.txt      # Python dependencies
```

---

## API Endpoints
- `/` : Main web app
- `/process-coordinates` : POST, receives lat/lng, returns location scores and top places
- `/chat` : POST, receives chat message, returns AI response
- `/health` : GET, health check

---

## Customization
- **Google API Keys**: Replace with your own keys in `.env`.
- **Scoring Logic**: Modify `utils.py` to adjust how scores are calculated.
- **Chat Logic**: Extend chat responses in `app.py` and integrate more AI features.

---

## Screenshots
![Location Scores Example](screenshots/location_scores.png)
![Chat Sidebar Example](screenshots/chat_sidebar.png)

---

## License
MIT License

---

## Author
- Neeraj Pathak ([GitHub](https://github.com/Neerajpathak07))

---

## Acknowledgements
- Google Maps & Places APIs
- Gemini LLM (Google GenAI)
- Flask & Flask-CORS

---

## Contributing
Pull requests and suggestions are welcome! Please open an issue for major changes.
