select
    id,
    first_name,
    last_name,
    date_of_birth,
    date_part('year', age(date_of_birth))::int as age
from {{ source('source_db', 'users') }}