'''Compare_QLearn_to_VI.py
Added to the starter code on Feb. 18 to facilitate
quantitative comparison of Q Learning with Value Iteration results.

S. Tanimoto,
Paul G. Allen School of Computer Sci. & Engineering,
Univ. of Washington.
'''

Q_from_VI=None; Q_from_QL=None;  V_from_VI=None;  V_from_QL=None; \
    POLICY_from_VI=None;  POLICY_from_QL=None; Terminal_state=None; \
    ALL_STATES=None;  ACTIONS=None;  NGOALS=None; GOLDEN_PATH=None;  SILVER_PATH=None; 

TOH={}
def receive_globals(TOH_globals):
    TOH = TOH_globals
    global Q_from_VI, Q_from_QL, V_from_VI, V_from_QL,\
                POLICY_from_VI, POLICY_from_QL, Terminal_state,\
                ALL_STATES, ACTIONS, NGOALS, GOLDEN_PATH, SILVER_PATH
    Q_from_VI=TOH['Q_from_VI']
    Q_from_QL=TOH['Q_from_QL']
    V_from_VI=TOH['V_from_VI']
    V_from_QL=TOH['V_from_QL']
    POLICY_from_VI=TOH['POLICY_from_VI']
    POLICY_from_QL=TOH['POLICY_from_QL']
    Terminal_state=TOH['Terminal_state']
    ALL_STATES=TOH['ALL_STATES']
    ACTIONS=TOH['ACTIONS']
    NGOALS=TOH['NGOALS']
    GOLDEN_PATH=TOH['GOLDEN_PATH']
    SILVER_PATH=TOH['SILVER_PATH']
                
def full_compare():
    print("Let's do a full comparison... ")
    print("Policy comparison:")
    all_subsets = [("all states", ALL_STATES), ("golden path", GOLDEN_PATH)]
    if NGOALS==2:
        if SILVER_PATH==[]:
            print("Error: SILVER_PATH is empty")
        else:
            all_subsets+=[("silver path", SILVER_PATH)]
    for (name, subset) in all_subsets:
        results = compare_policies(subset)
        print("For "+name+", policies agree on "+\
              str(results[0])+" states out of "+str(results[1])+\
              "; percentage="+str(100*results[2])+".")
    print('') # newline

    print("Comparison of state values:")
    for (name, subset) in all_subsets:
        results = compare_state_vals(subset)
        print("For "+name+", mean squared error is "+str(results)+".")
    print('') # newline
        
    print("Comparison of Q values:")
    for (name, subset) in all_subsets:
        results = compare_q_vals(subset)
        print("For "+name+", mean squared error is "+str(results)+".")
    print('') # newline
    

    
def compare_policies(state_subset=ALL_STATES):
    # For the given states, compute the number of states on
    # which the VI and QL-based policies match.
    match_count = 0
    n_states = 0
    for s in state_subset:
        if s==Terminal_state: continue
        n_states += 1
        try:
            a_VI = POLICY_from_VI[s]
            a_QL = POLICY_from_QL[s]
            if a_VI==a_QL: match_count += 1
        except: pass
    return (match_count, n_states, match_count / n_states)

def compare_state_vals(state_subset=ALL_STATES):
    sum_sq_diffs = 0.0
    n_states = 0
    for s in state_subset:
        if s==Terminal_state: continue
        n_states += 1
        v_VI = V_from_VI[s]
        v_QL = V_from_QL[s]
        sum_sq_diffs += (v_VI - v_QL)**2
    mean_sq_error = sum_sq_diffs / n_states
    return mean_sq_error

def compare_q_vals(state_subset=ALL_STATES):
    sum_sq_diffs = 0.0
    n_q_vals = 0
    for s in state_subset:
        if s==Terminal_state: continue
        for a in ACTIONS:
            try:
                q_VI = Q_from_VI[(s,a)]
                q_QL = Q_from_QL[(s,a)]
                sum_sq_diffs += (q_VI - q_QL)**2
                n_q_vals += 1
            except: pass
    mean_sq_error = sum_sq_diffs / n_q_vals
    return mean_sq_error
   
    
