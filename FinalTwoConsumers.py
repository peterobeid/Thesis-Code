print("\n")

# Interpreting Results:

# Each row_types of the matrix of consumer types gives (in order): Consumer 1's valuation for item 1 from A, Consumer 1's valuation for item 2 from A, 
# Consumer 1's valuation for item 1 from B, Consumer 1's valuation for item 2 from B, then all correspodning for Consumer 2 also
# Matrix rows are defined by: values_A_1[0], values_A_1[1], values_B_1[0], values_B_1[1], values_A_2[0], values_A_2[1], values_B_2[0], values_B_2[1]])

# Each row_types of the matrix of answers gives (in order): Optimal payoff, optimal p1, optimal p2, optimal s, quantity of item 1 sold, quantity of item 2 sold

# Imports
from random import seed
from random import choice
from re import S
import numpy as np 
from docplex.mp.model import Model


# Which values of x and y are we going to allow?
sequence_x = [0, 1/2, 1]
sequence_y = [-1, 0, 1]

# Set a pre-determined value of a, which is the ratio factor of the relative importance 
# of external value to the consumer relative to the intrinsic value of the product 
multiplier = 0.1
# Prices set by competitor - Just for now set [0.5, 0.5, 0] with assumption of no bundle discount offered by comptetitor
prices_b = np.array([1/2, 1/2, 0])

count = 0
option1 = 0
option2 = 0
option3 = 0
option4 = 0 
option5 = 0
option6 = 0
option7 = 0
option8 = 0
option9 = 0
option10 = 0


# Initialize the matrix that will store each combination of consumer types
mat_types = np.array([-7, -7, -7, -7, -7, -7, -7, -7])

# Initialize the matrix that will store the optimal answers to the optimisation problem
mat_answers = np.array([-7, -7, -7, -7, -7, -7])


## MAIN

