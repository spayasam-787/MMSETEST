import datetime
import random
import json
import requests
from openai import OpenAI
import base64
import requests
from KEYS import OPENAI_API_KEY

def get_three_things():
    three_things = (
    ("car", "tree", "ball"),
    ("pencil", "moon", "shoe"),
    ("apple", "mountain", "watch"),
    ("flower", "book", "fridge"),
    ("guitar", "cloud", "spoon"),
    ("bird", "bottle", "chair"),
    ("lamp", "ocean", "hat"),
    ("computer", "banana", "door"),
    ("glass", "cat", "bridge"),
    ("phone", "sweater", "lake"),
    ("plate", "sky", "beach"),
    ("sandwich", "star", "key"),
    ("dog", "paper", "train"),
    ("pizza", "planet", "ring"),
    ("butterfly", "boot", "tower"),
    ("camera", "lemon", "bed"),
    ("song", "candle", "river"),
    ("grape", "pocket", "museum"),
    ("whistle", "island", "desk"),
    ("chocolate", "kite", "park")
)
    return random.choice(three_things)

def get_reverse_word():
    reverse_words = ("APPLE","BIRD","DOG","FLOWER","GLASS","LAMP","SONG","GLASS","CAR")
    return random.choice(reverse_words)

def get_season(month, day):
    if (month == 12 and day >= 21) or (1 <= month <= 2) or (month == 3 and day < 20):
        return "Winter"
    elif (month == 3 and day >= 20) or (4 <= month <= 5) or (month == 6 and day < 21):
        return "Spring"
    elif (month == 6 and day >= 21) or (7 <= month <= 8) or (month == 9 and day < 22):
        return "Summer"
    else:
        return "Fall"
    
def get_date_info():
    current_date = datetime.datetime.now()
    year = current_date.year
    month_num = current_date.month
    month = current_date.strftime("%B") 
    day = current_date.day
    day_of_week = current_date.strftime("%A")

    return {
        "Year": year,
        "Month": month,
        "Day": day,
        "DayOfWeek": day_of_week,
        "Season": get_season(month_num, day)
    }

def get_date_info_with_season():
    date_info = get_date_info()
    return date_info

def get_image_link():
    image_links = {"wrist watch" : "https://i.pinimg.com/736x/11/13/0a/11130ac9de99eae78af686a9742a15e3.jpg",
                "airplane": 'https://thumbs.dreamstime.com/b/airplane-18327587.jpg',
                "car": 'https://vehicle-images.dealerinspire.com/stock-images/chrome/d51929e056d69529c5bf44c4ceaddf7e.png',
                }
    return random.choice(list(image_links.items()))
    
def get_words_to_click():
    words = ['hello', 'good', 'new', 'happy', 'beautiful']
    # return two random words
    return random.sample(words, 2)

def get_random_time():
    hour = random.randint(1, 12)
    minute = random.choice(range(0, 55, 5))
    if minute == 0:
        minute = "00"
    elif minute == 5:
        minute = "05"
    else:
        minute = minute
    return { "hour": hour, "minute": minute}

def get_location_info():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()

        country = data.get("country", "Unknown")
        state = data.get("region", "Unknown")

        return {
            "Country": country,
            "State": state
        }
    except Exception as e:
        return {
            "Country": "Unknown",
            "State": "Unknown",
        }

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def get_drawing_score(encoded):
    main_image = encode_image("static/image.png")
    client = OpenAI(api_key = OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[{
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": 'First image is a drawing, second image is a actual photo containing 2 pentagons, overlapped on one side, lets call it main image. please tell if the drawing resembeles the main image. score it 1 if all 10 sides present and its overlapping on one side, score it 0 if its not score is 0, no partial score. Write description of what you see, also please use the this format, example 1: {score: 1, description: "all 10 sides present and its overlapping on one side"}, example 2: {score: 0, description: "This image has a circle and a square, and it doesnt resemble main image, only 4 straight sides"}, follow this json strictly, dont give me any other information, just make sure its valid json. also be little lenient as old people might not be able to draw perfectly, but if its close to main image, give it a 1.',
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{encoded}",
            },
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{main_image}",
            },
            },
        ],
        }
    ],
    max_tokens=100,
    )
    content = response.choices[0].message.content
    print(content[content.find("{"):content.find("}")+1])
    content = content[content.find("{"):content.find("}")+1]
    # convert content to json and return score, description
    score, description = json.loads(content)['score'], json.loads(content)['description']
    print(score, description)
    return score, description


