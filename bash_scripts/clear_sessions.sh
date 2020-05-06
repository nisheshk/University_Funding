#Clear all the expired sessions. This runs as a cron job every once in a day.
cd ../uni_gofundme && python manage.py clearsessions
