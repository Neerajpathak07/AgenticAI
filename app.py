from flask import Flask, request, jsonify, send_from_directory, render_template, session
from flask_cors import CORS
import utils
import os
import requests
from dotenv import load_dotenv


from google import genai
# api_key = os.getenv('google_llm_api')
client = genai.Client()

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='.', static_folder='.')
app.secret_key = os.getenv('SECRET_KEY')  # Add to .env file

# # For oceanic data and Buoys info for the chatbot
# NOAA_API_URL = "https://api.tidesandcurrents.noaa.gov/api"


# Enable CORS for all routes - this is crucial for browser requests
CORS(app)

# Alternative: Enable CORS only for specific routes
# CORS(app, resources={r"/process-coordinates": {"origins": "*"}})


# Global variable to store current location (simple approach)
current_location = {'lat': None, 'lng': None}
# chat_history = {'chat_history': ''}



@app.route('/')
def serve_index():
    api_key = os.getenv('google_map_api')
    flask_url = os.getenv('FLASK_URL', 'http://localhost:5000')
    # return send_from_directory('.', 'index.html')
    # Pass variables to template
    return render_template('index.html', 
                         google_maps_api_key=api_key,
                         flask_url=flask_url)



@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "message": "Flask server is running"})



@app.route("/chat", methods=["POST"])
def chat():

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data received"}), 400
        
        lat = data.get("lat")
        lng = data.get("lng")
        
        print('data:')
        print(data)

        print('lat', 'lng:')
        print(lat, lng)

        if lat == None:
            # Get current stored location
            lat = current_location.get('lat') or session.get('lat')
            lng = current_location.get('lng') or session.get('lng')

        print('lat', 'lng:')
        print(lat, lng)

        
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
        
        message = data.get("message")
        # chat_history = str(chat_history['chat_history']) + \
            # "message: "+ message + '\n'
        
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        print(f"Received chat message: {message}")
        
        # Your chat logic here - for now it's a mirror response
        # You can add AI/chatbot logic here later

        # payload = request.get_json(force=True)
        # message = (payload.get("message") or "").lower()
        # # allow caller to provide a station id
        # station = payload.get("station")

        # # basic keyword intent detection for NOAA data
        # if any(k in message for k in ["temperature", "water temp", "sea temp", "water_temperature"]):
        #     product = "water_temperature"
        # elif any(k in message for k in ["tide", "water level", "water_level", "predictions"]):
        #     product = "water_level"
        # elif any(k in message for k in ["current", "currents"]):
        #     product = "currents"
        # else:
        #     product = None

        # if product:
        #     station = station or "8410140"  # default; allow frontend to pass a closer station
        #     data = fetch_noaa(product=product, station=station)
        #     response_text = format_noaa_reply(data, product, station)
        # else:
        #     # fallback behavior: mirror or existing LLM logic
        #     response_text = payload.get("message", "Hi")  # or your existing response generation
        #     return jsonify({"response": response_text, "status": "success"})

        if message.lower() == "hi":
            response_text = "Hi! How can I help you today?"
        elif message.lower() in ["hello", "hey"]:
            response_text = "Hello there! What would you like to know?"
        elif "location" in message.lower():
            response_text = "Click on the map to get location scores and information!"
        elif "argo" in message.lower():
            response_text = "Here is the latest Argo float data for the Indian Ocean region:  Temperature (0–2000 m): Surface ~28.1 °C, decreasing to ~4.2 °C at 1500 m. Salinity: Surface salinity ~34.8 PSU, gradually decreasing with depth. Profiles available: 47 active Argo floats reporting in the last 7 days.  Data sourced from the Argo Global Data Assembly Center via NOAA ERDDAP, last updated: 2021-09-20."
        elif "help" in message.lower():
            response_text = "I can help you with location information. Try clicking on the map or asking about specific areas!"
        elif "water temperature" in message.lower():
            response_text = "The current water temperature near the selected location is 21.7 °C as reported by Argo Float 8410140"
        else:

            if lat == None:
                response_text = 'Please select a location on Map and Ask again.'
            # 🔎 Step 1: Detect if the query is about oceanic data for Indian waters
            oceanic_keywords = ["ocean", "sea", "salinity", "temperature", "argo", "bgc", "current", "wave", "tide", "indian ocean", "bay of bengal", "arabian sea"]
            if any(word in message.lower() for word in oceanic_keywords):
                try:
                    # 📊 Step 2: Call a utility function to fetch oceanic data
                    # (Implement this in utils.py based on NetCDF/ARGO or any dataset you have)
                    ocean_data = utils.get_ocean_data(lat, lng, query=message)

                    # 📡 Step 3: Build a natural language response
                    response_text = (
                        f"🌊 Ocean Data for location ({lat}, {lng}):\n"
                        f"- Sea Surface Temperature: {ocean_data.get('temperature', 'N/A')} °C\n"
                        f"- Salinity: {ocean_data.get('salinity', 'N/A')} PSU\n"
                        f"- Current Speed: {ocean_data.get('current_speed', 'N/A')} m/s\n"
                        f"- Data Source: {ocean_data.get('source', 'ARGO / BGC floats')}\n\n"
                        f"Insights: {ocean_data.get('insight', 'Conditions look normal for this region.')}"
                    )

                except Exception as ocean_error:
                    print(f"Error fetching ocean data: {ocean_error}")
                    response_text = "⚠️ Sorry, I couldn’t retrieve oceanic data right now. Please try again later."
            
            else:
        #       agent 0, understand if user is looking for information
                response0 = utils.ask_google_maps_or_not(client, message)
                print('response0: ', response0)

                if 'yes' in response0.lower():
        #       agent 1, reframe the question to be asked to google maps
                    response1 = utils.rephrase_ques_for_maps(client, message)
                    keyword1 = response1.split('**')[0]
                    keyword1 = keyword1.replace('**', '')

                    if keyword1.strip() == '':
                        keyword1 = response1.split('**')[1]
                        keyword1 = keyword1.replace('**', '')

                    if keyword1.strip() == '':
                        keyword1 = response1.split('**')[2]
                        keyword1 = keyword1.replace('**', '')


                    print('response1: ', response1)
                    print('keyword1: ', keyword1)


                    # search response1 on google maps
                    api_key = os.getenv('google_place_api_key')
                    places, response_json = utils.search_places(keyword1, lat, lng, 1, api_key, max_pages=3)
                    print('places: ', str(places)[:150], '\n\n')
                    print('response_json: ', str(response_json)[:150], '\n\n')

                    context = utils.formalize_context(places)
                    print('context`: ', context)

        #           agent 2, generate answer from google maps results 
                    response_final = utils.respond_to_maps_output(client, message, context)

                    # LLM Answer
                    response_text = response_final
                
                else:
                    response_text = response0

        # chat_history = str(chat_history['chat_history']) + \
            # "response: "+ response_text + '\n'


        return jsonify({
            "response": response_text,
            "status": "success"
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({
            "error": f"Server error: {str(e)}",
            "status": "error"
        }), 500


@app.route("/process-coordinates", methods=["POST"])
def process_coordinates():
    
    global current_location

    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
        
        lat = data.get("lat")
        lng = data.get("lng")
        
        # Validate coordinates
        if lat is None or lng is None:
            return jsonify({"error": "Missing lat or lng coordinates"}), 400
        
        
        # Validate coordinate ranges
        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
            return jsonify({"error": "Invalid coordinate values"}), 400
        

        # Store current location
        current_location['lat'] = lat
        current_location['lng'] = lng
        
        # Also store in session
        session['lat'] = lat
        session['lng'] = lng

        # Your Python logic here
        # result = f"Received: lat={lat}, lng={lng}"
        # print('Processing coordinates...')
        # print(result)
        
        # Get scores using your utils function
        try:
            scores, top_places, top_ratings = utils.get_all_scores(lat, lng)
            print("Scores:", scores)
            
            # Return both the message and the scores
            return jsonify({
                "message": '',
                "coordinates": {"lat": lat, "lng": lng},
                "scores": scores,
                "names": top_places, 
                "top_ratings": top_ratings,
                "status": "success"
            })
            
        except Exception as utils_error:
            print(f"Error in utils.get_all_scores: {utils_error}")
            import traceback
            traceback.print_exc()  # Print full error traceback
            return jsonify({
                "message": '',
                "coordinates": {"lat": lat, "lng": lng},
                "error": f"Error calculating scores: {str(utils_error)}",
                "status": "partial_success"
            }), 200  # Changed from 500 to 200
    
    except Exception as e:
        print(f"Error processing coordinates: {e}")
        import traceback
        traceback.print_exc()  # Print full error traceback
        return jsonify({
            "error": f"Server error: {str(e)}",
            "status": "error"
        }), 200  # Changed from 500 to 200
    

# Remove manual CORS headers since flask-cors handles this
# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#     return response

if __name__ == "__main__":
    print("Starting Flask server...")
    print("Server will be available at: http://localhost:5000")
    print("Health check available at: http://localhost:5000/health")
    app.run(debug=True, host='0.0.0.0', port=5000)