def get_gpt_score(prompt):
    client = OpenAI(
        api_key=OPENAI_API_KEY,
    )

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to score MMSE TEST that is voice recorded and captured using a not so great Speech to text, you were meant to be smart and understand and act as NLP so that evaluation might be fair, ignore punctuations, backslash n and etc, also output JSON. one of them is `score` and other is `explanation` Please respond with a valid JSON object. "},
            {"role": "user", "content": prompt}
        ]
    )

    # Assuming the response is a valid JSON object
    return json.loads(response.choices[0].message.content)

def process_report(report):
    total_score = 0

    for key, value in report.items():
        prompt = ""
        needs_scoring = False

        if key in ["Year", "Month", "Day", "DayOfWeek", "Season"]:
            # These are straightforward comparisons
            needs_scoring = True
            spoken_text = str(value.get('spoken_text', '')).strip()
            correct_answer = str(value.get('correct'))
            prompt = f"Score the response '{spoken_text.lower()}' against the correct answer '{correct_answer.lower()}'. Provide a score of 1 for correct and 0 for incorrect. be liberal in scoring, if the answer is close to correct, give it a 1. as this is taken from voice recording, like date and month might contain more info or in different format, like numbers for month or more words than necessary, since it can be a sentence. if correct answer presents in the spoken text, give it a 1."

        elif key == "three_things":
            # Similar straightforward comparison, but the response might be a list
            needs_scoring = True
            spoken_text = " ".join(value.get('spoken_text', '').strip().split())
            correct_answer = value.get('correct')
            prompt = f"Score the response '{spoken_text.lower()}' against the correct answer '{correct_answer.lower()}'. Provide a score of 1 for correct and 0 for incorrect. Be liberal, this is from voice recordings, so if the answer is close to correct, give it a 1. if correct answer presents in the spoken text also give it a 1. just check if three things are present"

        elif key == "reverse_word":
            # Scoring for reversed word
            needs_scoring = True
            spoken_text = value.get('spoken_text', '').strip().replace(",", "").replace(" ", "")
            correct_answer = value.get('correct')
            prompt = f"Score the response '{spoken_text.lower()}' against the correct answer '{correct_answer.lower()}'. Provide a score of 1 for correct and 0 for incorrect. be lenient in scoring, if the answer is close to correct, give it a 1. as this is taken from voice recording using SST module therefore it won't be straigh, may contain punctuations and etc, just ignore them."


        if key == "three_things_repeat":
            needs_scoring = True
            spoken_text = " ".join(value.get('spoken_text', '').strip().split())
            correct_answer = value.get('correct')
            prompt = f"Score the response '{spoken_text.lower()}' against the correct answer '{correct_answer.lower()}' with 1 or 0. Be liberal in scoring, if the answer is close to correct, give it a 1. as this is taken from voice recording, just check if three things are present"

        elif key in ["image1", "image2"]:
            needs_scoring = True
            spoken_text = value.get('spoken_text', '').strip()
            correct_answer = value.get('correct')
            prompt = f"Score the response '{spoken_text.lower()}' against the correct answer '{correct_answer.lower()}' with 1 or 0. Be liberal in scoring, if the answer is close to correct or even contains the word, give it a 1. as this is taken from voice recording"

        elif key == "phrase":
            needs_scoring = True
            spoken_text = value.get('spoken_text', '').strip()
            correct_answer = value.get('correct')
            prompt = f"Score the response '{spoken_text.lower()}' against the correct answer '{correct_answer.lower()}' with 1 or 0. Be liberal in scoring, if the answer is close to correct, give it a 1. as this is taken from voice recording the punctuation is not important, but the words are important, that is it should have if, and, but. they might be with a 's' like ifs, ands, buts, but it should be there in some form or another, even if one of them is missing give 0."

        elif key == "words":
            needs_scoring = True
            chosen_word = value.get('chosen_word', '').strip()
            correct_word = value.get('correct')
            prompt = f"Score the chosen word '{chosen_word.lower()}' against the correct word '{correct_word.lower()}'. with 1 or 0. Be liberal in scoring, if the answer is close to correct, give it a 1. as this is taken from voice recording"

        elif key == "clock":
            needs_scoring = True
            hour = value.get('time', {}).get('hour', 0)
            minute = value.get('time', {}).get('minute', 0)
            correct_hour = value.get('correct', {}).get('hour', 0)
            correct_minute = value.get('correct', {}).get('minute', 0)
            prompt = f"Score the time {hour}:{minute} against the correct time {correct_hour}:{correct_minute}. with 1 or 0. Be liberal, use common sense, as this is taken from voice recording, for example 00 is same as 60 in minutes and etc."

        elif key == "sentence":
            needs_scoring = True
            spoken_text = value.get('spoken_text', '').strip()
            prompt = f"Analyze the sentence '{spoken_text.lower()}' and score 1 if it contains at least one noun and one verb, otherwise score 0. this is taken from voice recording using STT, so please be understanding."


        if needs_scoring:
            json_response = get_gpt_score(prompt)
            score = json_response.get("score", 0)
            explanation = json_response.get("explanation", "")
            report[key]['score'] = score
            report[key]['explanation'] = explanation
            total_score += score

    report['total_score'] = total_score

