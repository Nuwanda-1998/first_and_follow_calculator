from itertools import chain
" This Program will find the Firsts and Follows of Non-Terminals Of given grammer"

grammmer_rules = [] # this variable will store all rules in a list
rules_dic = {} # will hold each rule left and right side(left as Key and right as Value)
firsts = {} # this Dic will hold the result of firsts(Non Terminal is Key and firsts are Value)
final_firsts = {}
follows = {} # Storing the non-Terminals and their Follows

'Reading the file of given grammer'
with open("grammer.txt", "r") as g_file:
    for line in g_file:
        # appending each rule of grammer to grammer_rule variable
        grammmer_rules.append(line.strip().split('\n'))

def first_calculator(r_side):
    """
    this function will find the firsts of 
    given terminal based on its right side.
    (it will be recursive)
    """
    firsts_epsilon_answer_list = [] #this is the variable to be returned at the end
    firsts_tuple = () # this will hold the first`s
    firsts_tuple_wtout_eps = () # this will hold the first`s without epsilon
    is_epsilon = False # epsilon flag for return value
    is_abs_epsilon = False # epsilon flag for return value(This will use for the ones that doesnt have epsilon directly)
    terminal_rules_list = [] # working list in loops
    if '|' in r_side:
        terminal_rules_list = r_side.split('|')
    else:
        terminal_rules_list = [r_side]
    
    if '~' in terminal_rules_list:
        'This will check for epsilon(we suppose epsilon sign as ~ )'
        is_epsilon = True
        firsts_tuple += ('~',)
    for rule in terminal_rules_list:
        'this loop will iterate over/'
        'rules in right side of the arrow/'
        'to find the firsts'
        for_breaker = True # this use to break the following loop
        for letter in rule:
            if for_breaker:
                'this loop will iterate over/'
                'each letter in each rule'
                if not letter.isupper() and not letter == '~':# changing the islower to not upper to make app able to recognize other signs instead of lower words
                    is_abs_epsilon = False
                    firsts_tuple += (letter,)
                    firsts_tuple_wtout_eps += (letter,)
                    for_breaker = False
                    break
                elif letter == '~':
                    if not is_epsilon:
                        is_epsilon = True # Added Now
                        firsts_tuple += ('~',)
                        for_breaker = False
                        break
                else:
                    if not letter in firsts:
                        rightside_of_letter = rules_dic.get(letter)
                        rule_firsts_epsilon = first_calculator(rightside_of_letter)
                        rules_first_eps_to_save = rule_firsts_epsilon[0]
                        if rule_firsts_epsilon[1]:
                            main_tup = rule_firsts_epsilon[0]
                            main_tup += ('~',)
                            is_abs_epsilon = True
                            final_firsts[letter] = rule_firsts_epsilon[2]
                        else:
                            is_abs_epsilon = False
                            firsts[letter] = rules_first_eps_to_save
                            final_firsts[letter] = rules_first_eps_to_save
                        conv_list_to_tuple = tuple(rule_firsts_epsilon[0])
                        firsts_tuple = firsts_tuple + conv_list_to_tuple
                        firsts_tuple_wtout_eps = firsts_tuple_wtout_eps + conv_list_to_tuple
                        if rule_firsts_epsilon[1] == False:
                            for_breaker = False # if there wasnt epsilon in the next letter it will break the loop
                    else:
                        letter_firsts = final_firsts.get(letter)
                        letter_firsts_list = list(letter_firsts)
                        for letter in letter_firsts_list:
                            firsts_tuple += (letter,)
                            if letter == '~':
                                is_abs_epsilon = True
                            else:
                                firsts_tuple_wtout_eps += (letter,)
            else:
                for_breaker = False
                # break # Commented Now
            if is_abs_epsilon:
                is_epsilon = True # Added Now
                firsts_tuple += ('~',) # Added Now
    if is_abs_epsilon:
        is_epsilon = True
        firsts_tuple += ('~',)
    firsts_epsilon_answer_list.append(firsts_tuple_wtout_eps)       
    firsts_epsilon_answer_list.append(is_epsilon)
    firsts_epsilon_answer_list.append(firsts_tuple)
    return firsts_epsilon_answer_list

# This lopp is to fill up the all rules in the rules_dic Dictionary
for rules in grammmer_rules:
    str_rule = rules[0] # rules in grammer rules are list and need to be converted to string
    splited_str_rule = str_rule.split(' ') # here we will split the left and right side
    terminal = splited_str_rule[0] # getting the Left side of rule as Terminal
    right_side = splited_str_rule[2] # getting the Right side of rule as Non Terminal
    rules_dic[terminal] = right_side

