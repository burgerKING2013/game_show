from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

htmlp1 = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Game Show</title>
  <style>
    body { font-family: Arial, sans-serif; text-align: center; background: #f4f4f4; }
    h1 { color: #333; }
    .scoreboard { margin: 20px; font-size: 20px; }
    .buttons { display: flex; justify-content: center; gap: 50px; margin: 20px; }
    .player { border: 2px solid #333; padding: 20px; background: #fff; }
    button { font-size: 18px; padding: 10px 20px; margin: 10px; cursor: pointer; }
    .red { background: crimson; color: white; }
    .green { background: seagreen; color: white; }
  </style>
</head>
<body>
  <h1>Game Show</h1>
  <div class="scoreboard">
    <p>Round: <span id="round">1</span> / 30</p>
    <p>Player 1 Score: <span id="score1">0</span></p>
    <p>Player 2 Score: <span id="score2">0</span></p>
  </div>

  <div class="buttons">
    <div class="player">
      <h2>Player 1</h2>
      <button class="green" onclick="choose('green')">Green</button>
      <button class="red" onclick="choose('red')">Red</button>
    </div>
  </div>

  <p id="message"></p>

  <script>
    let choice1 = null, choice2 = null;
    let round = 1;

    function choose(color) {
      if (round > 30) {
        document.getElementById("message").innerText = "Game Over!";
        return;
      }

      choice1 = color;

      if (choice1) {
        fetch(`/runp1/${choice1}`, {method: "POST"})
        .then(r => r.json())
        .then(data => {
          document.getElementById("score1").innerText = data.s1;
          document.getElementById("score2").innerText = data.s2;
          document.getElementById("round").innerText = round;
          choice2 = data.cchoice2
          document.getElementById("message").innerText =`Round ${round}: Player 1 chose ${choice1}, Player 2 chose ${choice2}`;
          // Reset
          choice1 = null;
          choice2 = null;
          round=data.round;
        });
      }
    }
  </script>
</body>
</html>
"""

htmlp2 = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Game Show</title>
  <style>
    body { font-family: Arial, sans-serif; text-align: center; background: #f4f4f4; }
    h1 { color: #333; }
    .scoreboard { margin: 20px; font-size: 20px; }
    .buttons { display: flex; justify-content: center; gap: 50px; margin: 20px; }
    .player { border: 2px solid #333; padding: 20px; background: #fff; }
    button { font-size: 18px; padding: 10px 20px; margin: 10px; cursor: pointer; }
    .red { background: crimson; color: white; }
    .green { background: seagreen; color: white; }
  </style>
</head>
<body>
  <h1>Game Show</h1>
  <div class="scoreboard">
    <p>Round: <span id="round">1</span> / 30</p>
    <p>Player 1 Score: <span id="score1">0</span></p>
    <p>Player 2 Score: <span id="score2">0</span></p>
  </div>

  <div class="buttons">
    <div class="player">
      <h2>Player 2</h2>
      <button class="green" onclick="choose('green')">Green</button>
      <button class="red" onclick="choose('red')">Red</button>
    </div>
  </div>

  <p id="message"></p>

  <script>
    let choice1 = null, choice2 = null;
    let round = 1;

    function choose(color) {
      if (round > 30) {
        document.getElementById("message").innerText = "Game Over!";
        return;
      }

      choice2 = color;

      if (choice2) {
        fetch(`/runp2/${choice2}`, {method: "POST"})
        .then(r => r.json())
        .then(data => {
          document.getElementById("score1").innerText = data.s1;
          document.getElementById("score2").innerText = data.s2;
          document.getElementById("round").innerText = round;
          choice1 = data.cchoice1
          document.getElementById("message").innerText =`Round ${round}: Player 1 chose ${choice1}, Player 2 chose ${choice2}`;
          // Reset
          choice1 = null;
          choice2 = null;
          round=data.round;
        });
      }
    }
  </script>
</body>
</html>
"""

s1 = 0
s2 = 0
choice1 = ''
choice2 = ''

@app.route('/p1')
def indexp1():
    return render_template_string(htmlp1)
@app.route('/p2')
def indexp2():
    return render_template_string(htmlp2)

@app.route('/runp1/<c1>', methods=["POST"])
def setc1(c1):
    global choice1
    choice1 = c1
    print("OK1 ")
    if(choice1!='' and choice2!=''):
      run(choice1,choice2)
    return jsonify(s1=s1, s2=s2)
    
@app.route('/runp2/<c2>', methods=["POST"])
def setc2(c2):
    global choice2
    choice2 = c2
    if(choice1!='' and choice2!=''):
      run(choice1,choice2)
    return jsonify(s1=s1,s2=s2)

def run(c1, c2):
  global s1, s2, choice1, choice2, round

  if c1 == 'green' and c2 == 'green':
      s1 += 3
      s2 += 3
  elif c1 == 'red' and c2 == 'red':
      s1 += 1
      s2 += 1
  elif c1 == 'red' and c2 == 'green':
      s1 += 5
  elif c1 == 'green' and c2 == 'red':
      s2 += 5

  round = round + 1

  return jsonify(s1=s1, s2=s2, round=round)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5001, debug=True)
