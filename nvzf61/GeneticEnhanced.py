############
############ ALTHOUGH I GIVE YOU THE 'BARE BONES' OF THIS PROGRAM WITH THE NAME
############ 'skeleton.py', YOU CAN RENAME IT TO ANYTHING YOU LIKE. HOWEVER, FOR
############ THE PURPOSES OF THE EXPLANATION IN THESE COMMENTS, I ASSUME THAT
############ THIS PROGRAM IS STILL CALLED 'skeleton.py'.
############
############ IF YOU WISH TO IMPORT STANDARD MODULES, YOU CAN ADD THEM AFTER THOSE BELOW.
############ NOTE THAT YOU ARE NOT ALLOWED TO IMPORT ANY NON-STANDARD MODULES!
############

import os
import sys
import time
import random

############
############ NOW PLEASE SCROLL DOWN UNTIL THE NEXT BLOCK OF CAPITALIZED COMMENTS.
############
############ DO NOT TOUCH OR ALTER THE CODE IN BETWEEN! YOU HAVE BEEN WARNED!
############

def read_file_into_string(input_file, ord_range):
    the_file = open(input_file, 'r')
    current_char = the_file.read(1)
    file_string = ""
    length = len(ord_range)
    while current_char != "":
        i = 0
        while i < length:
            if ord(current_char) >= ord_range[i][0] and ord(current_char) <= ord_range[i][1]:
                file_string = file_string + current_char
                i = length
            else:
                i = i + 1
        current_char = the_file.read(1)
    the_file.close()
    return file_string

def remove_all_spaces(the_string):
    length = len(the_string)
    new_string = ""
    for i in range(length):
        if the_string[i] != " ":
            new_string = new_string + the_string[i]
    return new_string

def integerize(the_string):
    length = len(the_string)
    stripped_string = "0"
    for i in range(0, length):
        if ord(the_string[i]) >= 48 and ord(the_string[i]) <= 57:
            stripped_string = stripped_string + the_string[i]
    resulting_int = int(stripped_string)
    return resulting_int

def convert_to_list_of_int(the_string):
    list_of_integers = []
    location = 0
    finished = False
    while finished == False:
        found_comma = the_string.find(',', location)
        if found_comma == -1:
            finished = True
        else:
            list_of_integers.append(integerize(the_string[location:found_comma]))
            location = found_comma + 1
            if the_string[location:location + 5] == "NOTE=":
                finished = True
    return list_of_integers

def build_distance_matrix(num_cities, distances, city_format):
    dist_matrix = []
    i = 0
    if city_format == "full":
        for j in range(num_cities):
            row = []
            for k in range(0, num_cities):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    elif city_format == "upper_tri":
        for j in range(0, num_cities):
            row = []
            for k in range(j):
                row.append(0)
            for k in range(num_cities - j):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    else:
        for j in range(0, num_cities):
            row = []
            for k in range(j + 1):
                row.append(0)
            for k in range(0, num_cities - (j + 1)):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    if city_format == "upper_tri" or city_format == "strict_upper_tri":
        for i in range(0, num_cities):
            for j in range(0, num_cities):
                if i > j:
                    dist_matrix[i][j] = dist_matrix[j][i]
    return dist_matrix

def read_in_algorithm_codes_and_tariffs(alg_codes_file):
    flag = "good"
    code_dictionary = {}
    tariff_dictionary = {}
    if not os.path.exists(alg_codes_file):
        flag = "not_exist"
        return code_dictionary, tariff_dictionary, flag
    ord_range = [[32, 126]]
    file_string = read_file_into_string(alg_codes_file, ord_range)
    location = 0
    EOF = False
    list_of_items = []
    while EOF == False:
        found_comma = file_string.find(",", location)
        if found_comma == -1:
            EOF = True
            sandwich = file_string[location:]
        else:
            sandwich = file_string[location:found_comma]
            location = found_comma + 1
        list_of_items.append(sandwich)
    third_length = int(len(list_of_items)/3)
    for i in range(third_length):
        code_dictionary[list_of_items[3 * i]] = list_of_items[3 * i + 1]
        tariff_dictionary[list_of_items[3 * i]] = int(list_of_items[3 * i + 2])
    return code_dictionary, tariff_dictionary, flag