# this loop is the main loop to Find the Firsts
for rules in grammmer_rules:
    str_rule = rules[0] # rules in grammer rules are list and need to be converted to string
    splited_str_rule = str_rule.split(' ') # here we will split the left and right side
    terminal = splited_str_rule[0] # getting the Left side of rule as Terminal
    right_side = splited_str_rule[2] # getting the Right side of rule as Non Terminal
    if not terminal in firsts:
        rule_firsts = first_calculator(right_side) # starting the recursive call of first calculator function
        # firsts[terminal] = rule_firsts[0] # the return of first calculator function is firsts and if there is epsilon and firsts without epsilon(we just need firsts here)
        final_firsts[terminal] = rule_firsts[2] # the return of first calculator function is firsts and if there is epsilon and firsts without epsilon(we just need firsts here)
        ## exchange 0 and 2

print("The Firsts Are:")
for key, value in final_firsts.items():
    list_value = list(value) # Convert Value to list
    tuple_value = set([i for i in list_value]) # using set to remove duplicate added values
    tuple_value = tuple(tuple_value) # Make tuple again to show in proper way
    if not key == 'Z':
        print("First of {}: {}".format(key, tuple_value))

#######From Now Implementing Follows#######

follows_final = {}
firsts_list = {} # First Dictionary(The list Version)
# rules_dic = {} # will hold each rule left and right side(left as Key and right as Value)

# Converting Firsts Tuple to list to make/
# working with it easier and removing/
# dplicate value by using Set operator
for key, value in final_firsts.items():
    list_value = list(value) # Convert Value to list
    set_value = set([i for i in list_value]) # using set to remove duplicate added values
    list_value = list(set_value) # convert ti list to use in further use
    firsts_list[key] = list_value

def letter_matching_rightside(letter):
    """
    This function will find right sides
    that including the given letter
    """
    right_sides_of_letter = []
    # print('the rules_dic is {}'.format(rules_dic))
    for key, value in rules_dic.items():
        # print('the value is {}'.format(value))
        # print('the letter is {}'.format(letter))
        # print('the letter is {}'.format(type(letter)))
        # print('the value is {}'.format(type(value)))
        if letter in value:
            # print('the key and value {} {}'.format(key, value))
            # print('the letter in if is {}'.format(letter))
            # # this loop will break the OR and just return asked rule
            # if '|' in value:
            #     split_r_side = value.split('|')
            #     for rule in split_r_side:
            #         if letter in rule:
            #             right_sides_of_letter.append(rule)
            # else:
            right_sides_of_letter.append(value)
    # print('the right_sides_of_letter is {}'.format(right_sides_of_letter))
    return right_sides_of_letter

# function to return key for any value(Getting left side of Grammer)
def get_key(val): 
    for key, value in rules_dic.items():
        if val == value:
            return key 
  
    return "key doesn't exist"

def next_letter_calculator(c_letter, r_side):
    """
    This function will calculate
    next letter.(the answer can be 
    none)
    """
    or_spliting = r_side.split('|')
    is_next_flag = False
    nex_let = [] # this will be return the current letter and next letter
    # print('the Current letter {}'.format(c_letter))
    nex_let.append(r_side)
    for rule in or_spliting:
        if c_letter in rule:
            r_side_length = len(rule)
            # print('the r_side_length is {}'.format(r_side_length))
            r_side_length = r_side_length - 1 # to make it comparable to indexing
            # print('the r_side_length ---1 is {}'.format(r_side_length))
            letter_index = rule.index(c_letter) # getting the index of letter
            # print('the letter_index is {}'.format(letter_index))
            if not r_side_length == letter_index:
                nex_let.append(rule[letter_index +1])
                is_next_flag = True
    if is_next_flag:
        nex_let.append(c_letter)
        # print('the Current letter in final return is {} and next letter is {}'.format(r_side, nex_let))
        return nex_let
    else:
        nex_let.append(False)
        nex_let.append(c_letter)
        # print('the Current letter in final return is {} and next letter is False'.format(nex_let))
        return nex_let

