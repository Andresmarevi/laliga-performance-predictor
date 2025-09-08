def compute_mf_rating(row):

    if row.get('Minutes-match', 0) == 0:
        return 0
    
    assists = (row['Assists-U5'] * 0.1 + row['Assists-U3'] * 0.2 + row['Assists-match'] * 0.7)
    key_passes = (row['KeyPasses-U5'] * 0.2 + row['KeyPasses-U3'] * 0.3 + row['KeyPasses-match'] * 0.5)
    creativity = (assists + key_passes) * 0.6

    goal_impact = (row['Goals-U5'] * 0.1 + row['Goals-U3'] * 0.2 + row['Goals-match'] * 0.7) * 0.2

    defensive_work = (row['Recoveries-U5'] * 0.2 + row['Recoveries-U3'] * 0.3 + row['Recoveries-match'] * 0.5) * 0.2

    rating = creativity + goal_impact + defensive_work
    
    return rating