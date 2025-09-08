def compute_gk_rating(row):
    
    if row.get('Minutes-match', 0) == 0:
        return 0
    
    saves = (row['Sav-U5'] * 0.2 + row['Sav-U3'] * 0.3 + row['Sav-match'] * 0.5) * 0.2
    
    goals_conceded = (row['GoalsConced-U5'] * 0.2 + row['GoalsConced-U3'] * 0.3 + row['GoalsConced-match'] * 0.5)
    goals_conceded_impact = (max(0, 3 - goals_conceded) / 3) * 0.3  
    
    clean_sheet_bonus = 0.1 if row['GoalsConced-match'] == 0 else 0

    pen_saves = (row['PenSav-U5'] * 0.2 + row['PenSav-U3'] * 0.3 + row['PenSav-match'] * 0.5) * 0.4

    errors = (row['ErrorGoal-U5'] * 0.2 + row['ErrorGoal-U3'] * 0.3 + row['ErrorGoal-match'] * 0.5) * -0.3

    rating = saves + goals_conceded_impact + clean_sheet_bonus + pen_saves + errors

    return max(0, rating)