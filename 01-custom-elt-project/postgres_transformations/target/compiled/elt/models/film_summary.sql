select
    f.film_id,
    f.title,
    f.release_date,
    f.rating,
    f.user_rating,
    f.price,
    string_agg(distinct c.category_name, ', ') as categories,
    string_agg(distinct a.actor_name, ', ') as actors
from "destination_db"."public"."films" f
left join "destination_db"."public"."film_category" c on c.film_id = f.film_id
left join "destination_db"."public"."film_actors" fa on fa.film_id = f.film_id
left join "destination_db"."public"."actors" a on a.actor_id = fa.actor_id
group by 1, 2, 3, 4, 5, 6