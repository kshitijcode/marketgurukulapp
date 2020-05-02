# marketgurukulapp
Stock Recommendation App


**This a Django based app which helps in recommendation for stocks based on the EMA cross over strategy.
The app also displays quotes and trend for over a period of time**.


The default Django sqlite3  configured as the database for this project. 


Django follows the MVT pattern. The same has been used along with few services as well.



# STEPS TO RUN THE PROJECT

```git clone git@github.com:kshitijcode/markegurukulapp.git

   docker build -t market-gurukul:v1 .
   
   docker run -e DJANGO_SECRET_KEY=YOUR_DJANGO_SECRET -e ALPHAVANTAGE_SECRET_KEY=YOUR_ALPHAVANTAGE_KEY -p 80:8000 market-   gurukul:v1 ```



That's it ! The web app would be up and running on localhost:8000


# TESTS


`python3 manage.py test `




# ASSMUPTIONS AND KNOWNS



1. I have considered the EMA CrossOver Strategy to detect trend for generating buy/sell recommendations.
2. The period of trend is considered last Closing. So if stock price is more than last closing price , it shows trend as POSITIVE.
3. I have used the AlphaVantage API Pythonic Wrapper to do things in pythonic way .
4. The web page takes about 10 seconds to load since it is generating the recommendation signals as well parsing the quotes. The AlphaVantage API through the python wrapper is considerably slow taking about 5-6 seconds to return a single API Request.
5. If recommendation engine is separated from quotes then it hardly takes any time for the page to load.
6. Currently I am using the default sqlite which comes with Django which does not need any credentials/authorization. Under ideal production scenarios we should setup a separate DB with credentials.
7. I have currently made the API unauthenticated since it had only one client(the frontend). Ideally, when developing API's we should be using authentication of any form.
8. We have models,services,forms all are under a single files each, but if the project is complex , it can be structure into individiual packages of services/models/forms etc.
9. Secret Keys are injected through environment variables , but in production we can have a secret server(AWS,Azure,Vault) and fetch the secrets.
10. SESSION_COOKIE_SECURE  and CSRF_COOKIE_SECURE is enabled to prevent CSRF Attacks.



