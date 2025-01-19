from BinaryTree import *

u = 1.1
d = 0.9
r = 0.05
K = 105
S0 = 100
T = 2

import numpy as np
q_u = (np.e**(r) - d) / (u - d)
q_d = 1 - q_u
Call = True
## If Put please change it to False

BT = BinaryTree(S0, q_u)

for prev_period in range(T):
    for index in range(2 ** prev_period):
        BT.add_child(prev_period, index, BT.get_node(prev_period, index) * u, BT.get_node(prev_period, index) * d)

BT_payoff = BinaryTree(0, 0)
BT.copy_to(BT_payoff)
BT_payoff.bulk_create(T + 1)

for level in range(1, T + 1):
    for index in range(2 ** level):
        if Call:
            payoff = max(BT.get_node(level, index) - K, 0)
        else:
            payoff = max(K - BT.get_node(level, index), 0)
        BT_payoff.update_node(level, index, payoff)


for level in range(T):
    for index in range(2 ** level):
        BT_payoff.update_node(level, index, BT_payoff.pv(level, index, r))

print(BT_payoff)