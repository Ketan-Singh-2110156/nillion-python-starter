from nada_dsl import *

def initialize_voters(num_voters):
    voters = []
    for i in range(num_voters):
        voters.append(Party(name="Voter" + str(i)))
    return voters

def inputs_initialization(num_voters, num_candidates, voters):
    votes_per_candidate = []
    for c in range(num_candidates):
        votes_per_candidate.append([])
        for v in range(num_voters):
            votes_per_candidate[c].append(SecretUnsignedInteger(Input(name="v" + str(v) + "_c" + str(c), party=voters[v])))
    return votes_per_candidate

def count_votes(num_voters, num_candidates, votes_per_candidate, out_party):
    votes = []
    for c in range(num_candidates):
        result = votes_per_candidate[c][0]
        for v in range(1, num_voters):
            result += votes_per_candidate[c][v]
        votes.append(Output(result, "final_vote_count_c" + str(c), out_party))
    return votes

def check_sum(num_voters, num_candidates, votes_per_candidate, out_party):
    check_sums = []
    for v in range(num_voters):
        check = votes_per_candidate[0][v]
        for c in range(1, num_candidates):
            vote_v_c = votes_per_candidate[c][v]
            check += vote_v_c
        check_sums.append(Output(check, "check_sum_v" + str(v), out_party))
    return check_sums

def check_product(num_voters, num_candidates, votes_per_candidate, out_party):
    check_products = []
    for v in range(num_voters):
        for c in range(num_candidates):
            vote_v_c = votes_per_candidate[c][v]
            check_v_c_product = (UnsignedInteger(1) - vote_v_c) * (UnsignedInteger(2) - vote_v_c)
            check_products.append(Output(check_v_c_product, "check_prod_v" + str(v) + "_c" + str(c), out_party))
    return check_products

def nada_main():
    num_voters = 3
    num_candidates = 2

    voters = initialize_voters(num_voters)
    out_party = Party(name="OutParty")

    votes_per_candidate = inputs_initialization(num_voters, num_candidates, voters)
    
    votes = count_votes(num_voters, num_candidates, votes_per_candidate, out_party)
    check_sums = check_sum(num_voters, num_candidates, votes_per_candidate, out_party)
    check_products = check_product(num_voters, num_candidates, votes_per_candidate, out_party)

    results = votes + check_sums + check_products
    return results
