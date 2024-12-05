# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 12:52:26 2024

@author: Richard.Smith
"""

--- Day 5: Print Queue ---
Satisfied with their search on Ceres, the squadron of scholars suggests subsequently scanning the stationery stacks of sub-basement 17.

The North Pole printing department is busier than ever this close to Christmas, and while The Historians continue their search of this historically significant facility, an Elf operating a very familiar printer beckons you over.

The Elf must recognize you, because they waste no time explaining that the new sleigh launch safety manual updates won't print correctly. Failure to update the safety manuals would be dire indeed, so you offer your services.

Safety protocols clearly indicate that new pages for the safety manuals must be printed in a very specific order. The notation X|Y means that if both page number X and page number Y are to be produced as part of an update, page number X must be printed at some point before page number Y.

The Elf has for you both the page ordering rules and the pages to produce in each update (your puzzle input), but can't figure out whether each update has the pages in the right order.

For example:

47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
The first section specifies the page ordering rules, one per line. The first rule, 47|53, means that if an update includes both page number 47 and page number 53, then page number 47 must be printed at some point before page number 53. (47 doesn't necessarily need to be immediately before 53; other pages are allowed to be between them.)

The second section specifies the page numbers of each update. Because most safety manuals are different, the pages needed in the updates are different too. The first update, 75,47,61,53,29, means that the update consists of page numbers 75, 47, 61, 53, and 29.

To get the printers going as soon as possible, start by identifying which updates are already in the right order.

In the above example, the first update (75,47,61,53,29) is in the right order:

75 is correctly first because there are rules that put each other page after it: 75|47, 75|61, 75|53, and 75|29.
47 is correctly second because 75 must be before it (75|47) and every other page must be after it according to 47|61, 47|53, and 47|29.
61 is correctly in the middle because 75 and 47 are before it (75|61 and 47|61) and 53 and 29 are after it (61|53 and 61|29).
53 is correctly fourth because it is before page number 29 (53|29).
29 is the only page left and so is correctly last.
Because the first update does not include some page numbers, the ordering rules involving those missing page numbers are ignored.

The second and third updates are also in the correct order according to the rules. Like the first update, they also do not include every page number, and so only some of the ordering rules apply - within each update, the ordering rules that involve missing page numbers are not used.

The fourth update, 75,97,47,61,53, is not in the correct order: it would print 75 before 97, which violates the rule 97|75.

The fifth update, 61,13,29, is also not in the correct order, since it breaks the rule 29|13.

The last update, 97,13,75,29,47, is not in the correct order due to breaking several rules.

For some reason, the Elves also need to know the middle page number of each update being printed. Because you are currently only printing the correctly-ordered updates, you will need to find the middle page number of each correctly-ordered update. In the above example, the correctly-ordered updates are:

75,47,61,53,29
97,61,53,29,13
75,29,13
These have middle page numbers of 61, 53, and 29 respectively. Adding these page numbers together gives 143.

Of course, you'll need to be careful: the actual list of page ordering rules is bigger and more complicated than the above example.

Determine which updates are already in the correct order. What do you get if you add up the middle page number from those correctly-ordered updates?

#%%
import pandas as pd
from collections import defaultdict, deque

# Import Day 5 .txt file
file_path = 'C:/Users/Richard.Smith/Downloads/day_05.txt'

# Read the file content and parse into Rules and Updates DF's
def parse_input(file_path):
    with open(file_path, 'r') as file:
        content = file.read().strip()
    rules_part, updates_part = content.split('\n\n')
    
    # Split the rules part into a list and create a DataFrame
    rules = [line.split('|') for line in rules_part.splitlines()]
    rules_df = pd.DataFrame(rules, columns=['X', 'Y']).astype(int)
    
    # Split the updates part into a list and create a DataFrame
    updates = [list(map(int, line.split(','))) for line in updates_part.splitlines()]
    updates_df = pd.DataFrame(updates)
    
    return rules_df, updates_df

# Function to check order of a single update and return rule validation details
def check_update_order(rules_df, update):
    
    # Filter rules that apply to the current update
    applicable_rules_df = rules_df[rules_df['X'].isin(update) & rules_df['Y'].isin(update)]
    position = {page: idx for idx, page in enumerate(update)}
    validated_rules = []
    violated_rules = []
    
    # Check each rule to see if it's validated or violated based on the page positions
    for _, rule in applicable_rules_df.iterrows():
        if position.get(rule['X'], -1) < position.get(rule['Y'], -1):
            validated_rules.append(f"{rule['X']}|{rule['Y']}")
        else:
            violated_rules.append(f"{rule['X']}|{rule['Y']}")

    # Determine if the update is ordered correctly
    is_correct = not violated_rules  # Correct if no rules are violated
    
    # Join rule details into strings for display
    applicable_rules_str = ', '.join(f"{row['X']}|{row['Y']}" for _, row in applicable_rules_df.iterrows())
    return is_correct, applicable_rules_str, ', '.join(validated_rules), ', '.join(violated_rules)

# Function to process all updates and return results in df
def process_updates(file_path):
    rules_df, updates_df = parse_input(file_path)
    results_data = {
        'Update': [],
        'Is Correctly Ordered': [],
        'Middle Page': [],
        'Applicable Rules': [],
        'Validated Rules': [],
        'Violated Rules': []
    }

    # Evaluate each update for rule compliance and calculate the middle page
    for index, update_row in updates_df.iterrows():
        update = update_row.dropna().astype(int).tolist()
        is_correct, applicable_rules_str, validated_rules, violated_rules = check_update_order(rules_df, update)
        middle_page = update[len(update) // 2] if update else None
        
        # Append each update's results to the results_data dictionary
        results_data['Update'].append(update)
        results_data['Is Correctly Ordered'].append(is_correct)
        results_data['Middle Page'].append(middle_page)
        results_data['Applicable Rules'].append(applicable_rules_str)
        results_data['Validated Rules'].append(validated_rules)
        results_data['Violated Rules'].append(violated_rules)
    
    results_df = pd.DataFrame(results_data)
    return results_df, rules_df, updates_df

# Execute the process and calculate the sum of middle pages for correctly ordered updates
results_df, rules_df, updates_df = process_updates(file_path)
sum_middle_pages = results_df.loc[results_df['Is Correctly Ordered'], 'Middle Page'].sum()

# Output the results
print("Sum of Middle Pages where ordered correctly:", sum_middle_pages)

#%%

--- Part Two ---
While the Elves get to work printing the correctly-ordered updates, you have a little time to fix the rest of them.

For each of the incorrectly-ordered updates, use the page ordering rules to put the page numbers in the right order. For the above example, here are the three incorrectly-ordered updates and their correct orderings:

75,97,47,61,53 becomes 97,75,47,61,53.
61,13,29 becomes 61,29,13.
97,13,75,29,47 becomes 97,75,47,29,13.
After taking only the incorrectly-ordered updates and ordering them correctly, their middle page numbers are 47, 29, and 47. Adding these together produces 123.

Find the updates which are not in the correct order. What do you get if you add up the middle page numbers after correctly ordering just those updates?

#%%
# Function to perform topological sorting based on provided rules and a list of page numbers
def topological_sort(rules_df, update):
    # Create a graph and in-degree dictionary to store the relationships and prerequisites counts
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    
    # Build the graph from rules applicable to the current update
    for _, rule in rules_df[rules_df['X'].isin(update) & rules_df['Y'].isin(update)].iterrows():
        graph[rule['X']].append(rule['Y'])
        in_degree[rule['Y']] += 1

    # Queue to manage pages with no prerequisites (in-degree of 0)
    queue = deque([page for page in update if in_degree[page] == 0])
    sorted_order = []

    # Process the queue until empty
    while queue:
        node = queue.popleft()
        sorted_order.append(node)
        # Reduce the in-degree of connected nodes and add to queue if in-degree becomes 0
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return [int(page) for page in sorted_order]  # Ensure conversion to native Python int

# Function to process updates, reorder them if incorrectly ordered, and calculate middle pages
def fix_and_sum_incorrect_updates(results_df, rules_df):
    sum_middle_pages_incorrect = 0
    updated_results = []

    # Process each update and check if it's incorrectly ordered
    for i, row in results_df[results_df['Is Correctly Ordered'] == False].iterrows():
        update = row['Update']
        # Correct the order of the update
        corrected_order = topological_sort(rules_df, update)
        # Calculate the middle page after reordering
        middle_page = corrected_order[len(corrected_order) // 2]
        sum_middle_pages_incorrect += middle_page
        # Collect results including the corrected order of pages
        updated_results.append({
            'Update': update,
            'Corrected Order': corrected_order,
            'Middle Page': middle_page
        })

    # Create a DataFrame to display corrected orders and their middle pages
    corrected_updates_df = pd.DataFrame(updated_results)
    return corrected_updates_df, sum_middle_pages_incorrect

print("Sum of Middle Pages of Corrected Incorrectly Ordered Updates:", sum_middle_pages_incorrect)

#%%

# Add Corrected Order to results_df
def process_updates(file_path):
    rules_df, updates_df = parse_input(file_path)
    results_data = {
        'Update': [],
        'Is Correctly Ordered': [],
        'Middle Page': [],
        'Applicable Rules': [],
        'Validated Rules': [],
        'Violated Rules': [],
        'Corrected Order': []  # Adding the corrected order to the results data
    }

    for index, update_row in updates_df.iterrows():
        update = update_row.dropna().astype(int).tolist()
        is_correct, applicable_rules_str, validated_rules, violated_rules = check_update_order(rules_df, update)
        middle_page = update[len(update) // 2] if update else None
        corrected_order = topological_sort(rules_df, update) if not is_correct else update
        
        results_data['Update'].append(update)
        results_data['Is Correctly Ordered'].append(is_correct)
        results_data['Middle Page'].append(middle_page)
        results_data['Applicable Rules'].append(applicable_rules_str)
        results_data['Validated Rules'].append(validated_rules)
        results_data['Violated Rules'].append(violated_rules)
        results_data['Corrected Order'].append(corrected_order)
    
    results_df = pd.DataFrame(results_data)
    return results_df

results_df = process_updates(file_path)