def process_mmse_report(results):
    process_report(next(iter(results.values())))
    print(json.dumps(results, indent=4))
    return results



def generate_html(data):
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MMSE Report</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-50 p-8">
    <div class="max-w-4xl mx-auto">
        <h1 class="text-2xl font-bold text-gray-800 mb-6">Mini-Mental State Examination (MMSE) Report</h1>
        <div class="bg-white shadow-md rounded-lg p-6">
            <div class="grid grid-cols-1 gap-4">
    """
    
    for date, sections in data.items():
        for section, details in sections.items():
            if section == "drawing":
                html_content += f'<div class="border-b pb-4"><h2 class="text-xl font-semibold text-gray-700">{section}</h2>'
                html_content += f'<p><strong>Score:</strong> {details["score"]}</p>'
                html_content += f'<p><strong>Description:</strong> {details["description"]}</p>'
                # image
                html_content += f'<img src="{"drawing.png"}" alt="Drawing" class="mt-4">'
                html_content += '</div>'
            elif section == "total_score":
                html_content += f'<div class="mt-4"><h3 class="text-lg font-semibold text-gray-700">Total Score: {details}</h3></div>'
            else:
                html_content += f'<div class="border-b pb-4"><h2 class="text-xl font-semibold text-gray-700">{section}</h2>'
                for key, value in details.items():
                    if key not in ['score', 'description']:  # Adjust based on JSON structure
                        html_content += f'<p><strong>{key.capitalize()}:</strong> {value}</p>'
                if 'score' in details:
                    html_content += f'<p><strong>Score:</strong> {details["score"]}</p>'
                html_content += '</div>'
    
    html_content += """
            </div>
        </div>
    </div>
</body>
</html>
    """
    return html_content

j = {
    "2024-01-29 00:37:57.452163": {
        "Year": {
            "question": "What is the current year?",
            "spoken_text": "2024",
            "correct": 2024,
            "score": 1
        },
        "Month": {
            "question": "What is the current month?",
            "spoken_text": "January.",
            "correct": "January",
            "score": 1
        },
        "Day": {
            "question": "What is the date today?",
            "spoken_text": "29th",
            "correct": 29,
            "score": 1
        },
        "DayOfWeek": {
            "question": "What is the current day of the week?",
            "spoken_text": "Monday.",
            "correct": "Monday",
            "score": 1
        },
        "Season": {
            "question": "what is the current season?",
            "spoken_text": "winter",
            "correct": "Winter",
            "score": 0
        },
        "three_things": {
            "spoken_text": "phone, sweater, lake.",
            "correct": "phone sweater lake",
            "score": 1
        },
        "reverse_word": {
            "spoken_text": "G.O.D.",
            "correct": "GOD",
            "score": 1
        },
        "three_things_repeat": {
            "spoken_text": "phone, sweater, leg.",
            "correct": "phone sweater lake",
            "score": 1
        },
        "image1": {
            "spoken_text": "airplane.",
            "correct": "airplane",
            "score": 1
        },
        "image2": {
            "spoken_text": "car",
            "correct": "car",
            "score": 1
        },
        "phrase": {
            "spoken_text": "No ifs, ands, or buts.",
            "correct": "No ifs, ands, or buts",
            "score": 1
        },
        "words": {
            "chosen_word": "happy",
            "correct": "happy",
            "score": 0
        },
        "clock": {
            "time": {
                "hour": 11,
                "minute": 25
            },
            "correct": {
                "hour": 11,
                "minute": 25
            },
            "score": 1
        },
        "sentence": {
            "spoken_text": "I like computer programming.",
            "score": 1
        },
        "drawing": {
            "score": 1,
            "description": "all 10 sides present and its overlapping on one side"
        },
        "total_score": 12
    }
}

# h = generate_html(j)

# with open("report.html", "w") as f:
#     f.write(h)
#     f.close()




