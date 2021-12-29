import math
import random

amount = bigs = initial_inv_level = inv_level = next_event_type = num_events = num_months = num_values_demand = smalls = 0

area_holding = area_shortage = holding_cost = incremental_cost = maxlag = mean_interdemand = minlag = setup_cost = shortage_cost = sim_time = time_last_event = time_since_last_event = total_ordering_cost = 0.0

prob_distrib_demand = [0] * 26
time_next_event = [0] * 3

prob_distrib = []
num_events = 4


def initialization():

    global sim_time, inv_level, initial_inv_level, time_last_event, total_ordering_cost, area_holding, area_shortage, time_next_event, mean_interdemand, num_months

    inv_level = initial_inv_level

    time_next_event[1] = 1.0 * 10**30
    time_next_event[2] = sim_time + expon(mean_interdemand)
    time_next_event[3] = num_months
    time_next_event[4] = 0.0


def timing():
    global sim_time, next_event_type, num_events

    main_time_next_event = 1.0 * 10**29
    next_event_type = 0
    for i in range(num_events):
        if (time_next_event[i+1] < main_time_next_event):
            main_time_next_event = time_next_event[i+1]
            next_event_type = i+1

    if (next_event_type == 0):
        output_file.write(
            "\nEvent list is empty at time {0}".format(sim_time))
        exit(1)

    sim_time = main_time_next_event


def order_arrival():

    global inv_level, amount, time_next_event

    inv_level += amount
    time_next_event[1] = 1.0 * 10**30


def demand():
    global inv_level, random_integer, time_next_event, prob_distrib_demand, sim_time, mean_interdemand

    inv_level -= random_integer(prob_distrib_demand)
    time_next_event[2] = sim_time + expon(mean_interdemand)


def evaluate():

    global inv_level, smalls, amount, bigs, total_ordering_cost, setup_cost, minlag, maxlag, time_next_event, sim_time

    if (inv_level < smalls):

        amount = bigs - inv_level
        total_ordering_cost += setup_cost + uniform(minlag, maxlag)

    time_next_event[4] = sim_time + 1.0


def update_time_avg_stats():

    global sim_time, time_last_event, inv_level, area_shortage, area_holding, time_since_last_event

    time_since_last_event = sim_time - time_last_event
    time_last_event = sim_time

    if (inv_level < 0):
        area_shortage - + inv_level * time_since_last_event
    elif (inv_level > 0):
        area_holding += inv_level * time_since_last_event


def report():

    global total_ordering_cost, num_months, holding_cost, area_holding, shortage_cost, area_shortage, smalls, bigs

    avg_holding_cost = avg_ordering_cost = avg_shortage_cost = 0.0

    avg_ordering_cost = total_ordering_cost / num_months
    avg_holding_cost = holding_cost * area_holding / num_months
    avg_shortage_cost = shortage_cost * area_shortage / num_months

    output_file.write("\npolicy ({0},{1}) \n\n".format(smalls, bigs))
    output_file.write("total_ordering_cost  {0}\n\n".format(
        avg_ordering_cost + avg_holding_cost + avg_shortage_cost))
    output_file.write("avg_ordering_cost  {0}\n\n".format(
        avg_ordering_cost))
    output_file.write("avg_holding_cost  {0}\n\n".format(
        avg_holding_cost))
    output_file.write("avg_shortage_cost  {0}\n\n".format(
        avg_shortage_cost))


def expon(mean):
    rand = random.uniform(0.0001, 1.0)
    return -(float(mean)) * math.log(rand)


def random_integer(prob_distrib):

    i = 1
    u = 0.0

    u = random.uniform(0.00001, 1.0)

    for i in range(u >= prob_distrib[i]):
        return i


def uniform(a, b):
    rand1 = random.uniform(0.0001, 1.0)
    return (a + math.log(rand1) * (b-a))


if __name__ == '__main__':

    i = num_policies = 0
    input_file = open("infile.txt", "r")
    output_file = open("outfile.txt", "w")

    num_events = 4

    input_parameters = input_file.readline().split()

    mean_interarrival = input_parameters[0]
    mean_service = input_parameters[1]
    num_delays_required = input_parameters[2]

    output_file.write("Single-server queueing system\n\n")
    output_file.write(
        "Mean interarrival time {0} \n\n".format(mean_interarrival))
    output_file.write("Mean service time {0} \n\n".format(mean_service))
    output_file.write("No of Cutomers {0} \n".format(num_delays_required))

    for i in range(num_policies):
        # inputs

        initialization()

        while (num_custs_delayed < int(num_delays_required)):

            timing()
            update_time_avg_stats()

            if (next_event_type == 1):
                arrive()
            elif (next_event_type == 2):
                depart()

        report()

    input_file.close()
    output_file.close()
