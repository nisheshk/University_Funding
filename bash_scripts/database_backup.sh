#Get current system date and time
a=$(date +%F);
b=$(date +%T);

#Concat date and time 
c="${a}_${b}";

#Create directory backups if does not exist
cd ~/ && mkdir -p backups

#Dump the database into the /backups directory.
#Ideally the dump should be stored in some other server.
#Note $PGPASSWORD is an environmental variable.
cd ~/backups/  && PGPASSWORD=$PGPASSWORD pg_dump -U postgres fundme_university_windsor > "backup_$c".bak

#Place this in a Crontab (crontab -e)
#01 00 * * * ~/database_backup.sh