# Create a loop for all possible consumer type combinations
for a in range(len(sequence_x)):
    for b in range(len(sequence_x)):
        for c in range(len(sequence_y)):
            for d in range(len(sequence_y)):
                for e in range(len(sequence_x)):
                    for f in range(len(sequence_x)):
                        for g in range(len(sequence_y)):
                            for h in range(len(sequence_y)):
                                # Generate the values for Consumer 1
                                x1 = [sequence_x[a], sequence_x[b]]
                                x1 = np.array(x1)

                                y1 = [sequence_y[c], sequence_y[d]]
                                y1 = np.array(y1)

                                values_A_1 = x1 + multiplier*y1
                                values_B_1 = x1 - multiplier*y1


                                # Generate the values for Consumer 2
                                x2 = [sequence_x[e], sequence_x[f]]
                                x2 = np.array(x2)

                                y2 = [sequence_y[g], sequence_y[h]]
                                y2 = np.array(y2)

                                values_A_2 = x2 + multiplier*y2
                                values_B_2 = x2 - multiplier*y2


                                # Insert these values into the matrix storing combinations of consumer types
                                row_types = np.array([values_A_1[0], values_A_1[1], values_B_1[0], values_B_1[1], values_A_2[0], values_A_2[1], values_B_2[0], values_B_2[1]])
                                mat_types = np.vstack([mat_types,row_types])


                                ############### START OPTIMISATION ##################

                                # Let's look at all the possible options - Producer A can "target" consumers in the market in the following ways

                                
                                # Set up the variable for maximum payoff
                                optimal_payoff = 0
                                optimal_p1 = 0
                                optimal_p2 = 0
                                optimal_s = 0 
                                sales_item_1 = 0
                                sales_item_2 = 0
                                
                                ############## OPTION 1 - Producer A targets both consumers for both products ##############
                                # Optimisation Model
                                m = Model(name = 'Price Optimisation')

                                # Variables
                                p1 = m.continuous_var(name = 'Good 1 Price')
                                p2 = m.continuous_var(name = 'Good 2 Price')
                                s = m.continuous_var(name = 'Bundle Discount')

                                # Constraints C1 -> Setting prices such that C1 will choose to buy both items from A
                                no_items_1 = m.add_constraint(values_A_1[0]+values_A_1[1] - (p1+p2-s) >= 0)
                                item1B_1 = m.add_constraint(values_A_1[0]+values_A_1[1] - (p1+p2-s) >= values_B_1[0] - prices_b[0])
                                item2B_1 = m.add_constraint(values_A_1[0]+values_A_1[1] - (p1+p2-s) >= values_B_1[1] - prices_b[1])
                                item1A_1 = m.add_constraint(values_A_1[0]+values_A_1[1] - (p1+p2-s) >= values_A_1[0] - p1)
                                item2A_1 = m.add_constraint(values_A_1[0]+values_A_1[1] - (p1+p2-s) >= values_A_1[1] - p2)
                                item1A_item2B_1 = m.add_constraint(values_A_1[0]+values_A_1[1] - (p1+p2-s) >= values_A_1[0]+values_B_1[1] - (p1+prices_b[1]))
                                item1B_item2A_1 = m.add_constraint(values_A_1[0]+values_A_1[1] - (p1+p2-s) >= values_A_1[1]+values_B_1[0] - (p2+prices_b[0]))
                                both_itemsB_1 = m.add_constraint(values_A_1[0]+values_A_1[1] - (p1+p2-s) >= values_B_1[0]+values_B_1[1] - (prices_b[0]+prices_b[1]))

                                # Constraints C2 -> Setting prices such that C2 will choose to buy both items from A
                                no_items_2 = m.add_constraint(values_A_2[0]+values_A_2[1] - (p1+p2-s) >= 0)
                                item1B_2 = m.add_constraint(values_A_2[0]+values_A_2[1] - (p1+p2-s) >= values_B_2[0] - prices_b[0])
                                item2B_2 = m.add_constraint(values_A_2[0]+values_A_2[1] - (p1+p2-s) >= values_B_2[1] - prices_b[1])
                                item1A_2 = m.add_constraint(values_A_2[0]+values_A_2[1] - (p1+p2-s) >= values_A_2[0] - p1)
                                item2A_2 = m.add_constraint(values_A_2[0]+values_A_2[1] - (p1+p2-s) >= values_A_2[1] - p2)
                                item1A_item2B_2 = m.add_constraint(values_A_2[0]+values_A_2[1] - (p1+p2-s) >= values_A_2[0]+values_B_2[1] - (p1+prices_b[1]))
                                item1B_item2A_2 = m.add_constraint(values_A_2[0]+values_A_2[1] - (p1+p2-s) >= values_A_2[1]+values_B_2[0] - (p2+prices_b[0]))
                                both_itemsB_2 = m.add_constraint(values_A_2[0]+values_A_2[1] - (p1+p2-s) >= values_B_2[0]+values_B_2[1] - (prices_b[0]+prices_b[1]))

                                # Constraint that bundle discount must be >= 0
                                bundle_contraint = m.add_constraint(s >= 0)

                                # Objective
                                m.maximize(2*(p1+p2-s))

                                sol = m.solve()

                                objective = sol.get_objective_value()
                                prices = sol.get_value_list([p1, p2, s])
                                
                                if objective >= optimal_payoff:
                                    optimal_payoff = objective
                                    optimal_p1 = prices[0]
                                    optimal_p2 = prices[1]
                                    optimal_s = prices[2]
                                    sales_item_1 = 2
                                    sales_item_2 = 2
                                    option1 = option1 + 1

                                
                                # Work out which consumer values which items from A the highest --> This will be needed for the rest of the optimisation options ###
                                # e.g. higherItem1_1A means the player with the higher valuation of item 1 (from producer A), their value of buying item 1 from producer A
                                # e.g. higherItem2_1B means the player with the higher valuation of item 2 (from producer A), their valuation of buying item 1 from producer B
                                # etc.

                                # Player 1 values item 1 from producer A higher than player 2
                                if values_A_1[0] >= values_A_2[0]:
                                    higherItem1_1A = values_A_1[0]
                                    lowerItem1_1A = values_A_2[0]
                                    higherItem1_1B = values_B_1[0]
                                    lowerItem1_1B = values_B_2[0]

                                    higherItem1_2A = values_A_1[1]
                                    lowerItem1_2A = values_A_2[1]
                                    higherItem1_2B = values_B_1[1]
                                    lowerItem1_2B = values_B_2[1]

                                # Player 1 values item 2 from producer A higher than player 2
                                if values_A_1[1] >= values_A_2[1]:
                                    higherItem2_2A = values_A_1[1]
                                    lowerItem2_2A = values_A_2[1]
                                    higherItem2_2B = values_B_1[1]
                                    lowerItem2_2B = values_B_2[1]

                                    higherItem2_1A = values_A_1[0]
                                    lowerItem2_1A = values_A_2[0]
                                    higherItem2_1B = values_B_1[0]
                                    lowerItem2_1B = values_B_2[0]

                                # Player 2 values item 1 from producer A higher than player 1
                                if values_A_1[0] < values_A_2[0]:
                                    lowerItem1_1A = values_A_1[0]
                                    higherItem1_1A = values_A_2[0]
                                    lowerItem1_1B = values_B_1[0]
                                    higherItem1_1B = values_B_2[0]

                                    higherItem1_2A = values_A_2[1]
                                    lowerItem1_2A = values_A_1[1]
                                    higherItem1_2B = values_B_2[1]
                                    lowerItem1_2B = values_B_1[1]

                                # Player 2 values item 2 from producer A higher than player 1
                                if values_A_1[1] < values_A_2[1]:
                                    lowerItem2_2A = values_A_1[1]
                                    higherItem2_2A = values_A_2[1]
                                    lowerItem2_2B = values_B_1[1]
                                    higherItem2_2B = values_B_2[1]

                                    higherItem2_1A = values_A_2[0]
                                    lowerItem2_1A = values_A_1[0]
                                    higherItem2_1B = values_B_2[0]
                                    lowerItem2_1B = values_B_1[0]
                                

                                ########### OPTION 2 - Producer A targets both consumers for item 1, but only higher consumer for item 2 ######

                                # Is this option even feasible?
                                if higherItem1_1A < 0 or lowerItem1_1A < 0 or higherItem2_2A < 0:
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

                                    # Constraints --> Setting prices so that the person who values item 2 higher buys both items  
                                    higherItem2_optout = m.add_constraint(higherItem2_1A + higherItem2_2A - (p1 + p2 - s) >= 0)
                                    higherItem2_alternate_mix_1 = m.add_constraint(higherItem2_1A + higherItem2_2A - (p1 + p2 - s) >= higherItem2_1A + higherItem2_2B - (p1 + prices_b[1]))
                                    higherItem2_alternate_mix_2 = m.add_constraint(higherItem2_1A + higherItem2_2A - (p1 + p2 - s) >= higherItem2_1B + higherItem2_2A - (prices_b[0] + p2))
                                    higherItem2_alternate_item1FromB = m.add_constraint(higherItem2_1A + higherItem2_2A - (p1 + p2 - s) >= higherItem2_1B - prices_b[0])
                                    higherItem2_alternate_item2FromB = m.add_constraint(higherItem2_1A + higherItem2_2A - (p1 + p2 - s) >= higherItem2_2B - prices_b[1])
                                    higherItem2_alternate_item1FromA = m.add_constraint(higherItem2_1A + higherItem2_2A - (p1 + p2 - s) >= higherItem2_1A - p1)
                                    higherItem2_alternate_item2FromA = m.add_constraint(higherItem2_1A + higherItem2_2A - (p1 + p2 - s) >= higherItem2_2A - p2)
                                    higherItem2_alternate_bothFromB = m.add_constraint(higherItem2_1A + higherItem2_2A - (p1 + p2 - s) >= higherItem2_1B + higherItem2_2B - (prices_b[0] + prices_b[1]))
                                    
                                    # Constraints -> Setting prices so that the person who values item 1 is also targeted 
                                    higherItem1_optout = m.add_constraint(higherItem1_1A - p1 >= 0)
                                    higherItem1_alterate = m.add_constraint(higherItem1_1A - p1 >= higherItem1_1B - prices_b[0])

                                    # Constraint that bundle discount must be >= 0
                                    bundle_contraint = m.add_constraint(s >= 0)

                                    # Objective
                                    m.maximize(2*p1 + p2 -s)

                                    sol = m.solve()
                                    objective = sol.get_objective_value()
                                    prices = sol.get_value_list([p1, p2, s])
                                
                                if objective > optimal_payoff:
                                    optimal_payoff = objective
                                    optimal_p1 = prices[0]
                                    optimal_p2 = prices[1]
                                    optimal_s = prices[2]
                                    sales_item_1 = 2
                                    sales_item_2 = 1
                                    option2 = option2 + 1
                            

                                ########### OPTION 3 - Producer A targets both consumers for item 2, but only higher consumer for item 1 ######
                                

                                # Is this option even feasible?
                                if higherItem2_2A < 0 or lowerItem2_2A < 0 or higherItem1_1A < 0:
                                    p1 = -1
                                    p2 = -1
                                    s = -1
                                    prices = [-1, -1, -1]
                                    objective = -1

                                
                                else:
                                    m = Model(name = 'Price Optimisation')

                                    # Variables
                                    p1 = m.continuous_var(name = 'Good 1 Price')
                                    p2 = m.continuous_var(name = 'Good 2 Price')
                                    s = m.continuous_var(name = 'Bundle Discount') 

                                    # Constraints --> Setting prices so that the person who values item 1 higher buys both items  
                                    higherItem1_optout = m.add_constraint(higherItem1_1A + higherItem1_2A - (p1 + p2 - s) >= 0)
                                    higherItem1_alternate_mix_1 = m.add_constraint(higherItem1_1A + higherItem1_2A - (p1 + p2 - s) >= higherItem1_1A + higherItem1_2B - (p1 + prices_b[1]))
                                    higherItem1_alternate_mix_2 = m.add_constraint(higherItem1_1A + higherItem1_2A - (p1 + p2 - s) >= higherItem1_1B + higherItem1_2A - (prices_b[0] + p2))
                                    higherItem1_alternate_item1FromB = m.add_constraint(higherItem1_1A + higherItem1_2A - (p1 + p2 - s) >= higherItem1_1B - prices_b[0])
                                    higherItem1_alternate_item2FromB = m.add_constraint(higherItem1_1A + higherItem1_2A - (p1 + p2 - s) >= higherItem1_2B - prices_b[1])
                                    higherItem1_alternate_item1FromA = m.add_constraint(higherItem1_1A + higherItem1_2A - (p1 + p2 - s) >= higherItem1_1A - p1)
                                    higherItem1_alternate_item2FromA = m.add_constraint(higherItem1_1A + higherItem1_2A - (p1 + p2 - s) >= higherItem1_2A - p2)
                                    higherItem1_alternate_bothFromB = m.add_constraint(higherItem1_1A + higherItem1_2A - (p1 + p2 - s) >= higherItem1_1B + higherItem1_2B - (prices_b[0] + prices_b[1]))
                                    
                                    # Constraints -> Setting prices so that the person who values item 2 is also targeted 
                                    higherItem1_optout = m.add_constraint(higherItem2_2A - p2 >= 0)
                                    higherItem1_alterate = m.add_constraint(higherItem2_2A - p2 >= higherItem2_2B - prices_b[1])

                                    # Constraint that bundle discount must be >= 0
                                    bundle_contraint = m.add_constraint(s >= 0)

                                    # Objective
                                    m.maximize(p1 + 2*p2 -s)

                                    sol = m.solve()
                                    objective = sol.get_objective_value()
                                    prices = sol.get_value_list([p1, p2, s])
                                

                                if objective > optimal_payoff:
                                    optimal_payoff = objective
                                    optimal_p1 = prices[0]
                                    optimal_p2 = prices[1]
                                    optimal_s = prices[2]
                                    sales_item_1 = 1
                                    sales_item_2 = 2
                                    option2 = option2 + 1


                                ########### OPTION 4 - Producer A targets both consumers for item 1 only ######

                                # Is this option even feasible?
                                if higherItem1_1A < 0 or lowerItem1_1A < 0:
                                    p1 = -1
                                    prices = [-1]
                                    objective = -1

                                
                                else:
                                    m = Model(name = 'Price Optimisation')

                                    # Variables
                                    p1 = m.continuous_var(name = 'Good 1 Price')

                                    # Constraints --> Setting prices so that we capture both items for item 1
                                    higher_optout = m.add_constraint(higherItem1_1A - p1 >= 0)
                                    higher_alterntive = m.add_constraint(higherItem1_1A - p1 >= higherItem1_1B - prices_b[0])
                                    lower_optout = m.add_constraint(lowerItem1_1A - p1 >= 0)
                                    lower_alterntive = m.add_constraint(lowerItem1_1A - p1 >= lowerItem1_1B - prices_b[0])

                                    # Objective
                                    m.maximize(2*p1)

                                    sol = m.solve()
                                    objective = sol.get_objective_value()
                                    prices = sol.get_value_list([p1])
                                

                                if objective > optimal_payoff:
                                    optimal_payoff = objective
                                    optimal_p1 = prices[0]
                                    optimal_p2 = -1
                                    optimal_s = -1
                                    sales_item_1 = 2
                                    sales_item_2 = 0
                                    option4 = option4 + 1


                                ########### OPTION 5 - Producer A targets both consumers for item 2 only ######

                                # Is this option even feasible?
                                if higherItem2_2A < 0 or lowerItem2_2A < 0:
                                    p2 = -1
                                    prices = [-1]
                                    objective = -1
                                
                                
                                else:
                                    m = Model(name = 'Price Optimisation')

                                    # Variables
                                    p2 = m.continuous_var(name = 'Good 2 Price')
                                    
                                    # Constraints --> Setting prices so that we capture both items for item 1
                                    higher_optout = m.add_constraint(higherItem2_2A - p2 >= 0)
                                    higher_alterntive = m.add_constraint(higherItem2_2A - p2 >= higherItem2_2B - prices_b[1])
                                    lower_optout = m.add_constraint(lowerItem2_2A - p2 >= 0)
                                    lower_alterntive = m.add_constraint(lowerItem2_2A - p2 >= lowerItem2_2B - prices_b[1])

                                    # Objective
                                    m.maximize(2*p2)

                                    sol = m.solve()
                                    objective = sol.get_objective_value()
                                    prices = sol.get_value_list([p2])
                                

                                if objective > optimal_payoff:
                                    optimal_payoff = objective
                                    optimal_p1 = -1
                                    optimal_p2 = prices[0]
                                    optimal_s = -1
                                    sales_item_1 = 0
                                    sales_item_2 = 2
                                    option5 = option5 + 1


                                ############## OPTION 6 - Producer A targets only the consumer that values each of its products the highest ##############

                                # Is this case even feasible?
                                if higherItem1_1A <= 0 or higherItem2_2A <= 0:
                                    p1 = -1
                                    p2 = -1
                                    prices = [-1, -1]
                                    objective = -1

                                else:
                                    # Optimisation Model
                                    m = Model(name = 'Price Optimisation')

                                    # Variables
                                    p1 = m.continuous_var(name = 'Good 1 Price')
                                    p2 = m.continuous_var(name = 'Good 2 Price')

                                    # Constraints item 1 --> Setting prices so that the player with the higher value for item 1 is targeted by producer A
                                    higher_optout_1 = m.add_constraint(higherItem1_1A - p1 >= 0)
                                    higher_alternate_1 = m.add_constraint(higherItem1_1A - p1 >= higherItem1_1B - prices_b[0])

                                    # Constraints C2 -> Setting prices so that the player with the higher value for item 2 is targeted by producer A
                                    higher_optout_2 = m.add_constraint(higherItem2_2A - p2 >= 0)
                                    higher_alternate_2 = m.add_constraint(higherItem2_2A - p2 >= higherItem2_2B - prices_b[1])

                                    # Objective
                                    m.maximize(p1+p2)

                                    sol = m.solve()
                                    objective = sol.get_objective_value()
                                    prices = sol.get_value_list([p1, p2])
                                
                                if objective > optimal_payoff:
                                    optimal_payoff = objective
                                    optimal_p1 = prices[0]
                                    optimal_p2 = prices[1]
                                    optimal_s = -1
                                    sales_item_1 = 1
                                    sales_item_2 = 1
                                    option6 = option6 + 1
                            

                                ############## OPTION 7 - Producer A targets only the consumer that values item 1 the highest, for both items ##############

                                # Is this option even feasible?
                                if higherItem1_1A < 0 or higherItem1_2A <0:
                                    p1 = -1
                                    p2 = -1
                                    s = -1
                                    prices = [-1, -1, -1]
                                    objective = -1
                                    

                                else:
                                    m = Model(name = 'Price Optimisation')

                                    # Variables
                                    p1 = m.continuous_var(name = 'Good 1 Price')
                                    p2 = m.continuous_var(name = 'Good 2 Price')
                                    s = m.continuous_var(name = 'Bundle Discount') 

                                    # Constraints --> Setting prices so that the person who values item 1 higher buys both items  
                                    higherItem1_optout = m.add_constraint(higherItem1_1A + higherItem1_2A - (p1 + p2 - s) >= 0)
                                    higherItem1_alternate_mix_1 = m.add_constraint(higherItem1_1A + higherItem1_2A - (p1 + p2 - s) >= higherItem1_1A + higherItem1_2B - (p1 + prices_b[1]))
                                    higherItem1_alternate_mix_2 = m.add_constraint(higherItem1_1A + higherItem1_2A - (p1 + p2 - s) >= higherItem1_1B + higherItem1_2A - (prices_b[0] + p2))
                                    higherItem1_alternate_item1FromB = m.add_constraint(higherItem1_1A + higherItem1_2A - (p1 + p2 - s) >= higherItem1_1B - prices_b[0])
                                    higherItem1_alternate_item2FromB = m.add_constraint(higherItem1_1A + higherItem1_2A - (p1 + p2 - s) >= higherItem1_2B - prices_b[1])
                                    higherItem1_alternate_item1FromA = m.add_constraint(higherItem1_1A + higherItem1_2A - (p1 + p2 - s) >= higherItem1_1A - p1)
                                    higherItem1_alternate_item2FromA = m.add_constraint(higherItem1_1A + higherItem1_2A - (p1 + p2 - s) >= higherItem1_2A - p2)
                                    higherItem1_alternate_bothFromB = m.add_constraint(higherItem1_1A + higherItem1_2A - (p1 + p2 - s) >= higherItem1_1B + higherItem1_2B - (prices_b[0] + prices_b[1]))

                                    # Constraint that bundle discount must be >= 0
                                    bundle_contraint = m.add_constraint(s >= 0)

                                    # Objective
                                    m.maximize(p1 + p2 -s)

                                    sol = m.solve()
                                    objective = sol.get_objective_value()
                                    prices = sol.get_value_list([p1, p2, s])
                                

                                if objective > optimal_payoff:
                                    optimal_payoff = objective
                                    optimal_p1 = prices[0]
                                    optimal_p2 = prices[1]
                                    optimal_s = prices[2]
                                    sales_item_1 = 1
                                    sales_item_2 = 1
                                    option7 = option7 + 1


                                ############## OPTION 8 - Producer A targets only the consumer that values item 2 the highest, for both items ##############

                                # Is this option even feasible?
                                if higherItem2_2A < 0 or higherItem2_1A < 0:
                                    p1 = -1
                                    p2 = -1
                                    s = -1
                                    prices = [-1, -1, -1]
                                    objective = -1

                                
                                else:

                                    m = Model(name = 'Price Optimisation')

                                    # Variables
                                    p1 = m.continuous_var(name = 'Good 1 Price')
                                    p2 = m.continuous_var(name = 'Good 2 Price')
                                    s = m.continuous_var(name = 'Bundle Discount') 

                                    # Constraints --> Setting prices so that the person who values item 2 higher buys both items  
                                    higherItem2_optout = m.add_constraint(higherItem2_1A + higherItem2_2A - (p1 + p2 - s) >= 0)
                                    higherItem2_alternate_mix_1 = m.add_constraint(higherItem2_1A + higherItem2_2A - (p1 + p2 - s) >= higherItem2_1A + higherItem2_2B - (p1 + prices_b[1]))
                                    higherItem2_alternate_mix_2 = m.add_constraint(higherItem2_1A + higherItem2_2A - (p1 + p2 - s) >= higherItem2_1B + higherItem2_2A - (prices_b[0] + p2))
                                    higherItem2_alternate_item1FromB = m.add_constraint(higherItem2_1A + higherItem2_2A - (p1 + p2 - s) >= higherItem2_1B - prices_b[0])
                                    higherItem2_alternate_item2FromB = m.add_constraint(higherItem2_1A + higherItem2_2A - (p1 + p2 - s) >= higherItem2_2B - prices_b[1])
                                    higherItem2_alternate_item1FromA = m.add_constraint(higherItem2_1A + higherItem2_2A - (p1 + p2 - s) >= higherItem2_1A - p1)
                                    higherItem2_alternate_item2FromA = m.add_constraint(higherItem2_1A + higherItem2_2A - (p1 + p2 - s) >= higherItem2_2A - p2)
                                    higherItem2_alternate_bothFromB = m.add_constraint(higherItem2_1A + higherItem2_2A - (p1 + p2 - s) >= higherItem2_1B + higherItem2_2B - (prices_b[0] + prices_b[1]))

                                    # Constraint that bundle discount must be >= 0
                                    bundle_contraint = m.add_constraint(s >= 0)

                                    # Objective
                                    m.maximize(p1 + p2 -s)

                                    sol = m.solve()
                                    objective = sol.get_objective_value()
                                    prices = sol.get_value_list([p1, p2, s])
                                
                                if objective > optimal_payoff:
                                    optimal_payoff = objective
                                    optimal_p1 = prices[0]
                                    optimal_p2 = prices[1]
                                    optimal_s = prices[2]
                                    sales_item_1 = 1
                                    sales_item_2 = 1
                                    option8 = option8 + 1
                            

                                ############## OPTION 9 - Producer A targets only the consumer that values item 1 the highest, for item 1 ##############
                                
                                if higherItem1_1A <= 0:
                                    p1 = -1
                                    prices = [-1]
                                    objective = -1

                                else:
                                    # Optimisation Model
                                    m = Model(name = 'Price Optimisation')

                                    # Variables
                                    p1 = m.continuous_var(name = 'Good 1 Price')

                                    # Constraints item 1 --> Setting prices so that the player with the higher value for item 1 is targeted by producer A
                                    higher_optout_1 = m.add_constraint(higherItem1_1A - p1 >= 0)
                                    higher_alternate_1 = m.add_constraint(higherItem1_1A - p1 >= higherItem1_1B - prices_b[0])


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
                                    option9 = option9 + 1
                                

                                ############## OPTION 10 - Producer A targets only the consumer that values item 2 the highest, for item 2 ##############
                              
                                if higherItem2_2A <= 0:
                                    p2 = -1
                                    prices = [-1]
                                    objective = -1

                                else:
                                    # Optimisation Model
                                    m = Model(name = 'Price Optimisation')

                                    # Variables
                                    p2 = m.continuous_var(name = 'Good 2 Price')
                                    
                                    # Constraints item 1 --> Setting prices so that the player with the higher value for item 2 is targeted by producer A
                                    higher_optout_2 = m.add_constraint(higherItem2_2A - p2 >= 0)
                                    higher_alternate_2 = m.add_constraint(higherItem2_2A - p2 >= higherItem2_2B - prices_b[1])

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
                                    option10 = option10 + 1


                                count = count + 1
                                optimal_payoff = round(optimal_payoff,2)
                                optimal_p1 = round(optimal_p1,2)
                                optimal_p2 = round(optimal_p2,2)
                                optimal_s = round(optimal_s,2)

                                # Add solutions of the optimisation into a matrix
                                # This can be interpreted as optimal payoff, optimal p1, p2, s, quant good 1 sold, quant good 2 sold
                                row_answers = np.array([optimal_payoff, optimal_p1, optimal_p2, optimal_s, sales_item_1, sales_item_2])
                                mat_answers = np.vstack([mat_answers, row_answers])

                                print("Comlpeted", count, "of 6561 combinations of consumer type")

                                # If using 2 elements for x and y, recommend count > ~245.
                                # If using 3 elements for x and y, recommend count > ~6550
                                if count > 6550:
                                    print("\n")
                                    print(mat_types[count])
                                    print(optimal_payoff, optimal_p1, optimal_p2, optimal_s, sales_item_1, sales_item_2)

                                
                    
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
print("Option 4 has been activated = %d times" %option4)
print("Option 5 has been activated = %d times" %option5)
print("Option 6 has been activated = %d times" %option6)
print("Option 7 has been activated = %d times" %option7)
print("Option 8 has been activated = %d times" %option8)
print("Option 9 has been activated = %d times" %option9)
print("Option 10 has been activated = %d times" %option10)

np.savetxt("DoubleConsumer1.csv", mat_types, delimiter = ",")
np.savetxt("DoubleConsumer2.csv", mat_answers, delimiter = ",")