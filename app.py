from flask import Flask, render_template, jsonify, request
import processor
from processor import set_flag,get_flag


app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html', **locals())



@app.route('/chatbot', methods=["GET", "POST"])
def chatbotResponse():

    if request.method == 'POST':
        the_question = request.form['question']
        f = get_flag()
        if f == 0:
            response = processor.chatbot_response(the_question)
            return jsonify({"response": response })
        else:
            response = processor.fetch_profile_data(the_question)
            return jsonify({"response": response })


    



if __name__ == '__main__':
    app.run(debug=True)

