SELECT (@row_number:=@row_number + 1) AS "#", entity, service, fn
FROM  anflerdb.jobs_services, (SELECT @row_number:=0) AS t
ORDER BY entity, service, fn
