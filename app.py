from flask import Flask, jsonify, render_template_string
from calculator import add, subtract, multiply, divide

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SIT707 CI/CD Calculator</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; padding: 20px; }
        h1 { color: #4285f4; }
        input { width: 80px; padding: 8px; margin: 5px; font-size: 16px; }
        button { padding: 8px 16px; margin: 5px; background: #4285f4; color: white; border: none; cursor: pointer; border-radius: 4px; font-size: 14px; }
        button:hover { background: #357abd; }
        #result { margin-top: 20px; font-size: 24px; font-weight: bold; color: #333; padding: 10px; background: #f0f0f0; border-radius: 4px; }
        .error { color: red; }
    </style>
</head>
<body>
    <h1>SIT707 Calculator</h1>
    <p>Deployed via GCP Cloud Build CI/CD Pipeline</p>
    <input type="number" id="a" placeholder="A" />
    <input type="number" id="b" placeholder="B" />
    <br>
    <button onclick="calc('add')">Add</button>
    <button onclick="calc('subtract')">Subtract</button>
    <button onclick="calc('multiply')">Multiply</button>
    <button onclick="calc('divide')">Divide</button>
    <div id="result">Enter numbers and click an operation</div>
    <script>
        async function calc(op) {
            const a = document.getElementById('a').value;
            const b = document.getElementById('b').value;
            if (!a || !b) { document.getElementById('result').innerHTML = '<span class="error">Please enter both numbers</span>'; return; }
            const res = await fetch(`/${op}/${a}/${b}`);
            const data = await res.json();
            const resultDiv = document.getElementById('result');
            if (data.result !== undefined) {
                resultDiv.innerHTML = `${a} ${op} ${b} = <strong>${data.result}</strong>`;
                resultDiv.style.color = '#333';
            } else {
                resultDiv.innerHTML = `<span class="error">Error: ${data.error}</span>`;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/add/<int:a>/<int:b>')
def add_route(a, b):
    return jsonify({"result": add(a, b)})

@app.route('/subtract/<int:a>/<int:b>')
def subtract_route(a, b):
    return jsonify({"result": subtract(a, b)})

@app.route('/multiply/<int:a>/<int:b>')
def multiply_route(a, b):
    return jsonify({"result": multiply(a, b)})

@app.route('/divide/<int:a>/<int:b>')
def divide_route(a, b):
    try:
        return jsonify({"result": divide(a, b)})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
