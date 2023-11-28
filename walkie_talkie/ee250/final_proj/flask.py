from flask import Flask, jsonify, render_template, redirect, url_for

app = Flask('final_proj')

@app.route('/')
def index():
    global TRANSCRIPT
    return render_template('index.html', user_input=TRANSCRIPT)


@app.route('/client_callback')


if __name__ == '__main__':
    client.loop_start()
    app.run(debug=False)
