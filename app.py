import sys
import os
from flask import Flask, request
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/utils')
from utils.BottleCounter import count_bottles

app = Flask(__name__)

@app.route('/process-image', methods=['POST'])
def process_image():
    # Retrieve the image file from the request
    image_file = request.files['image']

    # Process the image using the count_bottles function
    bottle_count = count_bottles(image_file)

    # Return the bottle count as a response
    return {'count': bottle_count}
if __name__ == '__main__':
    app.run(debug=True)