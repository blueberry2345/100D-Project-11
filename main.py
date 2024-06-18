import numpy as np
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for

# Create new app.
app = Flask(__name__)

# Establish the home page.
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

# Establish route to upload image.
@app.route('/upload', methods=['POST'])
def upload():
    # If there is POST request, carry out the colour palette operation. Else, redirect back to the home page.
    if request.method == 'POST':
        # Request the uploaded image and save it into the images folder.
        image_file = request.files["img_upload"]
        image_path = f"images/{image_file.filename}"
        image_file.save(image_path)

        # Open image and create a 2d array with contents containing rgb values for each pixel.
        image = Image.open(image_path)
        image_rgb = image.convert("RGB")
        rgb_array = np.array(image_rgb)
        pixel_array = rgb_array.reshape(-1,3)

        # Create ndarray listing the most common colours from most to least.
        unique_colour, no = np.unique(pixel_array, axis=0, return_counts=True)
        top_colours = unique_colour[np.argsort(no)[::-1]]

        # Converts the 10 most frequent rgb colours into string to be used for setting the colours of the squares.
        colours_style = []
        for i in range(10):
            colours_style.append(f"background-color: rgb({top_colours[i][0]}, {top_colours[i][1]}, {top_colours[i][2]}); padding-left:50px;")
        return render_template("colours.html", colours=colours_style, img_title=image_file.filename)

    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)