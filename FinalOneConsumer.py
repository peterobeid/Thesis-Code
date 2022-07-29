print("\n")

# Imports
from ftplib import parse227
from random import seed
from random import choice
import numpy as np 
from docplex.mp.model import Model


## MAIN

# Which values of x and y are we going to allow?
sequence_x = [0, 1]
sequence_y = [-1, 1]
# Set a pre-determined value of a, which is the ratio factor of the relative importance 
# of external value to the consumer relative to the intrinsic value of the product 
multiplier = 0.1
# Prices set by competitor - Just for now set [0.5, 0.5, 0] with assumption of no bundle discount offered by comptetitor
prices_b = np.array([1/2, 1/2, 0])

count = 0
option1 = 0
option2 = 0
option3 = 0

# Initialize the matrix that will store each combination of consumer types
mat_types = np.array([-7, -7, -7, -7])

# Initialize the matrix that will store the optimal answers to the optimisation problem
mat_answers = np.array([-7, -7, -7, -7, -7, -7])


for a in range(len(sequence_x)):
    for b in range(len(sequence_x)):
        for c in range(len(sequence_y)):
            for d in range(len(sequence_y)):
            
                # Generate the values for Consumer 1
                x = [sequence_x[a], sequence_x[b]]
                x = np.array(x)

                y = [sequence_y[c], sequence_y[d]]
                y = np.array(y)
                
                values_A = x + multiplier*y
                values_B = x - multiplier*y

                # Insert these values into the matrix storing combinations of consumer types
                # This can be interpreted as Consumer's valuation for item 1 from A, item 2 from A, item 1 from B, item 2 from B
                row_types = np.array([values_A[0], values_A[1], values_B[0], values_B[1]])
                mat_types = np.vstack([mat_types,row_types])

                
                # Set up the variables for maximum payoff
                # A price of -1 indicates that the firm is not participating in the market for that product
                # Of course, this corresponds to a payoff of 0 and 0 sales of each item
                # These variables will remain unchanged if Producer A opts out of participating in both markets
                optimal_payoff = 0
                optimal_p1 = -1
                optimal_p2 = -1
                optimal_s = -1 
                sales_item_1 = 0
                sales_item_2 = 0

                ############## OPTION 1 - Consumer buys both from A ##############

                # Is this even viable?
                if values_A[0] < 0 and values_A[1] < 0:
                    p1 = -1
                    p2 = -1
                    s = -1
                    prices = [-1, -1, -1]
                    objective = -1

                else:    
                    # Optimisation Model
                    m = Model(name = 'Price Optimisation')

                    # Variables
                    p1 = m.continuous_var(name = 'Good 1 Price')
                    p2 = m.continuous_var(name = 'Good 2 Price')
                    s = m.continuous_var(name = 'Bundle Discount')

                    # Constraints
                    no_items = m.add_constraint(values_A[0]+values_A[1] - (p1+p2-s) >= 0)
                    item1B = m.add_constraint(values_A[0]+values_A[1] - (p1+p2-s) >= values_B[0] - prices_b[0])
                    item2B = m.add_constraint(values_A[0]+values_A[1] - (p1+p2-s) >= values_B[1] - prices_b[1])
                    item1A = m.add_constraint(values_A[0]+values_A[1] - (p1+p2-s) >= values_A[0] - p1)
                    item2A = m.add_constraint(values_A[0]+values_A[1] - (p1+p2-s) >= values_A[1] - p2)
                    item1A_item2B = m.add_constraint(values_A[0]+values_A[1] - (p1+p2-s) >= values_A[0]+values_B[1] - (p1+prices_b[1]))
                    item1B_item2A = m.add_constraint(values_A[0]+values_A[1] - (p1+p2-s) >= values_A[1]+values_B[0] - (p2+prices_b[0]))
                    both_itemsB = m.add_constraint(values_A[0]+values_A[1] - (p1+p2-s) >= values_B[0]+values_B[1] - (prices_b[0]+prices_b[1]))

                    bundle_contraint = m.add_constraint(s >= 0)

                    # Objective
                    m.maximize(p1+p2-s)

                    sol = m.solve()
                                
                    objective = sol.get_objective_value()
                    
                    prices = sol.get_value_list([p1, p2, s])
                
                if objective >= optimal_payoff:
                    optimal_payoff = objective
                    optimal_p1 = prices[0]
                    optimal_p2 = prices[1]
                    optimal_s = prices[2]
                    sales_item_1 = 1
                    sales_item_2 = 1
                    option1 = option1 + 1
        

                ############# OPTION 2 - Consumer buys item 1 from A ##############

                # Is this even viable?
                if values_A[0] < 0:
                    p1 = -1
                    prices = [-1]
                    objective = -1

                else:
                      # Optimisation Model
                    m = Model(name = 'Price Optimisation')

                    # Variables
                    p1 = m.continuous_var(name = 'Good 1 Price')

                    # Constraints
                    no_items = m.add_constraint(values_A[0] - p1 >= 0)
                    item1B = m.add_constraint(values_A[0] - p1 >= values_B[0] - prices_b[0])

                    # Objective
                    m.maximize(p1)

                    sol = m.solve()
                                
                    objective = sol.get_objective_value()
                    
                    prices = sol.get_value_list([p1])
                
                if objective > optimal_payoff:
                    optimal_payoff = objective
                    optimal_p1 = prices[0]
                    optimal_p2 = -1
                    optimal_s = -1
                    sales_item_1 = 1
                    sales_item_2 = 0
                    option2 = option2 + 1


                ############# OPTION 3 - Consumer buys item 2 from A ##############

                # Is this even viable?
                if values_A[1] < 0:
                    p2 = -1
                    prices = [-1]
                    objective = -1

                else:
                    # Optimisation Model
                    m = Model(name = 'Price Optimisation')

                    # Variables
                    p2 = m.continuous_var(name = 'Good 2 Price')

                    # Constraints
                    no_items = m.add_constraint(values_A[1] - p2 >= 0)
                    item2B = m.add_constraint(values_A[1] - p2 >= values_B[1] - prices_b[1])

                    # Objective
                    m.maximize(p2)

                    sol = m.solve()
                                
                    objective = sol.get_objective_value()
                    
                    prices = sol.get_value_list([p2])
                
                if objective > optimal_payoff:
                    optimal_payoff = objective
                    optimal_p1 = -1
                    optimal_p2 = prices[0]
                    optimal_s = -1
                    sales_item_1 = 0
                    sales_item_2 = 1
                    option3 = option3 + 1


                count = count + 1
                optimal_payoff = round(optimal_payoff,2)
                optimal_p1 = round(optimal_p1,2)
                optimal_p2 = round(optimal_p2,2)
                optimal_s = round(optimal_s,2)

                # Add solutions of the optimisation into a matrix
                # This can be interpreted as optimal payoff, optimal p1, p2, s, quant good 1 sold, quant good 2 sold
                row_answers = np.array([optimal_payoff, optimal_p1, optimal_p2, optimal_s, sales_item_1, sales_item_2])
                mat_answers = np.vstack([mat_answers, row_answers])

print(count)

mat_types = np.delete(mat_types, 0, 0)
mat_answers = np.delete(mat_answers, 0, 0)
print(mat_types)
print("\n")
print(mat_answers)

#Confirm matrix size
rows_types = len(mat_types)
columns_types = len(mat_types[0])
print("Rows types = %d" %rows_types)
print("Columns types = %d" %columns_types)

rows_answers = len(mat_answers)
columns_answers = len(mat_answers[0])
print("Rows answers = %d" %rows_answers)
print("Columns answers = %d" %columns_answers)

print("\n")
print("Option 1 has been activated = %d times" %option1)
print("Option 2 has been activated = %d times" %option2)
print("Option 3 has been activated = %d times" %option3)

print((type(mat_types)))
print((type(mat_answers)))

np.savetxt("SingleConsumer1.csv", mat_types, delimiter = ",")
np.savetxt("SingleConsumer2.csv", mat_answers, delimiter = ",")





                   