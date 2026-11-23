select
    f.film_id,
    f.title,
    f.release_date,
    f.rating,
    f.user_rating,
    f.price,
    string_agg(distinct c.category_name, ', ') as categories,
    string_agg(distinct a.actor_name, ', ') as actors
from {{ source('source_db', 'films') }} f
left join {{ source('source_db', 'film_category') }} c on c.film_id = f.film_id
left join {{ source('source_db', 'film_actors') }} fa on fa.film_id = f.film_id
left join {{ source('source_db', 'actors') }} a on a.actor_id = fa.actor_id
group by 1, 2, 3, 4, 5, 6