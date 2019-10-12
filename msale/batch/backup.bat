SET path=%1
SET PGPASSWORD=postgresdb_mysale
pg_dump -U postgres_mysale mysale > %path%