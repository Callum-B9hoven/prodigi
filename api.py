import urllib.request
from PIL import Image
import flask
from flask import request, jsonify

COLOUR_THRESHHOLD = 192

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#Dictionary of colours and their associated RGB Values
Colours = {'Red' : (255,0,0),
           'Green' : (0,255,0),
           'Blue' : (0,0,255),
           'Black' : (0,0,0),
           'Grey' : (128,128,128),
           'White' : (256, 256, 256),
           'Pink' : (255,0,255),
           'Yellow' : (255,255,0),
           'Turquoise' : (0,255,255),
           'Dark Red' : (128,0,0),
           'Dark Green' : (0,128,0),
           'Navy' : (0,0,128),
           'Purple' : (128,0,128),
           'Gross Bogey Colour' : (128,128,0),
           'Teal' : (0,128,128)
           }

#Used for the mode pixel method to work out how many of each pixel there is
ColoursBucket = {'Red' : 0,
           'Green' : 0,
           'Blue' : 0,
           'Black' : 0,
           'Grey' : 0,
           'White' : 0,
           'Pink' : 00,
           'Yellow' : 0,
           'Turquoise' : 0,
           'Dark Red' : 0,
           'Dark Green' : 0,
           'Navy' : 0,
           'Purple' : 0,
           'Gross Bogey Colour' : 0,
           'Teal' : 0
           }

def absoluteDifference(r, g, b):
    smallestDistance = 1000
    closestColour = ''
    for c in Colours:
        rgbDistance = abs(r - Colours[c][0]) + abs(g - Colours[c][1]) + abs(b - Colours[c][2])
        if rgbDistance < smallestDistance:
            smallestDistance = rgbDistance
            closestColour = c
    if smallestDistance > COLOUR_THRESHHOLD:
        closestColour = 'None'
    return closestColour

def modePixel(u):
    urllib.request.urlretrieve(u, 'images/myimage.jpg')
    im = Image.open('images/myimage.jpg', 'r')
    pix = im.load()
    width, height = im.size
    totalPixels = width * height
    pixel_values = list(im.getdata())
    biggestBucket = 0
    mostFrequentColour = ''
    for w in range(0, width, 1):
        for h in range(0, height, 1):
            pixel = pix[w,h]
            closest = absoluteDifference(pixel[0],pixel[1],pixel[2])
            if closest != 'None':
                ColoursBucket[closest] = ColoursBucket[closest]+1

    for c in ColoursBucket:
        print(c, ColoursBucket[c])
        if ColoursBucket[c] > biggestBucket:
            biggestBucket = ColoursBucket[c]
            mostFrequentColour = c
    return mostFrequentColour

def meanPixel(u):
    urllib.request.urlretrieve(u, 'images/myimage.jpg')
    im = Image.open('images/myimage.jpg', 'r')
    pix = im.load()
    width, height = im.size
    totalPixels = width * height
    pixel_values = list(im.getdata())
    redBucket = 0
    greenBucket = 0
    blueBucket = 0
    for w in range(0, width, 1):
        for h in range(0, height, 1):
            pixel = pix[w,h]
            redBucket = redBucket + pixel[0]
            blueBucket = blueBucket + pixel[1]
            greenBucket = greenBucket + pixel[2]
    redVal = redBucket / totalPixels
    blueVal = blueBucket / totalPixels
    greenVal = greenBucket / totalPixels
    closest = absoluteDifference(redVal, blueVal, greenVal)
    return closest

@app.route('/', methods=['GET'])
def home():
    return "<h1>Test API</h1><p>Use the GETs /api/colour/mean or /api/colour/mode, including a url as a parameter</p>"

# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

@app.route('/api/colour/mean', methods=['GET'])
def api_colourmean():
    if 'url' in request.args:
        url = request.args['url']
        colour = meanPixel(url)
    else:
        return "Error: no url provided. Please specify a URL."
    return jsonify(colour)

@app.route('/api/colour/mode', methods=['GET'])
def api_colourmode():
    if 'url' in request.args:
        url = request.args['url']
        colour = modePixel(url)
    else:
        return "Error: no url provided. Please specify a URL."
    return jsonify(colour)

app.run()
