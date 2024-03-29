from flask import Flask, render_template, request, jsonify
import test_questions
import text_and_speech
import subprocess
import webbrowser
import json
import time
import random
import datetime
import base64
import os

app = Flask(__name__)

data = {}
three_things = ()
image_data1 = ()
image_data2 = ()
words = ()
chosen_word = ""
clock = {}
drawing_data = ""

def save_data_to_file():
    folder_name = str(datetime.datetime.now())
    # create freports folder if it doesn't exist
    if not os.path.exists('reports'):
        os.mkdir('reports')
    
    os.mkdir('reports/' + folder_name)

    # step2: save the data in that folder
    results = {}
    results[str(datetime.datetime.now())] = data
    try:
        results = test_questions.process_mmse_report(results)
        results_html = test_questions.generate_html(results)
    except Exception as e:
        print(f"Error: {e}")


    with open('reports/' + folder_name + '/results.json', 'w') as f:
        json.dump(results, f, indent=4)
    with open('reports/' + folder_name + '/results.html', 'w') as f:
        f.write(results_html)
    with open('reports/' + folder_name + '/drawing.png', 'wb') as f:
        f.write(drawing_data)

    return folder_name



def read_config_file():
    config_path = 'config.json'
    if not os.path.exists(config_path):
        default_config = {
            "enable_group1": True,
            "enable_group2": True,
            "enable_group3": True,
            "enable_group4": True,
            "enable_group5": True,
            "enable_group6": True,
            "enable_group7": True,
            "enable_group8": True,
            "enable_group9": True,
            "enable_group10": True,
            "enable_save_data": True
        }
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=4)
        return default_config
    else:
        with open(config_path, 'r') as f:
            return json.load(f)

def speak(text, default_model = "gTTS"):
    if default_model == "espeak":
        subprocess.call(["espeak", text])
    elif default_model == "gTTS":
        text_and_speech.convert_text_to_speech(text)

@app.route('/')
def index():
    data.clear()
    return render_template('index.html')

@app.route('/open_report', methods=['POST'])
def open_report():
    # Get folder name from the request
    folder_name = request.get_json()['folderName']
    file_path = os.path.join(os.getcwd(), 'reports', folder_name, 'results.html')
    # Use webbrowser to open the file
    webbrowser.open(file_path)

@app.route('/start', methods=['POST', 'GET'])
def start():
    global three_things, image_data1, image_data2, data, words, chosen_word, clock
    data = {}
    three_things = ()
    image_data1 = ()
    image_data2 = ()
    words = ()
    chosen_word = ""
    clock = {}

    if config['enable_group1']:
        instruction = "I will ask you some questions, and give you some problems to solve. Please answer them to the best of your ability."
        speak(instruction)
        time.sleep(1)

        questions = [
            "What is the current year?",
            "What is the current month?",
            "What is the date today?",
            "What is the current day of the week?",
            "what is the current season?",
            # "What country are we in?",
            # "What county are we in?",
            # "What city are we in?",
            # "What is the name or address of this building?",
            # "What floor of the building are we on?",
        ]

        right_answers = test_questions.get_date_info()

        for q in range(len(questions)):
            speak(questions[q])
            spoken_text = text_and_speech.convert_speech_to_text()
            if list(right_answers.keys())[q] == "Year":
                # extract text, remove all non-numeric characters
                spoken_text = "".join([c for c in spoken_text if c.isdigit()])
            data[list(right_answers.keys())[q]] = { "question" : questions[q], "spoken_text": spoken_text, "correct": list(right_answers.values())[q]}

    return jsonify({"data": data})

@app.route('/group2', methods=['POST', 'GET'])
def group2():
    global three_things
    if config['enable_group2']:
        instruction = 'I am going to name 3 objects. After I have said them I want you to repeat them back to me'
        speak(instruction)
        time.sleep(2)

        three_things = test_questions.get_three_things()
        speak(three_things[0] + '. ' + three_things[1] + '. And ' + three_things[2])

        spoken_text = text_and_speech.convert_speech_to_text()
        data['three_things'] = {
            'spoken_text': spoken_text,
            'correct': " ".join(three_things)
        }
        time.sleep(1)
        speak("Repeat them few more times and try to remember, I will ask you to repeat them in few minutes.")
        time.sleep(10)

    return jsonify(data)

@app.route('/group3', methods=['POST', 'GET'])
def group3():
    if config['enable_group3']:
        instruction = "Now I am going to give you a word, and I want you to say it backwards."
        speak(instruction)
        time.sleep(1)
        word = test_questions.get_reverse_word()
        speak("The word is: " + word)

        spoken_text = text_and_speech.convert_speech_to_text()
        spoken_text = "".join([c for c in spoken_text if c.isalpha()])
        data['reverse_word'] = {
            'spoken_text': spoken_text.replace(" ", ""),
            'correct': word[::-1]
        }

    return jsonify(data)