############
############ THE RESERVED VARIABLE 'input_file' IS THE CITY FILE UNDER CONSIDERATION.
############
############ IT CAN BE SUPPLIED BY SETTING THE VARIABLE BELOW OR VIA A COMMAND-LINE
############ EXECUTION OF THE FORM 'python skeleton.py city_file.txt'. WHEN SUPPLYING
############ THE CITY FILE VIA A COMMAND-LINE EXECUTION, ANY ASSIGNMENT OF THE VARIABLE
############ 'input_file' IN THE LINE BELOW iS SUPPRESSED.
############
############ IT IS ASSUMED THAT THIS PROGRAM 'skeleton.py' SITS IN A FOLDER THE NAME OF
############ WHICH IS YOUR USER-NAME, E.G., 'abcd12', WHICH IN TURN SITS IN ANOTHER
############ FOLDER. IN THIS OTHER FOLDER IS THE FOLDER 'city-files' AND NO MATTER HOW
############ THE NAME OF THE CITY FILE IS SUPPLIED TO THIS PROGRAM, IT IS ASSUMED THAT 
############ THE CITY FILE IS IN THE FOLDER 'city-files'.
############

input_file = "AISearchfile017.txt"

############
############ PLEASE SCROLL DOWN UNTIL THE NEXT BLOCK OF CAPITALIZED COMMENTS.
############
############ DO NOT TOUCH OR ALTER THE CODE IN BETWEEN! YOU HAVE BEEN WARNED!
############

if len(sys.argv) > 1:
    input_file = sys.argv[1]

the_particular_city_file_folder = "city-files"

if os.path.isfile("../" + the_particular_city_file_folder + "/" + input_file):
    ord_range = [[32, 126]]
    file_string = read_file_into_string("../" + the_particular_city_file_folder + "/" + input_file, ord_range)
    file_string = remove_all_spaces(file_string)
    print("I have found and read the input file " + input_file + ":")
else:
    print("*** error: The city file " + input_file + " does not exist in the folder '" + the_particular_city_file_folder + "'.")
    sys.exit()

location = file_string.find("SIZE=")
if location == -1:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()

comma = file_string.find(",", location)
if comma == -1:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()

num_cities_as_string = file_string[location + 5:comma]
num_cities = integerize(num_cities_as_string)
print("   the number of cities is stored in 'num_cities' and is " + str(num_cities))

comma = comma + 1
stripped_file_string = file_string[comma:]
distances = convert_to_list_of_int(stripped_file_string)

counted_distances = len(distances)
if counted_distances == num_cities * num_cities:
    city_format = "full"
elif counted_distances == (num_cities * (num_cities + 1))/2:
    city_format = "upper_tri"
elif counted_distances == (num_cities * (num_cities - 1))/2:
    city_format = "strict_upper_tri"
else:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()

dist_matrix = build_distance_matrix(num_cities, distances, city_format)
print("   the distance matrix 'dist_matrix' has been built.")

############
############ YOU NOW HAVE THE NUMBER OF CITIES STORED IN THE INTEGER VARIABLE 'num_cities'
############ AND THE TWO_DIMENSIONAL MATRIX 'dist_matrix' HOLDS THE INTEGER CITY-TO-CITY 
############ DISTANCES SO THAT 'dist_matrix[i][j]' IS THE DISTANCE FROM CITY 'i' TO CITY 'j'.
############ BOTH 'num_cities' AND 'dist_matrix' ARE RESERVED VARIABLES AND SHOULD FEED
############ INTO YOUR IMPLEMENTATIONS.
############

############
############ THERE NOW FOLLOWS CODE THAT READS THE ALGORITHM CODES AND TARIFFS FROM
############ THE TEXT-FILE 'alg_codes_and_tariffs.txt' INTO THE RESERVED DICTIONARIES
############ 'code_dictionary' AND 'tariff_dictionary'. DO NOT AMEND THIS CODE!
############ THE TEXT FILE 'alg_codes_and_tariffs.txt' SHOULD BE IN THE SAME FOLDER AS
############ THE FOLDER 'city-files' AND THE FOLDER WHOSE NAME IS YOUR USER-NAME, E.G., 'abcd12'.
############

code_dictionary, tariff_dictionary, flag = read_in_algorithm_codes_and_tariffs("../alg_codes_and_tariffs.txt")

if flag != "good":
    print("*** error: The text file 'alg_codes_and_tariffs.txt' does not exist.")
    sys.exit()

