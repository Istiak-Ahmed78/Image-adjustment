from flask import Flask, render_template, request, send_file
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/output"
STATIC_FRAME = "static/Frammed_image.png"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"

        file = request.files["file"]
        if file.filename == "":
            return "No selected file"

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        return render_template("index.html", uploaded_image=file.filename)

    return render_template("index.html", uploaded_image=None)

@app.route("/adjust", methods=["POST"])
def adjust():
    data = request.json
    image_path = os.path.join(UPLOAD_FOLDER, data["uploaded_image"])
    output_path = os.path.join(OUTPUT_FOLDER, "output.png")

    try:
        # Load frame and user images
        frame_image = Image.open(STATIC_FRAME).convert("RGBA")
        user_image = Image.open(image_path).convert("RGBA")

        # Resize user image to match the frame dimensions
        user_image = user_image.resize(frame_image.size, Image.Resampling.LANCZOS)

        # Get adjustment offsets
        offset_x = int(data.get("offsetX", 0))*2
        offset_y = int(data.get("offsetY", 0))*2
        if offset_x > 0:
            offset_x += 8
        elif offset_x < 0:
            offset_x -= 8

        if offset_y > 0:
            offset_y += 8
        elif offset_y < 0:
            offset_y -= 8
        # Create a blank canvas with transparency
        combined = Image.new("RGBA", frame_image.size, (255, 255, 255, 0))

        # Paste the user image at the adjusted position
        combined.paste(user_image, (offset_x, offset_y), user_image)

        # Overlay the frame on top
        combined.paste(frame_image, (0, 0), frame_image)

        # Placeholder: Trigger a popup on the front-end here
        # Example: Call a JavaScript function to show a "Saving..." message

        if os.path.exists(output_path):
            os.remove(output_path)
            print(f"{output_path} has been deleted.")
        else:
            print(f"{output_path} does not exist.")
        # Save the final combined image
        combined.save(output_path, "PNG")

        # Debugging info
        print(f"Offsets: X={offset_x}, Y={offset_y}")
        print(f"Output saved at: {output_path}")

        return {"success": True, "output_image": "/" + output_path}
    except Exception as e:
        print(f"Error during adjustment: {e}")
        return {"success": False, "error": str(e)}




@app.route("/download")
def download():
    output_path = os.path.join(OUTPUT_FOLDER, "output.png")
    print(output_path)
    if not os.path.exists(output_path):
        return "No adjusted image available for download."
    return send_file(output_path, as_attachment=True)
if __name__ == "__main__":
    app.run(debug=True)