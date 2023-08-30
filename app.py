from flask import Flask, render_template, request, session, redirect, url_for

from assistant import Assistant
from config import PATH_TO_BOOK, MODEL

app = Flask(__name__)

# Set a secret key for sessions
app.secret_key = 'asdfghjkl'

# Initialize the BookAssistant
assistant = Assistant(PATH_TO_BOOK, MODEL)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        user_question = request.form['question']
        
        # Use the Assistant to get the response
        response = assistant.process_question(user_question)
        # response = user_question
        
        # Store the response in the session
        session['response'] = response

        session['visited'] = False

        # Redirect to the same route (or another route if desired)
        return redirect(url_for('index'))
    
    else:
        # If the 'visited' session variable exists, clear the session
        if session['visited']:
            session.clear()
        # Set the 'visited' session variable to indicate the page has been visited
        session['visited'] = True

    return render_template('index.html', response=session.get('response', ""))

if __name__ == '__main__':
    # app.run(debug=True)
    app.run()
