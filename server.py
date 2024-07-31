from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import math

app = Flask(__name__)

# Swagger configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Calculatrice RPN API"})
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


def evaluate_rpn(expression):

    if expression is None or expression == "":
        raise Exception("L'expression a evaluer est nulle ou vide.")

    # Il faut 3 elements a minima: 2 nombres et un operateur
    if len(expression) < 3:
        raise Exception('Expression a evaluer pas assez longue.')

    # TODO Ajouter une expression regex pour verifier la validite de l'expression passee

    stack = []
    for token in expression:
        if token in ['+', '-', '*', '/', '^']:
            # Ensure there are enough operands in the stack
            if len(stack) < 2:
                raise ValueError("Invalid RPN expression: not enough operands in the stack.")
            b = stack.pop() # Récupération du dernier élément de la pile
            a = stack.pop() # Récupération du dernier élément de la pile
            if token == '+': # Opération +
                result = a + b
            elif token == '-': # Opération -
                result = a - b
            elif token == '*': # Opération *
                result = a * b
            elif token == '^': # Opération ^
                result = a ** b
            elif token == '/': # Opération /
                if b == 0:
                    raise ValueError("Division par zero.")
                result = a / b

            # Ajout de l'élément dans la pile
            stack.append(result)
        else:
            try:
                stack.append(float(token))
            except ValueError:
                raise ValueError("Invalid token.")
    if len(stack) != 1:
        raise ValueError("Invalid RPN expression.")
    return stack[0]


@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    if not data or 'expression' not in data:
        return jsonify({'error': 'Invalid input.'}), 400
    try:
        expression = data['expression']
        result = evaluate_rpn(expression)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
