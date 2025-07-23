import os  # Import the os module
from app import create_app

app = create_app()

if __name__ == "__main__":
    print("Starting the Flask application...")
    app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))