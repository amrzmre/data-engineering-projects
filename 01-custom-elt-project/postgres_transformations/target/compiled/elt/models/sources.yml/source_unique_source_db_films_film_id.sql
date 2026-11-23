
    
    

select
    film_id as unique_field,
    count(*) as n_records

from "destination_db"."public"."films"
where film_id is not null
group by film_id
having count(*) > 1