@app.route('/group4', methods=['POST', 'GET'])
def group4():
    if config['enable_group4']:
        instruction = "Can you repeat the three things I asked you to remember earlier?"
        speak(instruction)

        spoken_text = text_and_speech.convert_speech_to_text()
        data['three_things_repeat'] = {
            'spoken_text': spoken_text,
            'correct': " ".join(three_things)
        }

    return jsonify(data)

@app.route('/group5_1', methods=['POST', 'GET'])
def group5_1():
    if config['enable_group5']:
        global image_data1
        image_data1= test_questions.get_image_link()
        return jsonify(image_data1)
    else:
        return jsonify({"status": "group5 is disabled"})

@app.route('/group5_2', methods=['POST', 'GET'])
def group5_2():
    if config['enable_group5']:
        instructions = "Now name this object"
        speak(instructions)
        time.sleep(1)

        spoken_text = text_and_speech.convert_speech_to_text()
        data['image1'] = {
            'spoken_text': spoken_text,
            'correct': image_data1[0]
        }

    return jsonify(data)

# lets repeat the same thing for the second image, group5_1_repeat and group5_2_repeat
@app.route('/group5_1_repeat', methods=['POST', 'GET'])
def group5_1_repeat():
    global image_data2
    while True:
        image_data2 = test_questions.get_image_link()
        if image_data2[0] != image_data1[0]:
            break

    return jsonify(image_data2)

@app.route('/group5_2_repeat', methods=['POST', 'GET'])
def group5_2_repeat():
    if config['enable_group5']:
        instructions = "Now name this object"
        speak(instructions)
        time.sleep(1)

        spoken_text = text_and_speech.convert_speech_to_text()
        data['image2'] = {
            'spoken_text': spoken_text,
            'correct': image_data2[0]
        }

    return jsonify(data)

@app.route('/group6', methods=['POST', 'GET'])
def group6():
    if config['enable_group6']:
        instructions = "I would like you to repeat the following phrase after me: No ifs, ands, or buts."
        speak(instructions)

        spoken_text = text_and_speech.convert_speech_to_text()
        data['phrase'] = {
            'spoken_text': spoken_text,
            'correct': "No ifs, ands, or buts"
        }

    return jsonify(data)


@app.route('/group7_1', methods=['POST', 'GET'])
def group7_1():
    global words, chosen_word
    if config['enable_group7']:
        instructions = "Read the instructions on the screen and do what it says."
        speak(instructions)

        words = test_questions.get_words_to_click()
        chosen_word = random.choice(words)
        return jsonify(words, chosen_word)
    else:
        return jsonify({"status": "group7 is disabled"})

@app.route('/group7_2', methods=['POST', 'GET'])
def group7_2():
    if request.method == 'POST':
        r = request.get_json()
        result = r['target']

        data['words'] = {
            'chosen_word': result,
            'correct': chosen_word
        }

    return jsonify(data)

@app.route('/group8_1', methods=['POST', 'GET'])
def group8_1():
    global clock
    if config['enable_group8']:
        instructions = "I am going to give you a time, please use the sliders on screen to set the time to the given time."
        speak(instructions)
        time.sleep(0.5)

        clock = test_questions.get_random_time()
        speak(f"The time is {clock['hour']} {clock['minute']}")

        return jsonify(clock)
    else:
        return jsonify({"status": "group8 is disabled"})

@app.route('/group8_2', methods=['POST', 'GET'])
def group8_2():
    if request.method == 'POST':
        r = request.get_json()
        r['hour'] = 12 if int(r['hour'])//30 == 0 else int(r['hour'])//30
        r['minute'] = int(r['minute'])//6

        data['clock'] = {
            'time': r,
            'correct': clock
        }

    return jsonify(data)

@app.route('/group9', methods=['POST', 'GET'])
def group9():
    if config['enable_group9']:
        instructions = "Please make up and speak a sentence about anything you like."
        speak(instructions)

        spoken_text = text_and_speech.convert_speech_to_text()
        data['sentence'] = {
            'spoken_text': spoken_text,
        }

    return jsonify(data)


@app.route('/group10_1', methods=['POST', 'GET'])
def group10_1():
    if config['enable_group10']:
        instructions = "Please draw a picture shown on the left side of the screen on to the right side of the screen."
        speak(instructions)
        return jsonify({"status": "group10 is enabled"})
    else:
        return jsonify({"status": "group10 is disabled"})


@app.route('/group10', methods=['POST', 'GET'])
def group10():
    if config['enable_group10']:
        if request.method == 'POST':
            global drawing_data
            r = request.get_json()
            data_url = r['dataURL']
            header, encoded = data_url.split(",", 1)
            drawing_data = base64.b64decode(encoded)

            score, description = test_questions.get_drawing_score(encoded)
            data['drawing'] = {
                'score': score,
                'description': description
            }
            
            if config['enable_save_data']:
                folder_name = save_data_to_file()
                data['folder_name'] = folder_name
            return jsonify(data)
        else:
            return jsonify({"status": "GET request not supported"})
    else:
        if config['enable_save_data']:
            folder_name = save_data_to_file()
            data['folder_name'] = folder_name
        return jsonify({"status": "group10 is disabled"})


if __name__ == "__main__":
    config = read_config_file()
    app.run(debug=True)