print("The codes and tariffs have been read from 'alg_codes_and_tariffs.txt':")

############
############ YOU NOW NEED TO SUPPLY SOME PARAMETERS.
############
############ THE RESERVED STRING VARIABLE 'my_user_name' SHOULD BE SET AT YOUR USER-NAME, E.G., "abcd12"
############

my_user_name = "nvzf61"

############
############ YOU CAN SUPPLY, IF YOU WANT, YOUR FULL NAME. THIS IS NOT USED AT ALL BUT SERVES AS
############ AN EXTRA CHECK THAT THIS FILE BELONGS TO YOU. IF YOU DO NOT WANT TO SUPPLY YOUR
############ NAME THEN EITHER SET THE STRING VARIABLES 'my_first_name' AND 'my_last_name' AT 
############ SOMETHING LIKE "Mickey" AND "Mouse" OR AS THE EMPTY STRING (AS THEY ARE NOW;
############ BUT PLEASE ENSURE THAT THE RESERVED VARIABLES 'my_first_name' AND 'my_last_name'
############ ARE SET AT SOMETHING).
############

my_first_name = "Thomas"
my_last_name = "Milton"

############
############ YOU NEED TO SUPPLY THE ALGORITHM CODE IN THE RESERVED STRING VARIABLE 'algorithm_code'
############ FOR THE ALGORITHM YOU ARE IMPLEMENTING. IT NEEDS TO BE A LEGAL CODE FROM THE TEXT-FILE
############ 'alg_codes_and_tariffs.txt' (READ THIS FILE TO SEE THE CODES).
############

algorithm_code = "GA"

############
############ DO NOT TOUCH OR ALTER THE CODE BELOW! YOU HAVE BEEN WARNED!
############

if not algorithm_code in code_dictionary:
    print("*** error: the agorithm code " + algorithm_code + " is illegal")
    sys.exit()
print("   your algorithm code is legal and is " + algorithm_code + " -" + code_dictionary[algorithm_code] + ".")

############
############ YOU CAN ADD A NOTE THAT WILL BE ADDED AT THE END OF THE RESULTING TOUR FILE IF YOU LIKE,
############ E.G., "in my basic greedy search, I broke ties by always visiting the first 
############ city found" BY USING THE RESERVED STRING VARIABLE 'added_note' OR LEAVE IT EMPTY
############ IF YOU WISH. THIS HAS NO EFFECT ON MARKS BUT HELPS YOU TO REMEMBER THINGS ABOUT
############ YOUR TOUR THAT YOU MIGHT BE INTERESTED IN LATER.
############

added_note = ""

############
############ NOW YOUR CODE SHOULD BEGIN.
############

#######################################################################################################################

# cd \Users\Tom\Documents\GitHub\AI-Search-Coursework\nvzf61
# python GeneticEnhanced.py AISearchfile535.txt

# Imports temporary libraries
from matplotlib import pyplot as plt
import keyboard

# Initialize variables
population_size = 100  # Must be even
mutation_chance = 0.1
elitism_percentage = 0.1
population = []
t0 = time.time()

# Initialises temporary variables for graph plotting
progress = []
best = []

# for i in range(population_size):
#     """Generate initial random population"""
#
#     # Initializes random tour
#     tour_i = random.sample(range(num_cities), num_cities)
#     tour_length_i = 0
#
#     # Calculates tour length
#     for i in range(num_cities):
#         if i == num_cities - 1:  # Adds distance from last city to first
#             tour_length_i += dist_matrix[tour_i[0]][tour_i[-1]]
#         else:  # Otherwise adds distance from current city to next
#             tour_length_i += dist_matrix[tour_i[i]][tour_i[i + 1]]
#
#     # Add to population
#     population.append((tour_i, tour_length_i))

for i in range(population_size):
    """Generate nearest neighbour population"""

    # Initialise tour with random start city
    tour_i = [random.randrange(num_cities)]
    tour_length_i = 0

    # Generates remaining cities in tour
    while True:

        # If the last city in tour, calculate its length
        if len(tour_i) == num_cities:
            # Adds distance from last city to first to complete tour
            tour_length_i += dist_matrix[tour_i[0]][tour_i[-1]]
            # Adds tour to population
            population.append((tour_i, tour_length_i))
            break

        # Extracts row of dist_matrix for current end city of tour
        dist_array = dist_matrix[tour_i[-1]].copy()

        # Makes already visited city distances infinity so they arent chosen as minimum
        for j in range(num_cities):
            if j in tour_i:
                dist_array[j] = float('inf')

        # Chooses city with minimum distance
        minimum = min(dist_array)
        # Adds it to current tour
        tour_i.append(dist_array.index(minimum))
        # Adds distance to tour length
        tour_length_i += minimum

