# This code determines the expected payoff of a particular pricing strategy for a given distribution of consumer types
# Specifically, it will be used to determine the payoff using a default pricing strategy of [0.5, 0.5, 0], in order to
# contrast this payoff with the payoff used under a non-linear pricing strategy

print("\n")

from random import seed
from random import choice
import numpy as np 
from docplex.mp.model import Model

# What is the pricing strategy we are considering?
strategy = [0.7, 0.3, 0]

# Which values of x and y are we going to allow?

## Item 1's Distribution
sequence_x_1 = [0, 0.5, 1]
sequence_y_1 = [-1, 0, 1]

prob_x_1 =  [1/3, 1/3, 1/3]
prob_y_1 = [0.1, 0.3, 0.6]

## Item 2's Distribution
sequence_x_2 = [0, 0.5, 1]
sequence_y_2 = [-1, 0, 1]

prob_x_2 =  [1/3, 1/3, 1/3]
prob_y_2 = [0.6, 0.3, 0.1]

# Set a pre-determined value of a, which is the ratio factor of the relative importance 
# of external value to the consumer relative to the intrinsic value of the product 
multiplier = 0.1
# Prices set by competitor - Just for now assume no bundle discount offered by comptetitor
prices_b = [0.7, 0.3, 0]
# Costs of production:
costs_a = np.array([0, 0])


expected_value = 0 