def follow_calculator(l_side):
    """
    This function will calculate the
    follows of given non-terminal
    """
    n_terminal_follows_list = [] # main list to be returned as answer of function
    rules_containing_letter = letter_matching_rightside(l_side) # the rules that contains the non terminal(getting the list of right sides)
    for rule in rules_containing_letter:
        # print('for')
        is_epsilon_continue = True # by default set it true to start the proccess(but in while loop it will continue if there is epsilon)
        next_item_decider = next_letter_calculator(l_side, rule)
        c_rule = next_item_decider[0]
        item = next_item_decider[1]
        c_item = next_item_decider[2]
        while is_epsilon_continue:
            # print('While')
            if item:
                # print('0')
                if not item.isupper() and not item == '~':# if terminal
                    # print('1')
                    n_terminal_follows_list.append(item)
                    is_epsilon_continue = False
                else: # if its non terminal
                    # first_of_next_nterminal = firsts_list[item] # finding the first of the n-terminal in firsts dic
                    first_of_next_nterminal = firsts_list.get(item) # finding the first of the n-terminal in firsts dic
                    n_terminal_follows_list.append(first_of_next_nterminal)
                    if '~' in first_of_next_nterminal:
                        # print('2')
                        # print('~')
                        # n_terminal_follows_list.remove('~')
                        is_epsilon_continue = True
                    else:
                        # print('3')
                        is_epsilon_continue = False
                if is_epsilon_continue:
                    # print('4')
                    next_item_decider = next_letter_calculator(item, rule)
                    c_rule = next_item_decider[0]
                    item = next_item_decider[1]
                    c_item = next_item_decider[2]
            else:
                l_side_current_rule = get_key(c_rule) # getting the left side of the rule(by using the rule)
                if not c_item == l_side_current_rule:
                    # print('5')
                    # print('l_side_current_rule is {}'.format(l_side_current_rule))
                    if l_side_current_rule in follows_final:
                        # print('6')
                        # print('follows_final is {}'.format(follows_final))
                        # print('l_side_current_rule is {}'.format(l_side_current_rule))
                        item_follows = follows_final.get(l_side_current_rule)
                        n_terminal_follows_list.append(item_follows)
                        is_epsilon_continue = False
                    else:
                        is_epsilon_continue = False
                else:
                    if not c_item == l_side_current_rule:
                        # print('7')
                        # print('l_side_current_rule is {}'.format(l_side_current_rule))
                        item_follows = follow_calculator(l_side_current_rule) # if there is no next item, it means we should find the follows of left side
                        # print('item is {}'.format(l_side_current_rule))
                        follows_final[l_side_current_rule] = item_follows # Addinng the follows of Calculated Follows to the final list
                        n_terminal_follows_list.append(item_follows)
                        is_epsilon_continue = False
                    else:
                        is_epsilon_continue = False

                # n_terminal_follows_list.append(first_of_next_nterminal)
    # print('finallllllllyyyyyy')
    return n_terminal_follows_list

def list_valu_calculator(nes_list):
    """
    This function will calculate
    the values in unkown nested list
    """
    # inside_nest_list = list(chain.from_iterable(inner_list))
    # if isinstance(letter, str):
    # flat_list = [item for sublist in value for item in sublist]
    flat_list = nes_list
    final_flat_list = nes_list
    rectify_needed = False
    while_ender = True
    while while_ender:
        while_ender = False
        for item in flat_list:
            if isinstance(item, str):
                pass
            else:
                rectify_needed = True
                while_ender = True
        if rectify_needed:
            flat_list = [item for sublist in flat_list for item in sublist]
            final_flat_list = flat_list
    while '~' in final_flat_list: # Removing the duplicates
        final_flat_list.remove('~')
    return final_flat_list

# this loop is the main loop to Find the Follows
for rules in grammmer_rules:
    str_rule = rules[0] # rules in grammer rules are list and need to be converted to string
    splited_str_rule = str_rule.split(' ') # here we will split the left and right side
    terminal = splited_str_rule[0] # getting the Left side of rule as Terminal
    if not terminal in follows_final and not terminal == 'Z':
        # print('terminal is {}'.format(terminal))
        terminal_follows = follow_calculator(terminal) # starting the recursive call of first calculator function
        follows_final[terminal] = terminal_follows # it just return the Follows of the Terminal

print('\n \n')

print("The Follows Are:")
# print("Follows Are {}".format(follows_final))
for key, value in follows_final.items():
    # print("list_value to send is {} , key is {}".format(value, key))
    list_value = list_valu_calculator(value)
    # print("list Are {}".format(list_value))
    # while '~' in list_value:
    #     list_value.remove('~')
    # print("list After Are {}".format(list_value))
    tuple_value = set([i for i in list_value]) # using set to remove duplicate added values
    tuple_value = tuple(tuple_value) # Make tuple to show in proper way
    print("Follows of {}: {}".format(key, tuple_value))

print('\n \n \n end')
