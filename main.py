from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
s1 = 0
s2 = 0
choice1 = ''
choice2 = ''
last_choice1 = ''
last_choice2 = ''
ok = False
round_number = 0

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/p1')
def indexp1():
    return render_template("htmlp1.html")

@app.route('/p2')
def indexp2():
    return render_template("htmlp2.html")

@app.route('/runp1/<c1>', methods=["POST"])
def setc1(c1):
    global choice1
    choice1 = c1
    return check_run()

@app.route('/runp2/<c2>', methods=["POST"])
def setc2(c2):
    global choice2
    choice2 = c2
    return check_run()

def check_run():
    global s1, s2, choice1, choice2, last_choice1, last_choice2, ok, round_number
    if choice1 != '' and choice2 != '':
        last_choice1 = choice1
        last_choice2 = choice2
        if choice1 == 'green' and choice2 == 'green':
            s1 += 3
            s2 += 3
        elif choice1 == 'red' and choice2 == 'red':
            s1 += 1
            s2 += 1
        elif choice1 == 'red' and choice2 == 'green':
            s1 += 5
        elif choice1 == 'green' and choice2 == 'red':
            s2 += 5
        choice1 = ''
        choice2 = ''
        round_number += 1
        ok = True
    return jsonify(s1=s1, s2=s2, round=round_number, ok=ok)

@app.route('/status')
def status():
    return jsonify(
        s1=s1, s2=s2, round=round_number, ok=ok,
        last_choice1=last_choice1, last_choice2=last_choice2
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
