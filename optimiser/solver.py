import pulp, pandas as pd
from fpl_ai.config import BUDGET, POSITIONS, SQUAD_LIMITS, TEAM_LIMIT

def build_team(expected_points: pd.Series, meta: pd.DataFrame):
    players = expected_points.index.tolist()
    prob = pulp.LpProblem("FPL", pulp.LpMaximize)
    pick = pulp.LpVariable.dicts("pick", players, cat="Binary")

    # Objective
    prob += pulp.lpSum([expected_points[p] * pick[p] for p in players])

    # Budget
    prob += pulp.lpSum([meta.loc[p, "now_cost"] * pick[p] for p in players]) <= BUDGET * 10  # cost in £0.1m

    # Squad size 15
    prob += pulp.lpSum([pick[p] for p in players]) == 15

    # Position constraints
    for pos, name in POSITIONS.items():
        prob += pulp.lpSum([pick[p] for p in players if meta.loc[p, "element_type"] == pos]) == SQUAD_LIMITS[name]

    # Max 3 per EPL club
    for t in meta.team.unique():
        prob += pulp.lpSum([pick[p] for p in players if meta.loc[p, "team"] == t]) <= TEAM_LIMIT

    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    squad_ids = [p for p in players if pick[p].value() == 1]
    return meta.loc[squad_ids]
