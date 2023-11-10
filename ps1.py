###########################
# 6.00.2x Problem Set 1: Space Cows 

from ps1_partition import get_partitions, partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')
    
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


# Problem 1
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    cows_copy = cows.copy()
    cow_transport = []

    # Continue until all cows have been transported
    while cows_copy:
        trip = []
        total_weight = 0

        # Sort cows based on their weight in descending order
        sorted_cows = sorted(cows_copy.items(), key=lambda x: x[1], reverse=True)

        # Try to fit cows into the current trip
        for name, weight in sorted_cows:
            if total_weight + weight <= limit:
                trip.append(name)
                total_weight += weight
                # Remove the cow from remaining cows
                del cows_copy[name]

        # Add the current trip to the transport list
        cow_transport.append(trip)

    return cow_transport


def brute_force_cow_transport(cows, limit=10):
    # Generate all possible partitions of cows
    possible_partitions = get_partitions(list(cows.keys()))
    # Initialize the list to store the solution of minimum trips
    optimal_partition = None

    # Go through each partition and check if it satisfies the weight limit
    for partition in possible_partitions:
        valid_partition = True
        for trip in partition:
            trip_weight = sum(cows[name] for name in trip)
            if trip_weight > limit:
                valid_partition = False
                break  # This partition is not valid, move to the next

        # If the partition is valid and either we have no optimal solution yet,
        # or this partition uses fewer trips than the current optimal solution,
        # update the optimal solution
        if valid_partition and (optimal_partition is None or len(partition) < len(optimal_partition)):
            optimal_partition = partition

    return optimal_partition
        
# Problem 3
def compare_cow_transport_algorithms(cows):

    # Measure the time taken and calculate the solution using the greedy algorithm
    start = time.time()
    greedy_solution = greedy_cow_transport(cows)
    end = time.time()
    greedy_time = end - start

    # Measure the time taken and calculate the solution using the brute force algorithm
    start = time.time()
    brute_force_solution = brute_force_cow_transport(cows)
    end = time.time()
    brute_force_time = end - start

    # Print the results
    print(f"Greedy Algorithm: {len(greedy_solution)} trips, time taken: {greedy_time} seconds")
    print(f"Brute Force Algorithm: {len(brute_force_solution)} trips, time taken: {brute_force_time} seconds")


"""
Here is some test data for you to see the results of your algorithms with. 
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
"""

cows = load_cows("ps1_cow_data.txt")
limit=100
print(cows)

print(greedy_cow_transport(cows, limit))
print(brute_force_cow_transport(cows, limit))
print(compare_cow_transport_algorithms(cows))

