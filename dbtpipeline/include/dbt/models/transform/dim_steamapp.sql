-- dim_steamapp.sql

select
    safe_cast(steam_appid as string) steam_appid
    ,safe_cast(name as string) name
    ,safe_cast(required_age as int64) required_age  
    ,safe_cast(is_free as bool) is_free
    ,safe_cast(detailed_description as string) detailed_description
    ,safe_cast(short_description as string) short_description
from {{ source('steam_reviews', 'raw_steamappdetails')}}