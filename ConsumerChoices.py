# Given a pricing scheme by each of the two Producers, this code determines what each possible consumer type will optimally choose to select
import numpy as np 

# What are the two Producers' pricing schemes?
prices_a = [0.5, 0.5, 0]
prices_b = [0.5, 0.5, 0]

# Which values of x and y are we going to allow?
sequence_x = [0, 1/2, 1]
sequence_y = [-1, 0, 1]
multiplier = 0.1

# Set up a Matrix to store values
choices = np.zeros((9,9))

for a in range(len(sequence_x)):
    for b in range(len(sequence_x)):
        for c in range(len(sequence_y)):
            for d in range(len(sequence_y)):
                x = [sequence_x[a], sequence_x[b]]
                x = np.array(x)

                y = [sequence_y[c], sequence_y[d]]
                y = np.array(y)

                values_A = x + multiplier*y
                values_B = x - multiplier*y

                total_revenue = 0
                ## Start by looking at the actions for the first consumer
                # Note, in the following, utility refers to the customer's payoff, and revenue refers to the firm's payoff

                # Start with the default of consumer exiting both markets
                best_consumer_utility = 0
                revenue = 0
                choice = "None"

                # Scenarios where something is purchased from A:
                both_A = values_A[0] + values_A[1] - (prices_a[0] + prices_a[1] - prices_a[2])
                both_A = round(both_A, 3)
                if both_A >= best_consumer_utility:
                    if best_consumer_utility == both_A:
                        if prices_a[0] + prices_a[1] - prices_a[2] >= revenue:
                            choice = "Bundle A"
                        revenue = max(revenue, prices_a[0] + prices_a[1] - prices_a[2])
                    else:
                        best_consumer_utility = both_A
                        revenue = prices_a[0] + prices_a[1] - prices_a[2]
                        choice = "Bundle A"

                item1A = values_A[0] - prices_a[0]
                item1A = round(item1A, 3)
                if item1A >= best_consumer_utility:
                    if item1A == best_consumer_utility:
                        if prices_a[0] >= revenue:
                            choice = "Item 1 A"
                        revenue = max(revenue, prices_a[0])
                    else:
                        best_consumer_utility = item1A
                        revenue = prices_a[0]
                        choice = "Item 1 A"

                item1A_item2B = values_A[0] + values_B[1] - (prices_a[0] + prices_b[1])
                item1A_item2B = round(item1A_item2B, 3)
                if item1A_item2B >= best_consumer_utility:
                    if item1A_item2B == best_consumer_utility:
                        if prices_a[0] >= revenue:
                            choice = "Item 1 A, Item 2 B"
                        revenue = max(revenue, prices_a[0])
                    else:
                        best_consumer_utility = item1A_item2B
                        revenue = prices_a[0]
                        choice = "Item 1 A, Item 2 B"

                item2A = values_A[1] - prices_a[1]
                item2A = round(item2A, 3)
                if item2A >= best_consumer_utility:
                    if item2A == best_consumer_utility:
                        if prices_a[1] >= revenue:
                            choice = "Item 2 A"
                        revenue = max(revenue, prices_a[1])
                    else:
                        best_consumer_utility = item2A
                        revenue = prices_a[1]
                        choice = "Item 2 A"

                item2A_item1B = values_A[1] + values_B[0] - (prices_a[1] + prices_b[0])
                item2A_item1B = round(item2A_item1B, 3)
                if item2A_item1B >= best_consumer_utility:
                    if item2A_item1B == best_consumer_utility:
                        if prices_a[1] >= revenue:
                            choice = "Item 2 A, Item 1 B"
                        revenue = max(revenue, prices_a[1])
                    else:
                        best_consumer_utility = item2A_item1B
                        revenue = prices_a[1]
                        choice = "Item 2 A, Item 1 B"

                item1B = values_B[0] - prices_b[0]
                item1B = round(item1B, 3)
                if item1B >= best_consumer_utility:
                    if item1B == best_consumer_utility:
                        if 0 >= revenue:
                            choice = "Item 1 B"
                        revenue = max(revenue, 0)
                    else:
                        best_consumer_utility = item1B
                        revenue = 0
                        choice = "Item 1 B"

                item2B = values_B[1] - prices_b[1]
                item2B = round(item2B, 3)
                if item2B >= best_consumer_utility:
                    if item2B == best_consumer_utility:
                        if 0 >= revenue:
                            choice = "Item 2 B"
                        revenue = max(revenue, 0)
                    else:
                        best_consumer_utility = item2B
                        revenue = 0
                        choice = "Item 2 B"

                item1B_item2B = values_B[0] + values_B[1] - (prices_b[0] + prices_b[1])
                item1B_item2B = round(item1B_item2B, 3)
                if item1B_item2B >= best_consumer_utility:
                    if item1B_item2B == best_consumer_utility:
                        if 0 >= revenue:
                            choice = "Item 1 B, Item 2 B"
                        revenue = max(revenue, 0)
                    else:
                        best_consumer_utility = item1B_item2B
                        revenue = 0
                        choice = "Item 1 B, Item 2 B"
                
                print(choice)

