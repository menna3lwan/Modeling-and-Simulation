import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set random seed for reproducibility
np.random.seed(2)


def create_probability_list(num_items, item_name):
    probability_list = []
    cumulative = 0.0
    for i in range(num_items):
        item = int(input(f"Enter {item_name} {i}: "))
        probability = float(input(f"Enter probability of {item_name} {i}: "))
        cumulative += probability
        random_digit_assignment = [int(cumulative * 10 ** size) for size in range(1, 6)]
        probability_list.append([item, probability, cumulative, random_digit_assignment])
    return np.array(probability_list, dtype=object)


# Create demand list
number_probability_1 = int(input("Enter number of demands: "))
demand_list = create_probability_list(number_probability_1, "demand")

# Create lead time list
number_probability_2 = int(input("Enter number of lead times: "))
lead_time_list = create_probability_list(number_probability_2, "lead time")

# Simulation parameters
M = 500
N = 12
Cycle = 50
init_inv = 100
order = 8
Time_recive = 1

# Initialize simulation array
simulation = np.zeros((N * Cycle + 1, 10))

# Simulation loop
for i in range(N * Cycle):
    cycle = i // N
    day = i % N
    simulation[i, 0] = cycle
    simulation[i, 1] = day

    # Random demand
    rand = np.random.randint(0, 10 ** 5)
    for k in range(number_probability_1 - 1):
        if demand_list[k][3][0] <= rand <= demand_list[k][3][1]:
            simulation[i, 4] = demand_list[k][0]
            break
    else:
        simulation[i, 4] = demand_list[-1][0]

    # Inventory logic
    if i == 0:
        simulation[i, 2] = init_inv
    else:
        simulation[i, 2] = simulation[i - 1, 5]

    simulation[i, 5] = simulation[i, 2] - simulation[i, 4]

    # Shortage logic
    if simulation[i, 4] > simulation[i, 2]:
        simulation[i, 6] = simulation[i, 4] - simulation[i, 2]

    # Order logic
    if simulation[i, 9] == 0:
        simulation[i + 1, 2] += order - simulation[i, 6]

    # Lead time logic
    if (i + 1) % N == 0:
        rand = np.random.randint(0, 10 ** 5)
        for k in range(number_probability_2 - 1):
            if lead_time_list[k][3][0] <= rand <= lead_time_list[k][3][1]:
                simulation[i, 9] = lead_time_list[k][0]
                break
        else:
            simulation[i, 9] = lead_time_list[-1][0]

    # Update days until order arrives
    if simulation[i, 9] != 0:
        simulation[i + 1, 9] = simulation[i, 9] - 1

# Create DataFrame
df = pd.DataFrame(simulation[:-1, :], columns=['Cycle', 'Day', 'Begining Inventory',
                                               'Random digits for Demand', 'Demand',
                                               'Ending Inventory', 'Shorting Quantity',
                                               'Order Quantity', 'Random digits for lead time',
                                               'Days until Order Arrrives'])

# Plot inventory levels
plt.plot(df['Day'], df['Begining Inventory'])
plt.xlabel('Day')
plt.ylabel('Begining Inventory')
plt.show()

# Save to CSV
df.to_csv('Inventory3.csv', index=False)