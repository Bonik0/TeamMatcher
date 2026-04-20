if [ ! -d nt-reports ]; then
    mkdir nt-reports
fi


docker stop $(docker ps -a -q)
docker compose -f ./compose.yaml up -d
sleep 15s


docker compose run --rm migrations alembic downgrade base
docker compose run --rm migrations alembic upgrade head



echo "-------------------------------NT FOR EMAIL SERVICE-------------------------------"
locust -f ./backend/nt_tests/locustfile_email_service.py --headless -u 500 -r 1500 --run-time "$1" --processes 4 --host=http://localhost:8003 --csv=./nt-reports/email-service.csv




echo "-------------------------------NT FOR SEARCH SERVICE-------------------------------"
locust -f ./backend/nt_tests/locustfile_search_service.py --headless -u 1000 -r 2000 --run-time "$1" --processes 4 --host=http://localhost:8007 --csv=./nt-reports/search-service.csv



echo "-------------------------------NT FOR AUTH SERVICE-------------------------------"
locust -f ./backend/nt_tests/locustfile_auth_service.py --headless -u 1000 -r 2000 --run-time "$1" --processes 4 --host=http://localhost:8005 --csv=./nt-reports/auth-service.csv



echo "-------------------------------NT FOR PROJECT SERVICE-------------------------------"
locust -f ./backend/nt_tests/locustfile_project_service.py --headless -u 250 -r 1000 --run-time "$1" --processes 3 --host=http://localhost:8006  --csv=./nt-reports/project-service.csv


echo "-------------------------------NT FOR USER SERVICE-------------------------------"
locust -f backend/nt_tests/locustfile_user_service.py --headless -u 1000 -r 2000 --run-time "$1" --host=http://localhost:8008 --csv=./nt-reports/user-service.csv


docker compose run --rm migrations alembic downgrade base
docker compose run --rm migrations alembic upgrade head

