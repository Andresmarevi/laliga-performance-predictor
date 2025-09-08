import joblib
import os
import numpy as np
from .utils import get_last_match_data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'data\\models')

MODEL_PATHS = {
    'goalkeeper': {
        'performance': {
            'next_1': 'goalkeeper/ratings/best_model_Rating-F1_LinearRegression_8f.pkl',
            'next_2': 'goalkeeper/ratings/best_model_Rating-F2_LinearRegression_8f.pkl',
            'next_3': 'goalkeeper/ratings/best_model_Rating-F3_LinearRegression_5f.pkl',
            'next_5': 'goalkeeper/ratings/best_model_Rating-F5_LinearRegression_3f.pkl',
        },
        'saves': {
            'next_1': 'goalkeeper/saves/best_model_Saves-F1_LinearRegression_10f.pkl',
            'next_2': 'goalkeeper/saves/best_model_Saves-F2_LinearRegression_5f.pkl',
            'next_3': 'goalkeeper/saves/best_model_Saves-F3_LinearRegression_5f.pkl',
            'next_5': 'goalkeeper/saves/best_model_Saves-F5_LinearRegression_8f.pkl',
        }
    },
    'defender': {
        'performance': {
            'next_1': 'defender/ratings/best_model_Rating-F1_LinearRegression_13f.pkl',
            'next_2': 'defender/ratings/best_model_Rating-F2_LinearRegression_10f.pkl',
            'next_3': 'defender/ratings/best_model_Rating-F3_LinearRegression_8f.pkl',
            'next_5': 'defender/ratings/best_model_Rating-F5_LinearRegression_13f.pkl',
        },
        'recoveries': {
            'next_1': 'defender/recoveries/best_model_Recoveries-F1_LinearRegression_5f.pkl',
            'next_2': 'defender/recoveries/best_model_Recoveries-F2_LinearRegression_5f.pkl',
            'next_3': 'defender/recoveries/best_model_Recoveries-F3_LinearRegression_3f.pkl',
            'next_5': 'defender/recoveries/best_model_Recoveries-F5_LinearRegression_8f.pkl',
        }
    },
    'midfielder': {
        'performance': {
            'next_1': 'midfielder/ratings/best_model_Rating-F1_LinearRegression_16f.pkl',
            'next_2': 'midfielder/ratings/best_model_Rating-F2_LinearRegression_16f.pkl',
            'next_3': 'midfielder/ratings/best_model_Rating-F3_LinearRegression_10f.pkl',
            'next_5': 'midfielder/ratings/best_model_Rating-F5_LinearRegression_8f.pkl',
        },
        'key_passes': {
            'next_1': 'midfielder/keyPasses/best_model_KeyPasses-F1_LinearRegression_5f.pkl',
            'next_2': 'midfielder/keyPasses/best_model_KeyPasses-F2_LinearRegression_8f.pkl',
            'next_3': 'midfielder/keyPasses/best_model_KeyPasses-F3_GradientBoosting_13f.pkl',
            'next_5': 'midfielder/keyPasses/best_model_KeyPasses-F5_GradientBoosting_13f.pkl',
        }
    },
    'forward': {
        'performance': {
            'next_1': 'forward/ratings/best_model_Rating-F1_LinearRegression_13f.pkl',
            'next_2': 'forward/ratings/best_model_Rating-F2_LinearRegression_13f.pkl',
            'next_3': 'forward/ratings/best_model_Rating-F3_LinearRegression_8f.pkl',
            'next_5': 'forward/ratings/best_model_Rating-F5_LinearRegression_8f.pkl',
        },
        'goals': {
            'next_1': 'forward/goals/best_model_Goals-F1_LinearRegression_5f.pkl',
            'next_2': 'forward/goals/best_model_Goals-F2_LinearRegression_5f.pkl',
            'next_3': 'forward/goals/best_model_Goals-F3_LinearRegression_5f.pkl',
            'next_5': 'forward/goals/best_model_Goals-F5_LinearRegression_5f.pkl',
        }
    }
}

MODELS = {}
for pos, metrics in MODEL_PATHS.items():
    MODELS[pos] = {}
    for metric, windows in metrics.items():
        MODELS[pos][metric] = {}
        for window, filename in windows.items():
            path = os.path.join(MODELS_DIR, filename)
            MODELS[pos][metric][window] = joblib.load(path)

def predict_performance_for_player(matches, position):
    """
    Usa los datos de get_last_match_data para predecir las 4 ventanas futuras.
    """
    windows = ['next_1', 'next_2', 'next_3', 'next_5']

    if position == 'goalkeeper':
        extra_metric = 'saves'
    elif position == 'defender':
        extra_metric = 'recoveries'
    elif position == 'midfielder':
        extra_metric = 'key_passes'
    elif position == 'forward':
        extra_metric = 'goals'
    else:
        extra_metric = None

    features_dict = get_last_match_data(matches)
    if features_dict is None:
        return {
            "windows": windows,
            "performance": [None]*4,
            "extra": [None]*4
        }

    performance = []
    extra = []
    for w in windows:
        perf_model = MODELS[position]['performance'][w]
        extra_model = MODELS[position][extra_metric][w]
        perf_features = perf_model.feature_names_in_
        extra_features = extra_model.feature_names_in_
        X_perf = np.array([features_dict.get(f, 0) for f in perf_features]).reshape(1, -1)
        X_extra = np.array([features_dict.get(f, 0) for f in extra_features]).reshape(1, -1)

        if np.all(X_perf == 0):
            perf_pred = 0.0
        else:
            perf_pred = perf_model.predict(X_perf)[0]

        if np.all(X_extra == 0):
            extra_pred = 0.0
        else:
            extra_pred = extra_model.predict(X_extra)[0]

        performance.append(round(float(perf_pred), 2))
        extra.append(round(float(extra_pred), 2))
    return {
        "windows": windows,
        "performance": performance,
        "extra": extra
    }

MODELS = {}
for pos, metrics in MODEL_PATHS.items():
    MODELS[pos] = {}
    for metric, windows in metrics.items():
        MODELS[pos][metric] = {}
        for window, filename in windows.items():
            path = os.path.join(MODELS_DIR, filename)
            MODELS[pos][metric][window] = joblib.load(path)