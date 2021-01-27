# DeterminedApp

Web applicaiton for Capstone Class

Installation: 
1. Install Docker: https://docs.docker.com/get-docker/
1. Create a folder 'Capstone' where you want to host this application
1. Clone this github project into 'Capstone'
   1. Install git: https://git-scm.com/
   1. `git clone https://github.com/Josephkready/DeterminedApp.git`
1. Copy the contents of `./Capstone/DeterminedApp/deploy` to `./Capstone/`
1. Open a terminal and run `docker-compose up --build`
1. You can now access the website at http://localhost/
   1. To access the site outside of your localhost you must enable port forwarding
        1. Windows: https://docs.microsoft.com/en-us/sql/reporting-services/report-server/configure-a-firewall-for-report-server-access?view=sql-server-ver15#:~:text=To%20open%20port%2080,Click%20Inbound%20Rules.
        1. Linux: https://askubuntu.com/questions/646293/open-port-80-on-ubuntu-server

If you need to update the repository: 
1. Navigate to the 'Capstone/DeterminedApp' folder and open a terminal
2. Run `git pull`
2. Navigate to the 'Capstone' folder and open a terminal
2. Run `docker-compose up -d --build`
2. The updates should be applied and you can go back to using the application