# Create a loop for all possible consumer type combinations
for a in range(len(sequence_x_1)):
    for b in range(len(sequence_x_1)):
        for c in range(len(sequence_y_1)):
            for d in range(len(sequence_y_1)):
                for e in range(len(sequence_x_2)):
                    for f in range(len(sequence_x_2)):
                        for g in range(len(sequence_y_2)):
                            for h in range(len(sequence_y_2)):
                                # Generate the values for Consumer 1
                                x1 = [sequence_x_1[a], sequence_x_1[b]]
                                x1 = np.array(x1)

                                y1 = [sequence_y_1[c], sequence_y_1[d]]
                                y1 = np.array(y1)

                                values_A_1 = x1 + multiplier*y1
                                values_B_1 = x1 - multiplier*y1

                                # Generate the values for Consumer 2
                                x2 = [sequence_x_2[e], sequence_x_2[f]]
                                x2 = np.array(x2)

                                y2 = [sequence_y_2[g], sequence_y_2[h]]
                                y2 = np.array(y2)

                                values_A_2 = x2 + multiplier*y2
                                values_B_2 = x2 - multiplier*y2

                                # What is the Probability of this combination of consumer types occuring?
                                prob = prob_x_1[a]*prob_x_1[b]*prob_y_1[c]*prob_y_1[d]*prob_x_2[e]*prob_x_2[f]*prob_y_2[g]*prob_y_2[h]

                                # For this combination of consumer types, what consumption pattern will we see?
                                # Each consumer has the following options:
                                # - Buy neither product
                                # - Buy both items from A in bundle
                                # - Buy item 1 from A
                                # - Buy item 1 from A and item 2 from B
                                # - Buy item 2 from A
                                # - Buy item 2 from A and item 1 from B
                                # - Buy item 1 from B
                                # - Buy item 2 from B
                                # - Buy both items from B

                                ## Start by looking at the actions for the first consumer
                                # Note, in the following, utility refers to the customer's payoff, and revenue refers to the firm's payoff

                                # Start with the default of consumer exiting both markets
                                best_consumer_utility_1 = 0
                                revenue_1 = 0

                                # Scenarios where something is purchased from A:
                                both_A = values_A_1[0] + values_A_1[1] - (strategy[0] + strategy[1] - strategy[2])
                                both_A = round(both_A, 3)
                                if both_A >= best_consumer_utility_1:
                                    if best_consumer_utility_1 == both_A:
                                        revenue_1 = max(revenue_1, strategy[0] + strategy[1] - strategy[2])
                                    else:
                                        best_consumer_utility_1 = both_A
                                        revenue_1 = strategy[0] + strategy[1] - strategy[2]

                                item1A = values_A_1[0] - strategy[0]
                                item1A = round(item1A, 3)
                                if item1A >= best_consumer_utility_1:
                                    if item1A == best_consumer_utility_1:
                                        revenue_1 = max(revenue_1, strategy[0])
                                    else:
                                        best_consumer_utility_1 = item1A
                                        revenue_1 = strategy[0]

                                item1A_item2B = values_A_1[0] + values_B_1[1] - (strategy[0] + prices_b[1])
                                item1A_item2B = round(item1A_item2B, 3)
                                if item1A_item2B >= best_consumer_utility_1:
                                    if item1A_item2B == best_consumer_utility_1:
                                        revenue_1 = max(revenue_1, strategy[0])
                                    else:
                                        best_consumer_utility_1 = item1A_item2B
                                        revenue_1 = strategy[0]

                                item2A = values_A_1[1] - strategy[1]
                                item2A = round(item2A, 3)
                                if item2A >= best_consumer_utility_1:
                                    if item2A == best_consumer_utility_1:
                                        revenue_1 = max(revenue_1, strategy[1])
                                    else:
                                        best_consumer_utility_1 = item2A
                                        revenue_1 = strategy[1]

                                item2A_item1B = values_A_1[1] + values_B_1[0] - (strategy[1] + prices_b[0])
                                item2A_item1B = round(item2A_item1B, 3)
                                if item2A_item1B >= best_consumer_utility_1:
                                    if item2A_item1B == best_consumer_utility_1:
                                        revenue_1 = max(revenue_1, strategy[1])
                                    else:
                                        best_consumer_utility_1 = item2A_item1B
                                        revenue_1 = strategy[1]

                                item1B = values_B_1[0] - prices_b[0]
                                item1B = round(item1B, 3)
                                if item1B >= best_consumer_utility_1:
                                    if item1B == best_consumer_utility_1:
                                        revenue_1 = max(revenue_1, 0)
                                    else:
                                        best_consumer_utility_1 = item1B
                                        revenue_1 = 0

                                item2B = values_B_1[1] - prices_b[1]
                                item2B = round(item2B, 3)
                                if item2B >= best_consumer_utility_1:
                                    if item2B == best_consumer_utility_1:
                                        revenue_1 = max(revenue_1, 0)
                                    else:
                                        best_consumer_utility_1 = item2B
                                        revenue_1 = 0

                                item1B_item2B = values_B_1[0] + values_B_1[1] - (prices_b[0] + prices_b[1])
                                item1B_item2B = round(item1B_item2B, 3)
                                if item1B_item2B >= best_consumer_utility_1:
                                    if item1B_item2B == best_consumer_utility_1:
                                        revenue_1 = max(revenue_1, 0)
                                    else:
                                        best_consumer_utility_1 = item1B_item2B
                                        revenue_1 = 0
                                

                                ## Now, let's look at the actions of the second consumer
                            
                                # Start with the default of consumer exiting both markets
                                best_consumer_utility_2 = 0
                                revenue_2 = 0

                                # Scenarios where something is purchased from A:
                                both_A = values_A_2[0] + values_A_2[1] - (strategy[0] + strategy[1] - strategy[2])
                                both_A = round(both_A, 3)
                                if both_A >= best_consumer_utility_2:
                                    if both_A == best_consumer_utility_2:
                                        revenue_2 = max(revenue_2, strategy[0] + strategy[1] - strategy[2])
                                    else:
                                        best_consumer_utility_2 = both_A
                                        revenue_2 = strategy[0] + strategy[1] - strategy[2]

                                item1A = values_A_2[0] - strategy[0]
                                item1A = round(item1A, 3)
                                if item1A >= best_consumer_utility_2:
                                    if item1A == best_consumer_utility_2:
                                        revenue_2 = max(revenue_2, strategy[0])
                                    else:
                                        best_consumer_utility_2 = item1A
                                        revenue_2 = strategy[0]

                                item1A_item2B = values_A_2[0] + values_B_2[1] - (strategy[0] + prices_b[1])
                                item1A_item2B = round(item1A_item2B, 3)
                                if item1A_item2B >= best_consumer_utility_2:
                                    if item1A_item2B == best_consumer_utility_2:
                                        revenue_2 = max(revenue_2, strategy[0])
                                    else:    
                                        best_consumer_utility_2 = item1A_item2B
                                        revenue_2 = strategy[0]

                                item2A = values_A_2[1] - strategy[1]
                                item2A = round(item2A, 3)
                                if item2A >= best_consumer_utility_2:
                                    if item2A >= best_consumer_utility_2:
                                        revenue_2 = max(revenue_2, strategy[1])
                                    else:
                                        best_consumer_utility_2 = item2A
                                        revenue_2 = strategy[1]

                                item2A_item1B = values_A_2[1] + values_B_2[0] - (strategy[1] + prices_b[0])
                                item2A_item1B = round(item2A_item1B, 3)
                                if item2A_item1B >= best_consumer_utility_2:
                                    if item2A_item1B == best_consumer_utility_2:
                                        revenue_2 = max(revenue_2, strategy[1])
                                    else:
                                        best_consumer_utility_2 = item2A_item1B
                                        revenue_2 = strategy[1]

                                item1B = values_B_2[0] - prices_b[0]
                                item1B = round(item1B, 3)
                                if item1B >= best_consumer_utility_2:
                                    if item1B == best_consumer_utility_2:
                                        revenue_2 = max(revenue_2, 0)
                                    else:
                                        best_consumer_utility_2 = item1B
                                        revenue_2 = 0

                                item2B = values_B_2[1] - prices_b[1]
                                item2B = round(item2B, 3)
                                if item2B >= best_consumer_utility_2:
                                    if item2B == best_consumer_utility_2:
                                        revenue_2 = max(revenue_2, 0)
                                    else:
                                        best_consumer_utility_2 = item2B
                                        revenue_2 = 0

                                item1B_item2B = values_B_2[0] + values_B_2[1] - (prices_b[0] + prices_b[1])
                                item1B_item2B = round(item1B_item2B, 3)
                                if item1B_item2B >= best_consumer_utility_2:
                                    if item1B_item2B == best_consumer_utility_2:
                                        revenue_2 = max(revenue_2, 0)
                                    else:
                                        best_consumer_utility_2 = item1B_item2B
                                        revenue_2 = 0

                                # Combining the behaviour we see from both consumers
                                total_revenue = revenue_1 + revenue_2
                                expected_value = expected_value + prob*total_revenue
            


print("\n")
print("The payoff by using the strategy", strategy, "is", expected_value)
print("\n")


                                