from flask import Flask, render_template, request

from one import \
    summerizer  # Assuming the summarizer function is defined in one.py

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", summarized_text="", len_org=0, len_sum=0)  # Render the index.html template

@app.route('/summarize', methods=["GET", "POST"])
def summarize():
    if request.method == "POST":
        rawtext = request.form["rawtext"]
        summary,og_txt,len_og, len_sum,senti = summerizer(rawtext)  # Call the summarizer function
        
        label=senti[0]['label']  # Extract the sentiment label from the sentiment analysis result
        score=senti[0]['score']  # Extract the sentiment score from the sentiment analysis result
        
    return render_template("summarize.html", summarized_text=summary,og_txt=og_txt, len_org=len_og, len_sum=len_sum,label=label,score=score)  # Render the index.html template with the summarized text and original and summarized text lengths

# ///////////////////////////////////////////////////
        

# @app.route('/home', methods=["GET", "POST"])
# def home():
#     return render_template("home.html")  # Render the home.html template

# //////////////////////////////////////////////////

# @app.route('/analyze', methods=["GET", "POST"])
# def analyze():
#      # Get sentiment analysis result from the summarizer function
#     if request.method == "POST":
#         sentiment,summary = summerizer(rawtext)
#     return render_template("sentiment.html", sentiment=sentiment)
    


if __name__ == "__main__":
    app.run(debug=True)
