#If the server or database crashes then mey be postgresql needs to be installed again. May use docker for doing this.
#Following scripts recovers the database and maintains the intergrity of the system.

#Create a database used by the project
#Note that $PGPASSWORD is an environmental variable and in case the server changes.
#This has to be reconfigured. Better way of doing this would be to use docker. But due to time constraint, we could not use dockers.
PGPASSWORD=$PGPASSWORD psql -U postgres -c "DROP DATABASE IF EXISTS fundme_university_windsor";
PGPASSWORD=$PGPASSWORD psql -U postgres -c "CREATE DATABASE fundme_university_windsor";


#Go to the backup folder and fetch the latest backup file
cd ~/backups/ && a=$(ls -t1 |  head -n 1)

#User the latest backup file to restore the database.
cd ~/backups/ && PGPASSWORD=$PGPASSWORD psql -U postgres -d fundme_university_windsor -f "$a"
