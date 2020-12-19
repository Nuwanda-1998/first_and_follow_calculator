" This Program will find the First and Follow of Non-Terminals Of given grammer"

grammmer_rules = [] # this variable will store all rules in a list
rules_dic = {} # will hold each rule left and right side(left as Key and right as Value)
firsts = {} # this Dic will hold the result of firsts(Non Terminal is Key and firsts are Value)
final_firsts = {}

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
        print('the terminal_rules_list()Checking for OR is {}'.format(terminal_rules_list))
    else:
        terminal_rules_list = [r_side]
    
    if '~' in terminal_rules_list:
        'This will check for epsilon(we suppose epsilon sign as ~ )'
        is_epsilon = True
        firsts_tuple += ('~',)
    print('the terminal_rules_list is {}'.format(terminal_rules_list))
    for rule in terminal_rules_list:
        'this loop will iterate over/'
        'rules in right side of the arrow/'
        'to find the firsts'
        for_breaker = True # this use to break the following loop
        print('checking the outer for')
        print('the rule is {}'.format(rule))
        for letter in rule:
            print('the letter is {}'.format(letter))
            print('the letter is {}'.format(not letter.isupper()))
            print('the type of letter is {}'.format(type(letter)))
            if for_breaker:
                'this loop will iterate over/'
                'each letter in each rule'
                print('in For Breaker')
                if not letter.isupper() and not letter == '~':# changing the islower to not upper to make app able to recognize other signs instead of lower words
                    is_abs_epsilon = False
                    print('Hello')
                    print('the letter is {}'.format(letter))
                    firsts_tuple += (letter,)
                    firsts_tuple_wtout_eps += (letter,)
                    print('the firsts_tuple is {}'.format(firsts_tuple))
                    print('the firsts_tuple_wtout_eps is {}'.format(firsts_tuple_wtout_eps))
                    for_breaker = False
                    break
                elif letter == '~':
                    print('Bye')
                    if not is_epsilon:
                        firsts_tuple += ('~',)
                        for_breaker = False
                        break
                else:
                    print('Its Upper Letter')
                    if not letter in firsts:
                        print('Its firsts not calculated yet')
                        rightside_of_letter = rules_dic.get(letter)
                        rule_firsts_epsilon = first_calculator(rightside_of_letter)
                        print('the main Tup is OUTER {}, Key is {}'.format(rule_firsts_epsilon[0], letter))
                        rules_first_eps_to_save = rule_firsts_epsilon[0]
                        if rule_firsts_epsilon[1]:
                            main_tup = rule_firsts_epsilon[0]
                            main_tup += ('~',)
                            is_abs_epsilon = True
                            print('the main Tup is {} and the INNER KEY is {}'.format(main_tup, letter))
                            print('is_abs_epsilon {}'.format(is_abs_epsilon))
                            # final_firsts[letter] = main_tup
                            final_firsts[letter] = rule_firsts_epsilon[2]
                            print('final_firsts[IN] is  {}'.format(final_firsts))
                        else:
                            is_abs_epsilon = False
                            firsts[letter] = rules_first_eps_to_save
                            final_firsts[letter] = rules_first_eps_to_save
                            print('final_firsts[OUT] is  {}'.format(final_firsts))
                            print('is epsilon is  {}'.format(rule_firsts_epsilon[1]))
                        conv_list_to_tuple = tuple(rule_firsts_epsilon[0])
                        firsts_tuple = firsts_tuple + conv_list_to_tuple
                        firsts_tuple_wtout_eps = firsts_tuple_wtout_eps + conv_list_to_tuple
                        if rule_firsts_epsilon[1] == False:
                            for_breaker = False # if there wasnt epsilon in the next letter it will break the loop
                    else:
                        print('The first of letter {}  calculated before nad just need to be add'.format(letter))
                        # letter_firsts = firsts.get(letter)
                        letter_firsts = final_firsts.get(letter)
                        letter_firsts_list = list(letter_firsts)
                        for letter in letter_firsts_list:
                            firsts_tuple += (letter,)
                            if letter == '~':
                                is_abs_epsilon = True
                            else:
                                firsts_tuple_wtout_eps += (letter,)
                        # for_breaker = False
            else:
                print('The F Problem')
                for_breaker = False
                break
    if is_abs_epsilon:
        is_epsilon = True
        firsts_tuple += ('~',)
    print('is_abs_epsilon222 {}'.format(is_abs_epsilon))
    firsts_epsilon_answer_list.append(firsts_tuple_wtout_eps)       
    firsts_epsilon_answer_list.append(is_epsilon)
    firsts_epsilon_answer_list.append(firsts_tuple)
    print('the firsts with ~ is {}'.format(firsts_tuple))
    return firsts_epsilon_answer_list

# This lopp is to fill up the all rules in the rules_dic Dictionary
for rules in grammmer_rules:
    str_rule = rules[0] # rules in grammer rules are list and need to be converted to string
    splited_str_rule = str_rule.split(' ') # here we will split the left and right side
    terminal = splited_str_rule[0] # getting the Left side of rule as Terminal
    right_side = splited_str_rule[2] # getting the Right side of rule as Non Terminal
    rules_dic[terminal] = right_side

# this loop is the main loop to do the work
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
    print('there')

# print('{}'.format(firsts))
# print('final_firsts[letter] is  {}'.format(final_firsts))

print("The Firsts Are:")
# print('final_firsts[letter] is  {}'.format(final_firsts))
for key, value in final_firsts.items():
    list_value = list(value) # Convert Value to list
    # print('the Final List Value is {}'.format(list_value)) 
    tuple_value = set([i for i in list_value]) # using set to remove duplicate added values
    tuple_value = tuple(tuple_value) # Make tuple again to show in proper way
    print("First of {}: {}".format(key, tuple_value))
