import os
import requests
import base64
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="../templates")

# API Backend URL (default to localhost if not set, but in docker we will set it)
# When running in docker network, use container name, or public IP if accessed from browser
# But here server-side rendering needs access to backend.
API_URL = os.getenv("API_URL", "http://localhost:8000")

@app.route("/", methods=["GET", "POST"])
def index():
    image_data_url = None
    filename = None
    detections = []
    count = 0

    if request.method == "POST":
        if "file" not in request.files:
            return render_template("index.html", error="No file part")
        
        file = request.files["file"]
        if file.filename == "":
            return render_template("index.html", error="No selected file")

        if file:
            filename = file.filename
            # Read file content
            file_content = file.read()
            # Convert to base64 for display
            encoded_image = base64.b64encode(file_content).decode('utf-8')
            image_data_url = f"data:image/jpeg;base64,{encoded_image}"

            # Call Backend API
            try:
                # Reset file pointer to beginning
                file.seek(0)
                files = {"file": (filename, file, file.content_type)}
                response = requests.post(f"{API_URL}/predict", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    detections = result.get("detections", [])
                    count = result.get("count", 0)
                else:
                    print(f"Error from API: {response.text}")
            except Exception as e:
                print(f"Exception calling API: {e}")

    return render_template(
        "index.html",
        api_base=API_URL,
        image_data_url=image_data_url,
        filename=filename,
        detections=detections,
        count=count
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
