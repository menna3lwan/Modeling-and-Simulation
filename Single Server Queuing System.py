import random
#installin Prettytable package
from prettytable import PrettyTable

random.seed(10)

num_customers = 10

customers = [i for i in range(1, num_customers + 1)]

inter_arrival_times = [random.randrange(1, 10) for _ in range(num_customers)]

service_times = [random.randrange(1, 10) for _ in range(num_customers)]

arrival_times = [0] * num_customers
arrival_times[0] = inter_arrival_times[0]
for i in range(1, num_customers):
    arrival_times[i] = inter_arrival_times[i] + arrival_times[i - 1]

time_service_begins = [0] * num_customers
time_customer_waits = [0] * num_customers
time_service_ends = [0] * num_customers
time_customer_spends = [0] * num_customers
system_idle_times = [0] * num_customers

time_service_begins[0] = arrival_times[0]
time_service_ends[0] = service_times[0]
time_customer_spends[0] = service_times[0]

for i in range(1, num_customers):
    time_service_begins[i] = max(arrival_times[i], time_service_ends[i - 1])
    time_customer_waits[i] = time_service_begins[i] - arrival_times[i]
    time_service_ends[i] = time_service_begins[i] + service_times[i]
    time_customer_spends[i] = time_service_ends[i] - arrival_times[i]
    if arrival_times[i] > time_service_ends[i - 1]:
        system_idle_times[i] = arrival_times[i] - time_service_ends[i - 1]
    else:
        system_idle_times[i] = 0

table = PrettyTable()
table.field_names = ['Customer', 'IAT', 'AT', 'ST', 'TSB', 'TCWQ', 'TSE', 'TCSS', 'System Idle']
for i in range(num_customers):
    table.add_row([customers[i], inter_arrival_times[i], arrival_times[i], service_times[i],
                   time_service_begins[i], time_customer_waits[i], time_service_ends[i],
                   time_customer_spends[i], system_idle_times[i]])

print(table)

average_waiting_time = sum(time_customer_waits) / num_customers
prob_customer_waiting = len([t for t in time_customer_waits if t > 0]) / num_customers
average_service_time = sum(service_times) / num_customers
prob_idle_server = sum(system_idle_times) / time_service_ends[-1]
average_time_between_arrival = arrival_times[-1] / (len(arrival_times) - 1)
average_waiting_time_for_waiting_customers = sum(time_customer_waits) / len([t for t in time_customer_waits if t > 0])
average_time_spent_in_system = sum(time_customer_spends) / num_customers

print("Average waiting time: {:.2f} minutes".format(average_waiting_time))
print('-' * 50)

print("Probability of customer waiting: {:.2f}".format(prob_customer_waiting))
print('-' * 50)

print("Average service time: {:.2f} minutes".format(average_service_time))
print('-' * 50)

print("Probability of idle server: {:.2f}".format(prob_idle_server))
print('-' * 50)

print("Average time between arrivals: {:.2f} minutes".format(average_time_between_arrival))
print('-' * 50)

print("Average waiting time for those who wait: {:.2f} minutes".format(average_waiting_time_for_waiting_customers))
print('-' * 50)

print("Average time customer spent in the system: {:.2f} minutes".format(average_time_spent_in_system))