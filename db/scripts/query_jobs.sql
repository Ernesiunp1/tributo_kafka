SELECT (@row_number:=@row_number + 1) AS "#", job_id, msg_id, dt_created, dt_updated , user, fn, state as st, status as rc, kafka_key as kk, kafka_offset as ko, kafka_partition as kp,  errors
FROM  anflerdb.jobs, (SELECT @row_number:=0) AS t
ORDER BY dt_created, dt_updated;
