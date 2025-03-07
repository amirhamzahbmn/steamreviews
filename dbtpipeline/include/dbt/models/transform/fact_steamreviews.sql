-- dim_steamreviews.sql

select
    safe_cast(recommendationid as string) recommendation_id
    ,safe_cast(steam_appid as string) steam_appid
    ,safe_cast(language as string) language
    ,safe_cast(review as string) review
    ,safe_cast(timestamp_seconds(safe_cast(timestamp_created as int64)) as datetime) timestamp_created
    ,safe_cast(timestamp_seconds(safe_cast(timestamp_updated as int64)) as datetime) timestamp_updated
    ,safe_cast(voted_up as bool) voted_up
    ,safe_cast(votes_up as int64) votes_up
    ,safe_cast(votes_funny as int64) votes_funny
    ,safe_cast(steam_purchase as bool) steam_purchase
    ,safe_cast(received_for_free as bool) received_for_free
    ,safe_cast(written_during_early_access as bool) written_during_early_access
    ,safe_cast(author_steamid as string) author_steamid
    ,safe_cast(author_num_games_owned as int64) author_num_games_owned
    ,safe_cast(author_num_reviews as int64) author_num_reviews
    ,safe_cast(author_playtime_forever as int64) author_playtime_forever
    ,safe_cast(author_playtime_last_two_weeks as int64) author_playtime_last_two_weeks
    ,safe_cast(author_playtime_at_review as int64) author_playtime_at_review
    ,safe_cast(timestamp_seconds(safe_cast(author_last_played as int64)) as datetime) author_last_played
from {{ source('steam_reviews', 'raw_steam_reviews')}}