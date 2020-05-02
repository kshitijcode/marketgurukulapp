# markegurukulapp
Stock Recommendation App

**This a Django based app which helps in recommendation for stocks based on the EMA cross over strategy.
The app also displays quotes and trend for over a period of time**.

The default Django sqlite3  configured as the database for this project. 




STEPS TO RUN THE PROJECT : 

`git clone git@github.com:kshitijcode/markegurukulapp.git

 docker build -t market-gurukul:v1 .   
 docker run -e DJANGO_SECRET_KEY="(i^2#*goq_uj4aio#ndy5h@83225g#a" market-gurukul:v1 sh -c "python manage.py makemigrations && python manage.py migrate"
    
`

