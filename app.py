from flask import Flask, request, jsonify

app = Flask(__name__)

center_stock = {
    'C1': {'A': 3, 'B': 2, 'C': 8},
    'C2': {'D': 12, 'E': 25, 'F': 15},
    'C3': {'G': 0.5, 'H': 1, 'I': 2}
}

product_weights = {
    'A': 3, 'B': 2, 'C': 8,
    'D': 12, 'E': 25, 'F': 15,
    'G': 0.5, 'H': 1, 'I': 2
}

initial_cost_per_unit = 10
additional_cost_per_unit = 8
weight_threshold = 5

@app.route('/calculate_cost', methods=['POST'])
def calculate_cost():
    order = request.json

    total_cost = 0
    product_available = False
    for product, quantity in order.items():
        if product in product_weights:
            product_available = True
            break
    
    if not product_available:
        return jsonify({'error': 'Products not available at any center'}), 400

    for product, quantity in order.items():
        remaining_quantity = quantity

        # Iterate over each center's stock to calculate the cost
        for center, stock in center_stock.items():
            if product in stock:
                available_quantity = stock[product]
                if available_quantity > 0:
                    quantity_to_use = min(available_quantity, remaining_quantity)
                    total_weight = quantity_to_use * product_weights[product]
                    total_cost += calculate_product_cost(total_weight)
                    remaining_quantity -= quantity_to_use

                    # Update stock
                    center_stock[center][product] -= quantity_to_use

            if remaining_quantity == 0:
                break

    return jsonify({'minimum_cost': total_cost})

def calculate_product_cost(total_weight):
    if total_weight <= weight_threshold:
        return total_weight * initial_cost_per_unit
    else:
        additional_weight = total_weight - weight_threshold
        additional_cost = (additional_weight // 5) * additional_cost_per_unit
        return total_weight * initial_cost_per_unit + additional_cost

if __name__ == '__main__':
    app.run(debug=True)
