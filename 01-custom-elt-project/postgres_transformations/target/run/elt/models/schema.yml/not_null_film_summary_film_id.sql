
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select film_id
from "destination_db"."analytics"."film_summary"
where film_id is null



  
  
      
    ) dbt_internal_test