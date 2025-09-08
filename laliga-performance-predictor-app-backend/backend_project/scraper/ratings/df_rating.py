def compute_df_rating(row):
    
    if row.get('Minutes-match', 0) == 0:
        return 0
    
    recoveries = (row['Recoveries-U5'] * 0.2 + row['Recoveries-U3'] * 0.3 + row['Recoveries-match'] * 0.5) * 0.1

    goals_conceded = (row['GoalsConceded-U5'] * 0.2 + row['GoalsConceded-U3'] * 0.3 + row['GoalsConceded-match'] * 0.5)
    goals_conceded_impact = (max(0, 2 - goals_conceded) / 2) * 0.2 

    clean_sheet_bonus = 0.1 if row['GoalsConceded-match'] == 0 and row['Minutes-match'] >= 60 else 0

    goal_contrib = (
        (row['Goals-U5'] * 0.1 + row['Goals-U3'] * 0.2 + row['Goals-match'] * 0.7) * 0.5 +
        (row['Assists-U5'] * 0.1 + row['Assists-U3'] * 0.2 + row['Assists-match'] * 0.7) * 0.4
    )

    rating = (recoveries + goals_conceded_impact + clean_sheet_bonus + goal_contrib)

    return max(0, rating)