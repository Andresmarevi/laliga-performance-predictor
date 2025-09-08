from scraper.models import GoalkeeperMatch, DefenderMatch, MidfielderMatch, ForwardMatch
from scraper.ratings.gk_rating import compute_gk_rating
from scraper.ratings.df_rating import compute_df_rating
from scraper.ratings.mf_rating import compute_mf_rating
from scraper.ratings.fw_rating import compute_fw_rating

def get_player_performance_evolution(slug, season_slug='laliga-24-25'):
    for model, pos, extra_field, rating_func in [
        (GoalkeeperMatch, 'goalkeeper', 'saves', compute_gk_rating),
        (DefenderMatch, 'defender', 'recoveries', compute_df_rating),
        (MidfielderMatch, 'midfielder', 'key_passes', compute_mf_rating),
        (ForwardMatch, 'forward', 'goals', compute_fw_rating),
    ]:
        if model.objects.filter(player=slug, season=season_slug).exists():
            matches = list(model.objects.filter(player=slug, season=season_slug).order_by('matchday'))
            break
    else:
        return []

    def avg(matches, attr):
        vals = [getattr(m, attr, 0) for m in matches]
        return round(sum(vals) / len(vals), 2) if vals else 0

    evolution = []
    for idx, m in enumerate(matches):
        u5 = matches[max(0, idx-4):idx+1]
        u3 = matches[max(0, idx-2):idx+1]

        if isinstance(m, GoalkeeperMatch):
            data = {
                'Sav-U5': avg(u5, 'saves'),
                'Sav-U3': avg(u3, 'saves'),
                'Sav-match': m.saves,
                'GoalsConced-U5': avg(u5, 'goals_conceded'),
                'GoalsConced-U3': avg(u3, 'goals_conceded'),
                'GoalsConced-match': m.goals_conceded,
                'Minutes-U5': avg(u5, 'minutes'),
                'Minutes-U3': avg(u3, 'minutes'),
                'Minutes-match': m.minutes,
                'ErrorGoal-U5': avg(u5, 'errors_leading_to_goal'),
                'ErrorGoal-U3': avg(u3, 'errors_leading_to_goal'),
                'ErrorGoal-match': m.errors_leading_to_goal,
                'PenSav-U5': avg(u5, 'penalties_saved'),
                'PenSav-U3': avg(u3, 'penalties_saved'),
                'PenSav-match': m.penalties_saved,
            }
            perf = round(compute_gk_rating(data), 3)
        elif isinstance(m, DefenderMatch):
            data = {
                'Recoveries-U5': avg(u5, 'recoveries'),
                'Recoveries-U3': avg(u3, 'recoveries'),
                'Recoveries-match': m.recoveries,
                'GoalsConceded-U5': avg(u5, 'goals_conceded'),
                'GoalsConceded-U3': avg(u3, 'goals_conceded'),
                'GoalsConceded-match': m.goals_conceded,
                'Minutes-U5': avg(u5, 'minutes'),
                'Minutes-U3': avg(u3, 'minutes'),
                'Minutes-match': m.minutes,
                'Goals-U5': avg(u5, 'goals'),
                'Goals-U3': avg(u3, 'goals'),
                'Goals-match': m.goals,
                'Assists-U5': avg(u5, 'assists'),
                'Assists-U3': avg(u3, 'assists'),
                'Assists-match': m.assists,
            }
            perf = round(compute_df_rating(data), 3)
        elif isinstance(m, MidfielderMatch):
            data = {
                'Recoveries-U5': avg(u5, 'recoveries'),
                'Recoveries-U3': avg(u3, 'recoveries'),
                'Recoveries-match': m.recoveries,
                'Goals-U5': avg(u5, 'goals'),
                'Goals-U3': avg(u3, 'goals'),
                'Goals-match': m.goals,
                'Assists-U5': avg(u5, 'assists'),
                'Assists-U3': avg(u3, 'assists'),
                'Assists-match': m.assists,
                'Minutes-U5': avg(u5, 'minutes'),
                'Minutes-U3': avg(u3, 'minutes'),
                'Minutes-match': m.minutes,
                'KeyPasses-U5': avg(u5, 'key_passes'),
                'KeyPasses-U3': avg(u3, 'key_passes'),
                'KeyPasses-match': m.key_passes,
            }
            perf = round(compute_mf_rating(data), 3)
        elif isinstance(m, ForwardMatch):
            data = {
                'Goals-U5': avg(u5, 'goals'),
                'Goals-U3': avg(u3, 'goals'),
                'Goals-match': m.goals,
                'Assists-U5': avg(u5, 'assists'),
                'Assists-U3': avg(u3, 'assists'),
                'Assists-match': m.assists,
                'Minutes-U5': avg(u5, 'minutes'),
                'Minutes-U3': avg(u3, 'minutes'),
                'Minutes-match': m.minutes,
                'ShotsOnGoal-U5': avg(u5, 'shots_on_goal'),
                'ShotsOnGoal-U3': avg(u3, 'shots_on_goal'),
                'ShotsOnGoal-match': m.shots_on_goal,
                'Dribbles-U5': avg(u5, 'dribbles'),
                'Dribbles-U3': avg(u3, 'dribbles'),
                'Dribbles-match': m.dribbles,
            }
            perf = round(compute_fw_rating(data), 3)
        else:
            perf = None

        evolution.append({
            "matchday": getattr(m, 'matchday', None),
            "performance_rating": perf,
            "extra": getattr(m, extra_field, None)
        })
    return evolution