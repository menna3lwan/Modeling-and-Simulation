import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(10)

number_of_customers=int(input("please enter number of customers : "))

interarrival_time_list=[]
cumm_time=0

size_interval=0
number_probability=int(input("enter number of probapility of interarrival time : "))
def add_fractions(a, b):
    if a != 0:
        max_decimal_places = max(len(str(a).split('.')[1]), len(str(b).split('.')[1]))
        result = float(a) + b
        formatted_result = "{:.{}f}".format(result, max_decimal_places)
        return formatted_result
    else:
        return b

interarrival_time_list = []
cummulative = 0
end_prob=0


for i in range(number_probability):
    while True:
        try:
            interarrival_time = int(input(f'Enter interarrival time of {i+1}: '))
            probability = float(input(f'Enter probability of {i+1}: '))

            if probability < 0 or probability > 1:
                print("Probability must be between 0 and 1.")
                continue

            if float(cummulative) + probability > 1:
                print("The sum of probabilities cannot exceed 1. Please enter a lower probability.")
                continue

            cummulative = add_fractions(cummulative, probability)

            end = end_prob
            end_prob = int(str(cummulative).split('.')[1])

            if size_interval < len(str(end_prob)):
                size_interval = len(str(end_prob))

            Random_digit_assignment = [1 + end, end_prob]
            interarrival_time_list.append([interarrival_time, probability, cummulative, Random_digit_assignment])

            break
        except ValueError:
            print("Please enter a valid number.")

interarrival_time_list=np.array(interarrival_time_list,dtype=object)

cumm_time=0
cummulative=0
end_prob=0
services_time_list=[]
size_service=0
number_probability=int(input("enter number of probapility of service time : "))
for i in range(number_probability):
    while True:
        try:
            service_time = int(input(f'Enter service time of {i+1}: '))
            probability = float(input(f'Enter probability of {i+1}: '))

            if probability < 0 or probability > 1:
                print("Probability must be between 0 and 1")
                continue

            if float(cummulative) + probability > 1:
                print("The sum of probabilities cannot exceed 1. Please enter a lower probability.")
                continue

            cummulative += probability

            end = end_prob
            end_prob = int(str(cummulative).split('.')[1])

            if size_service < len(str(end_prob)):
                size_service = len(str(end_prob))

            Random_digit_assignment = [1 + end, end_prob]
            services_time_list.append([service_time, probability, cummulative, Random_digit_assignment])

            break
        except ValueError:
            print("Please enter a valid number.")
services_time_list=np.array(services_time_list,dtype=object)