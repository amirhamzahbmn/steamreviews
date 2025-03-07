
  
    

    create or replace table `steam-reviews-zc`.`steam_reviews`.`dim_steamreviews`
    
    
    OPTIONS()
    as (
      -- dim_steamreviews.sql

select
    recommendationid recommendation_id
    ,language
    ,review
    ,safe_cast(timestamp_seconds(safe_cast(timestamp_created as int64)) as datetime) timestamp_created
    ,safe_cast(timestamp_seconds(safe_cast(timestamp_updated as int64)) as datetime) timestamp_updated
    ,voted_up
    ,votes_up
    ,votes_funny
from `steam-reviews-zc`.`steam_reviews`.`raw_steam_reviews`
    );
  