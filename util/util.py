import pandas as pd

from util.data import data_dir, file_check
from util.nba_stats import PlayByPlay, ShotChartDetail, TeamAdvancedGameLogs


def merge_shot_pbp_for_season(season, season_type='Regular Season', override_file=False):
    file_path = data_dir + 'merged_shot_pbp/' + season + '.csv'

    if override_file or not file_check(file_path):
        play_by_play_endpoint = PlayByPlay()
        shot_endpoint = ShotChartDetail()

        pbp_df = pd.DataFrame()
        log = TeamAdvancedGameLogs().get_data({'Season': season, 'SeasonType': season_type}, override_file=True)
        games = log.GAME_ID.unique()
        for g in games:
            if len(str(g)) < 10:
                g = '00' + str(g)
            pbp_df = pbp_df.append(
                play_by_play_endpoint.get_data({'GameID': g, 'Season': season, 'SeasonType': season_type}))

        pbp_df['GAME_ID'] = '00' + pbp_df['GAME_ID'].astype(str)
        shots_df = shot_endpoint.get_data({'Season': season, 'SeasonType': season_type}, override_file=True)
        merge_df = pd.merge(pbp_df, shots_df, left_on=['EVENTNUM', 'GAME_ID', 'PERIOD'],
                            right_on=['GAME_EVENT_ID', 'GAME_ID', 'PERIOD'])

        merge_df.to_csv(file_path)
        return merge_df
    else:
        return pd.read_csv(file_path)


def merge_shot_pbp_for_game(season, game_id, season_type='Regular Season', override_file=False):
    file_path = data_dir + 'merged_shot_pbp/' + season + '/' + game_id + '.csv'

    if override_file or not file_check(file_path):
        play_by_play_endpoint = PlayByPlay()
        shot_endpoint = ShotChartDetail()

        pbp_df = play_by_play_endpoint.get_data({'GameID': game_id, 'Season': season, 'SeasonType': season_type})

        pbp_df['GAME_ID'] = '00' + pbp_df['GAME_ID'].astype(str)

        shots_df = shot_endpoint.get_data({'Season': season, 'SeasonType': season_type})
        if len(shots_df[shots_df['GAME_ID'] == int(game_id)]) == 0:
            shots_df = shot_endpoint.get_data({'Season': season, 'SeasonType': season_type}, override_file=True)

        merge_df = pd.merge(pbp_df, shots_df, left_on=['EVENTNUM', 'GAME_ID', 'PERIOD'],
                            right_on=['GAME_EVENT_ID', 'GAME_ID', 'PERIOD'])

        merge_df.to_csv(file_path)
        return merge_df
    else:
        return pd.read_csv(file_path)
