# flask_shortener
Flask URL shortener

Creating a URL shortener with Flask and Redis. 

##Overview
- User inputs URL into form
- store URL into Redis, with assigned key
- encode key into base 62, return that as unique short identifier
- attached encoded identifier to the URL
- when short URL given, grab from Redis 
