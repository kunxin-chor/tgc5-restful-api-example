# Sample movies API documentation

The base URL for all the applications call is: `https://ckx-movies-api.herokuapp.com/`

## Get all movies
```
GET /movies 
```
Return all the movies in the JSON format.

## Display one movie
```
GET /movie/<movie_id>
```

Display the information for one movie

## Add new movie
```
POST /movie/create
```
Create a new movie. Possible fields in the body are:

* title: The title of the movie
* plot: The plot of the movie

## Update a movie
```
PATCH /movie/<movie_id>
```

Update a movie. The URL params `movie_id` is the ID of the movie to update.

Possible fields in the body are:

* title: The title of the movie
* plot: The plot of the movie

## Delete a movie
```
DELETE /movie/<movie_id>
```

Delete the movie with the specified ID.
