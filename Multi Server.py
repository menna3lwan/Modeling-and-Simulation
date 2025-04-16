import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set random seed for reproducibility
np.random.seed(10)

# Function to input probabilities and create a list
def input_probabilities(prompt_prefix, num_probs):
    prob_list = []
    cumulative_prob = 0
    for i in range(num_probs):
        while True:
            try:
                time = int(input(f"{prompt_prefix} {i + 1}: "))
                probability = float(input(f"Enter probability {i + 1}: "))
                if not (0 <= probability <= 1):
                    print("Probability must be between 0 and 1.")
                    continue
                if cumulative_prob + probability > 1:
                    print("The sum of probabilities cannot exceed 1. Please enter a lower probability.")
                    continue
                cumulative_prob += probability
                prob_list.append([time, probability, cumulative_prob])
                break
            except ValueError:
                print("Please enter a valid number.")
    return np.array(prob_list, dtype=object)

# Input for number of customers
num_customers = int(input("Enter the number of customers: "))

# Input for interarrival time probabilities
num_interarrival_probs = int(input("Enter the number of probabilities for interarrival time: "))
interarrival_time_list = input_probabilities("Enter interarrival time", num_interarrival_probs)

# Input for service time probabilities for Server 1
num_service_probs_s1 = int(input("Enter the number of probabilities for service time (Server 1): "))
service_time_list_s1 = input_probabilities("Enter service time (Server 1)", num_service_probs_s1)

# Input for service time probabilities for Server 2
num_service_probs_s2 = int(input("Enter the number of probabilities for service time (Server 2): "))
service_time_list_s2 = input_probabilities("Enter service time (Server 2)", num_service_probs_s2)

# Input for number of iterations
num_iterations = int(input("Enter the number of iterations: "))

# Simulation loop
server1_busy = []
server2_busy = []
waiting_time = []
probability_waiting_time = []

for _ in range(num_iterations):
    # Generate time between arrivals
    time_between_arrivals = np.zeros((num_customers, 3), dtype='int32')
    for i in range(1, num_customers):
        rand = np.random.rand()
        for j, (inter_time, _, cum_prob) in enumerate(interarrival_time_list):
            if rand <= cum_prob:
                time_between_arrivals[i] = [i, rand, inter_time]
                break

    # Initialize solution and time service arrays
    solution = np.zeros((num_customers, 10))
    time_service = np.zeros((num_customers, 3))

    # Process customers
    m, n = 0, 0
    for i in range(num_customers):
        solution[i][0] = i
        solution[i][1] = time_between_arrivals[i][2]
        solution[i][2] = solution[i][1] + solution[i - 1][2] if i > 0 else 0

        if i == 0:
            # First customer
            time_service[i][0] = i
            rand = np.random.rand()
            for j, (service_time, _, cum_prob) in enumerate(service_time_list_s1):
                if rand <= cum_prob:
                    time_service[i][2] = service_time
                    break

            solution[m][3] = 0
            solution[m][4] = time_service[m][2]
            solution[m][5] = time_service[m][2]
            m = i
            n = i
        elif solution[i][2] < solution[m][5] and solution[i][2] >= solution[n][8]:
            # Assign to Server 2
            time_service[i][0] = i
            rand = np.random.rand()
            for j, (service_time, _, cum_prob) in enumerate(service_time_list_s2):
                if rand <= cum_prob:
                    time_service[i][2] = service_time
                    break

            solution[i][6] = max(solution[n][8], solution[i][2])
            solution[i][7] = time_service[i][2]
            solution[i][8] = solution[i][6] + solution[i][7]
            n = i
            if solution[i][2] - solution[n][8] > 0:
                solution[i][9] = solution[i][2] - solution[n][8]
        else:
            # Assign to Server 1
            time_service[i][0] = i
            rand = np.random.rand()
            for j, (service_time, _, cum_prob) in enumerate(service_time_list_s1):
                if rand <= cum_prob:
                    time_service[i][2] = service_time
                    break

            solution[i][3] = max(solution[m][5], solution[i][2])
            solution[i][4] = time_service[i][2]
            solution[i][5] = solution[i][3] + solution[i][4]
            m = i
            if solution[i][2] - solution[m][5] > 0:
                solution[i][9] = solution[i][2] - solution[m][5]

    # Create DataFrame for results
    df = pd.DataFrame(solution[:, 1:], columns=[
        'Interarrival Time', 'Arrival Time', 'Service Begin S1',
        'Service Time S1', 'Service End S1', 'Service Begin S2',
        'Service Time S2', 'Service End S2', 'Waiting in Queue'
    ])

    # Calculate metrics
    server1_busy.append(df['Service Time S1'].sum() / solution[m][5])
    server2_busy.append(df['Service Time S2'].sum() / solution[n][8])
    waiting_time.append(df['Waiting in Queue'].sum() / num_customers)
    probability_waiting_time.append(df['Waiting in Queue'][df['Waiting in Queue'] > 0].count() / num_customers)

# Plot results
plt.hist(server1_busy, bins=10, edgecolor='black')
plt.title('Server 1 Utilization')
plt.xlabel('Utilization')
plt.ylabel('Frequency')
plt.show()

plt.hist(server2_busy, bins=10, edgecolor='black')
plt.title('Server 2 Utilization')
plt.xlabel('Utilization')
plt.ylabel('Frequency')
plt.show()

plt.hist(waiting_time, bins=10, edgecolor='black')
plt.title('Average Waiting Time')
plt.xlabel('Time')
plt.ylabel('Frequency')
plt.show()

plt.hist(probability_waiting_time, bins=10, edgecolor='black')
plt.title('Probability of Waiting Time')
plt.xlabel('Probability')
plt.ylabel('Frequency')
plt.show()