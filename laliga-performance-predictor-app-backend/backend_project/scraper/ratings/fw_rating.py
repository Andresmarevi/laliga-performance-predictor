def compute_fw_rating(row):

    if row.get('Minutes-match', 0) == 0:
        return 0
    
    goal_impact = (row['Goals-U5'] * 0.1 + row['Goals-U3'] * 0.2 + row['Goals-match'] * 0.7) * 0.5

    assist_impact = (row['Assists-U5'] * 0.1 + row['Assists-U3'] * 0.2 + row['Assists-match'] * 0.7) * 0.25

    shot_impact = (row['ShotsOnGoal-U5'] * 0.1 + row['ShotsOnGoal-U3'] * 0.2 + row['ShotsOnGoal-match'] * 0.7) * 0.15

    dribble_impact = (row['Dribbles-U5'] * 0.1 + row['Dribbles-U3'] * 0.2 + row['Dribbles-match'] * 0.7) * 0.1

    if row['Goals-match'] >= 2:
        goal_impact *= 1.3

    rating = goal_impact + assist_impact + shot_impact + dribble_impact
    return rating