# while time.time()-t0 < 59:

# Alternative termination method
while keyboard.is_pressed('q') is False:

    # Sorts the population by tour length
    population = sorted(population, key=lambda x: x[1])

    # Stores best tour so far
    tour, tour_length = population[0]

    # Elitism: Stores the best tours from population
    minimums = population[:int(elitism_percentage * population_size)]

    # Weighting for each tour is 1 over the length of the tour so shorter tours are more likely to be selected
    weightings = [1 / i[1] for i in population]

    # Initialise new population
    new_population = []

    # Calculates average tour length and best tour length for the generation
    average = 0
    for i in range(population_size):
        average += population[i][1]

    # Stores average and best
    progress.append(average / population_size)
    best.append(tour_length)

    # Temporary method to show algorithm performance whilst its running
    if keyboard.is_pressed('p'):
        print(len(progress), "generations with best tour length:", tour_length)
        t1 = time.time() - t0
        print("Time elapsed: ", t1)

        # Plots graph of progress
        plt.plot(progress)
        plt.plot(best)
        plt.title('AlgAenhanced')
        plt.show()

    for i in range(int(population_size/2)):
        """Generate new population"""

        # Choose parents based on fitness weighting
        x, y = random.choices(population, weights=weightings, k=2)
        x, y = x[0], y[0]

        """Single split as in notes"""
        # # Choose a random point to split the parent tours
        # split = random.randint(0, num_cities)
        #
        # # Combine the two parents to produce two offspring
        # z1 = x[:split]
        # z2 = y[:split]
        # z1_missing = [i for i in y if i not in z1]
        # z2_missing = [i for i in x if i not in z2]
        # z1 = z1 + z1_missing
        # z2 = z2 + z2_missing

        """PMX"""
        # # Chooses two random points to split the parent tours
        # random_ints = random.choices(range(num_cities), k=2)
        # split1 = min(random_ints)
        # split2 = max(random_ints)
        #
        # # Combine the two parents to produce two offspring
        # z1, z1_2 = x[:split1], x[split2:]
        # z2, z2_2 = y[:split1], y[split2:]
        # z1_missing = [i for i in y if i not in z1 and i not in z1_2]
        # z2_missing = [i for i in x if i not in z2 and i not in z2_2]
        # z1 = z1 + z1_missing + z1_2
        # z2 = z2 + z2_missing + z2_2

        """OX"""
        # Chooses two random points to split the parent tours
        random_ints = random.choices(range(num_cities), k=2)
        split1 = min(random_ints)
        split2 = max(random_ints)

        # Combine the two parents to produce two offspring
        z1 = x[split1:split2]
        z2 = y[split1:split2]
        z1_missing = [i for i in y if i not in z1]
        z2_missing = [i for i in x if i not in z2]
        z1 = z1_missing[:split1] + z1 + z1_missing[split1:]
        z2 = z2_missing[:split1] + z2 + z2_missing[split1:]

        """CX"""
        # # Initialise offspring with "x"s
        # z1 = ["x" for i in range(num_cities)]
        # z2 = ["x" for i in range(num_cities)]
        #
        # # Compute first cycle
        # i = 0
        # while z1[i] == "x":
        #     z1[i] = x[i]
        #     z2[i] = y[i]
        #     i = x.index(y[i])
        #
        # # Add remaining cities from other parent
        # for i in range(num_cities):
        #     if z1[i] == "x":
        #         z1[i] = y[i]
        #     if z2[i] == "x":
        #         z2[i] = x[i]

        for z in [z1, z2]:
            # Swap two random cities if a mutation occurs
            if random.random() < mutation_chance:
                a, b = random.choices(range(num_cities), k=2)
                z[a], z[b] = z[b], z[a]

            # Calculate tour length for children
            z_tour_length = 0
            for i in range(num_cities):
                if i == num_cities - 1:  # Adds distance from last city to first
                    z_tour_length += dist_matrix[z[0]][z[-1]]
                else:  # Otherwise adds distance from current city to next
                    z_tour_length += dist_matrix[z[i]][z[i + 1]]

            # Add child to population
            new_population.append((z, z_tour_length))

    # Elitism: Adds best tours from previous generation
    new_population = new_population[:-int(population_size*elitism_percentage)] + minimums
    # Code now acts on new population
    population = new_population

