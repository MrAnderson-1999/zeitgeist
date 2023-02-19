from flask import Flask, request, jsonify, render_template
import psycopg2

app = Flask(__name__)

# connect to the database
conn = psycopg2.connect(
    host='localhost',
    database='mydatabase',
    user='myusername',
    password='mypassword'
)

# create a cursor object
cur = conn.cursor()

# create a table for storing the user inputs
cur.execute('CREATE TABLE IF NOT EXISTS user_inputs (name TEXT, happiness INTEGER, sadness INTEGER, anger INTEGER, fear INTEGER, surprise INTEGER, neutral INTEGER)')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_image')
def generate_image():
    # get the current hour
    current_hour = int(datetime.datetime.now().strftime('%H'))

    # get the user inputs from the database
    cur.execute('SELECT * FROM user_inputs')
    rows = cur.fetchall()

    # calculate the moving average of the user inputs for the current hour
    total_happiness = 0
    total_sadness = 0
    total_anger = 0
    total_fear = 0
    total_surprise = 0
    total_neutral = 0
    count = 0
    for row in rows:
        if int(row[0]) == current_hour:
            total_happiness += row[1]
            total_sadness += row[2]
            total_anger += row[3]
            total_fear += row[4]
            total_surprise += row[5]
            total_neutral += row[6]
            count += 1
    if count == 0:
        moving_average = None
    else:
        moving_average = {
            'happiness': total_happiness / count,
            'sadness': total_sadness / count,
            'anger': total_anger / count,
            'fear': total_fear / count,
            'surprise': total_surprise / count,
            'neutral': total_neutral / count
        }

    # select the appropriate emoji based on the moving average
    if moving_average is None:
        emoji_filename = 'neutral.png'
    else:
        # calculate the distance between the moving average and each emoji
        distances = {}
        for i in range(10):
            emoji = f'emotion_{i+1}.png'
            emoji_path = f'static/images/{emoji}'
            emoji_image = Image.open(emoji_path)
            emoji_histogram = emoji_image.histogram()
            emoji_histogram = [float(h) for h in emoji_histogram]
            emoji_histogram = np.divide(emoji_histogram, np.sum(emoji_histogram))
            distance = np.linalg.norm(emoji_histogram - np.array(list(moving_average.values())))
            distances[emoji] = distance

        # select the emoji with the smallest distance
        emoji_filename = min(distances, key=distances.get)

    # return the result as a JSON object
    return jsonify({
        'url': f'static/images/{emoji_filename}',
        'x': '0',
        'y': '0',
        'width': '100',
        'height': '100'
    })

@app.route('/submit_survey', methods=['POST'])
def submit_survey():
    # get the user inputs from the form data
    name = request.form['name']
    happiness = int(request.form['happiness'])
    sadness = int(request.form['sadness'])
    anger = int(request.form['anger'])
    fear = int(request.form['fear'])
    surprise = int(request.form['surprise'])
    # store the user inputs in the database
    cur.execute('INSERT INTO user_inputs VALUES (%s, %s, %s, %s, %s, %s, %s)', (name, happiness, sadness, anger, fear, surprise, neutral))
    conn.commit()

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
