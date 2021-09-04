# Import Statements -

from statistics import mean
from random import randint
import numpy as np


# Setup -

print("")
simulations = input("Change the number of simulations? ('yes'/'no') Type 'no' if unsure what to do. -> ")
if simulations == "yes":
    simulations = int(input("\nWhat do you want the new simulation number to be? \n50000 is default. \n500000 is a high amount (takes a long time). \n5000 or less may result in inaccuracies. \nSimulation Number -> "))
else:
    simulations = 50000

print("")
total_left = int(input("How many items left in the pipe? -> "))
desired_left = int(input("How many desired items (i.e. spotlights) left in the pipe? -> "))
total_rubies_spent = 0


# Function Definitions -

def give_advice(simulations):
    """
    The function that calls the others and actually tells you if you should do a ten pull
    @return: None
    """
    averages = get_averages(simulations)
    ten_pulls = np.argmin(averages)
    rubies = np.min(averages)
    print("\nIf you follow the given advice from here on out, you can expect to spend " + str(round(rubies, 1)) + " more rubies ON AVERAGE")
    print("Projections say " + str(ten_pulls) + " more ten pulls before singles. \nThis could change if you pull some desired items before then.")
    if ten_pulls > 0:
        print("\nYou should do a ten pull ---- > 10 <")
    else:
        print("\nYou should do one pulls ---- > 1 <")

def get_averages(simulations):
    """
    Run pull simulations for all possible number of ten pulls, and put the averages in an array
    @return: The list of average rubies spent
    """
    averages = []
    max_tens = total_left // 10
    for ten_pulls in range(max_tens + 1):
        averages.append(simulate_pulls(ten_pulls, simulations))
        # Print to ensure the user that the program is still running
        print(str(round((ten_pulls + 1) * 100 / (max_tens + 1))) + "% completed...")
    return averages

def simulate_pulls(ten_pulls, simulations=10000):
    """
    Simulate pipe pulls and find the average rubies spent for ten_pulls number of ten pulls, then one pulls
    @return: The average number of rubies spent
    """
    # Create the list of rubies spent
    rubies_spent = []
    # Simulation loop
    for sim in range(simulations):
        # Find the minimum location of the pulls
        locations = []
        for i in range(desired_left):
            rand_loc = randint(0, total_left)
            while rand_loc in locations:
                rand_loc = randint(0, total_left)
            locations.append(rand_loc)
        location = min(locations)
        # Calculate the rubies spent and add it to the list
        rubies_spent.append(ruby_calculation(location, ten_pulls))
    # Return the average of the rubies_spent list
    return mean(rubies_spent)

def ruby_calculation(location, ten_pulls):
    """
    Calculates the number of rubies spent to get an item at position location with a max of ten_pulls ten pulls
    @return: The number of rubies spent with thie given ruby strategy
    """
    rubies = 0
    position = total_left
    while position >= location and ten_pulls > 0:
        ten_pulls -= 1
        position -= 10
        rubies += 45
    while position >= location:
        position -= 1
        rubies += 5
    return rubies


# Main Loop -

#sim_number ensures that things don't take too long during single pulls
sim_number = simulations
while desired_left > 0:
    print("\nComputing --")
    if (sim_number >= 200000):
        print("Due to the high simulation number, this may take awhile.")

    # Failsafe:
    if total_left < desired_left:
        print("Failsafe encountered - total items left cannot be less than desired items left")
        print("Program ended to prevent infinite loop\n\n")
        break

    give_advice(sim_number)
    print("")
    total_change = int(input("Did you do a ten pull (type '10') or a one pull (type '1')? -> "))
    desired_change = int(input("How many of your desired items did you gain? -> "))
    total_left -= total_change
    if total_change == 1:
        total_rubies_spent += 5
        sim_number = simulations // 5
    elif total_change == 10:
        total_rubies_spent += 45
        sim_number = simulations
    desired_left -= desired_change
    print("")

    print("Current stats -- ")
    print("Total items left: " + str(total_left))
    print("Desired items left: " + str(desired_left))
    print("So far you have spent " + str(total_rubies_spent) + " rubies.")
    if desired_left <= 0:
        print("\nThank you! Come again!\n\n")