# Prints results of algorithm
print(len(progress), "generations with best tour length:", tour_length)
t1 = time.time() - t0
print("Time elapsed: ", t1)

# Plots results of algorithm
plt.plot(progress)
plt.plot(best)
plt.title('AlgAenhanced')
plt.show()

#######################################################################################################################

############
############ YOUR CODE SHOULD NOW BE COMPLETE AND WHEN EXECUTION OF THIS PROGRAM 'skeleton.py'
############ REACHES THIS POINT, YOU SHOULD HAVE COMPUTED A TOUR IN THE RESERVED LIST VARIABLE 'tour',
############ WHICH HOLDS A LIST OF THE INTEGERS FROM {0, 1, ..., 'num_cities' - 1}, AND YOU SHOULD ALSO
############ HOLD THE LENGTH OF THIS TOUR IN THE RESERVED INTEGER VARIABLE 'tour_length'.
############

############
############ YOUR TOUR WILL BE PACKAGED IN A TOUR FILE OF THE APPROPRIATE FORMAT AND THIS TOUR FILE,
############ WHOSE NAME WILL BE A MIX OF THE NAME OF THE CITY FILE, THE NAME OF THIS PROGRAM AND THE
############ CURRENT DATA AND TIME. SO, EVERY SUCCESSFUL EXECUTION GIVES A TOUR FILE WITH A UNIQUE
############ NAME AND YOU CAN RENAME THE ONES YOU WANT TO KEEP LATER.
############

############
############ DO NOT TOUCH OR ALTER THE CODE BELOW THIS POINT! YOU HAVE BEEN WARNED!
############

flag = "good"
length = len(tour)
for i in range(0, length):
    if isinstance(tour[i], int) == False:
        flag = "bad"
    else:
        tour[i] = int(tour[i])
if flag == "bad":
    print("*** error: Your tour contains non-integer values.")
    sys.exit()
if isinstance(tour_length, int) == False:
    print("*** error: The tour-length is a non-integer value.")
    sys.exit()
tour_length = int(tour_length)
if len(tour) != num_cities:
    print("*** error: The tour does not consist of " + str(num_cities) + " cities as there are, in fact, " + str(len(tour)) + ".")
    sys.exit()
flag = "good"
for i in range(0, num_cities):
    if not i in tour:
        flag = "bad"
if flag == "bad":
    print("*** error: Your tour has illegal or repeated city names.")
    sys.exit()
check_tour_length = 0
for i in range(0, num_cities - 1):
    check_tour_length = check_tour_length + dist_matrix[tour[i]][tour[i + 1]]
check_tour_length = check_tour_length + dist_matrix[tour[num_cities - 1]][tour[0]]
if tour_length != check_tour_length:
    flag = print("*** error: The length of your tour is not " + str(tour_length) + "; it is actually " + str(check_tour_length) + ".")
    sys.exit()
print("You, user " + my_user_name + ", have successfully built a tour of length " + str(tour_length) + "!")

local_time = time.asctime(time.localtime(time.time()))
output_file_time = local_time[4:7] + local_time[8:10] + local_time[11:13] + local_time[14:16] + local_time[17:19]
output_file_time = output_file_time.replace(" ", "0")
script_name = os.path.basename(sys.argv[0])
if len(sys.argv) > 2:
    output_file_time = sys.argv[2]
output_file_name = script_name[0:len(script_name) - 3] + "_" + input_file[0:len(input_file) - 4] + "_" + output_file_time + ".txt"

f = open(output_file_name,'w')
f.write("USER = " + my_user_name + " (" + my_first_name + " " + my_last_name + "),\n")
f.write("ALGORITHM CODE = " + algorithm_code + ", NAME OF CITY-FILE = " + input_file + ",\n")
f.write("SIZE = " + str(num_cities) + ", TOUR LENGTH = " + str(tour_length) + ",\n")
f.write(str(tour[0]))
for i in range(1,num_cities):
    f.write("," + str(tour[i]))
f.write(",\nNOTE = " + added_note)
f.close()
print("I have successfully written your tour to the tour file:\n   " + output_file_name + ".")

