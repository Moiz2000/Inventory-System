import math
import random

amount = bigs = initial_inv_level = inv_level = next_event_type = num_events = num_months = num_values_demand = smalls = 0

area_holding = area_shortage = holding_cost = incremental_cost = maxlag = mean_interdemand = minlag = setup_cost = shortage_cost = sim_time = time_last_event = time_since_last_event = total_ordering_cost = 0.0

prob_distrib_demand = [0] * 26
time_next_event = [0] * 5

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
        if (float(time_next_event[i+1]) < main_time_next_event):
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
    global inv_level, time_next_event, prob_distrib_demand, sim_time, mean_interdemand

    inv_level -= random_integer()
    time_next_event[2] = sim_time + expon(mean_interdemand)


def evaluate():

    global inv_level, smalls, amount, bigs, total_ordering_cost, setup_cost, minlag, maxlag, time_next_event, sim_time, incremental_cost

    if (inv_level < smalls):
        amount = bigs - inv_level
        total_ordering_cost += (setup_cost + (incremental_cost * amount))
        time_next_event[1] = sim_time + uniform(minlag, maxlag)

    time_next_event[4] = sim_time + 1.0


def update_time_avg_stats():

    global sim_time, time_last_event, inv_level, area_shortage, area_holding, time_since_last_event

    time_since_last_event = sim_time - time_last_event
    time_last_event = sim_time

    if (inv_level < 0):
        area_shortage -= inv_level * time_since_last_event
    elif (inv_level > 0):
        area_holding += inv_level * time_since_last_event


def report():

    global total_ordering_cost, num_months, holding_cost, area_holding, shortage_cost, area_shortage, smalls, bigs

    avg_holding_cost = avg_ordering_cost = avg_shortage_cost = 0.0

    avg_ordering_cost = total_ordering_cost / num_months
    avg_holding_cost = holding_cost * area_holding / num_months
    avg_shortage_cost = shortage_cost * area_shortage / num_months

    output_file.write("\npolicy ({0},{1})     {2}            {3}           {4}         {5} \n\n".format(
        smalls, bigs, avg_ordering_cost + avg_holding_cost + avg_shortage_cost, avg_ordering_cost, avg_holding_cost, avg_shortage_cost))


def expon(mean):
    rand = random.uniform(0.001, 1.0)
    return -(float(mean)) * math.log(rand)


def random_integer():

    u = random.uniform(0.001, 1.0)

    if (u <= 1/6):
        return 1
    elif(u > 1/6 and u <= 1/2):
        return 2
    elif (u > 1/2 and u <= 5/6):
        return 3
    else:
        return 4


def uniform(a, b):
    rand1 = random.uniform(0.001, 1.0)
    return (float(a) + ((float(b)-float(a)) * rand1))


if __name__ == '__main__':

    i = num_policies = 0
    input_file = open("infile.txt", "r")
    output_file = open("outfile.txt", "w")

    input_parameters = input_file.readline().split()

    initial_inv_lvl = int(input_parameters[0])
    num_months = int(input_parameters[1])
    num_policies = int(input_parameters[2])
    num_values_demand = int(input_parameters[3])
    mean_interdemand = float(input_parameters[4])
    setup_cost = float(input_parameters[5])
    incremental_cost = float(input_parameters[6])
    holding_cost = float(input_parameters[7])
    shortage_cost = float(input_parameters[8])
    minlag = float(input_parameters[9])
    maxlag = float(input_parameters[10])

    prob_distrib_demand[0] = float(input_parameters[11])
    prob_distrib_demand[1] = float(input_parameters[12])
    prob_distrib_demand[2] = float(input_parameters[13])
    prob_distrib_demand[3] = float(input_parameters[14])

    output_file.write("Single-product inventory system\n\n")
    output_file.write(
        " initial inventory lvl {0} items\n\n".format(initial_inv_level))
    output_file.write(
        "Number of demand sizes {0} \n\n".format(num_values_demand))
    output_file.write("Distribution function of demand sizes ")
    for i in range(num_values_demand):
        output_file.write("{0}  ".format(prob_distrib_demand[i]))

    output_file.write(
        "\nMean interdemand time {0} \n\n".format(mean_interdemand))
    output_file.write(
        "Delivery lag range {0} to {1} months\n\n".format(minlag, maxlag))
    output_file.write(
        "Length of the simulation {0} months\n\n".format(num_months))
    output_file.write(
        "K = {0}   i = {1}   h = {2}   pi = {3} \n\n".format(setup_cost, incremental_cost, holding_cost, shortage_cost))
    output_file.write(
        "Number of policies {0} \n\n".format(num_policies))
    output_file.write(
        "                      Average                       Average")
    output_file.write("                        Average             Average\n")
    output_file.write(
        " Policy             total cost                     ordering cost")
    output_file.write("                  holding cost         shortage cost")

    for i in range(num_policies):

        smalls = int(input())
        bigs = int(input())
        initialization()

        while (next_event_type != 3):

            timing()
            update_time_avg_stats()

            if (next_event_type == 1):
                order_arrival()
            elif (next_event_type == 2):
                demand()
            elif (next_event_type == 4):
                evaluate()
            elif (next_event_type == 3):
                report()

    input_file.close()
    output_file.close()
