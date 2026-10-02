favorite_movies =[
    {
        "name": "The Matrix I",
        "release_year": 1999,
        "sequels": ["The Matrix II", "The Matrix III", "The Matrix IV"]
    },
    {
        "name": "Star Wars IV",
        "release_year": 1977,
        "sequels": ["Star Wars V", "Star Wars VI", "Star Wars VII", "Star Wars VIII", "Star Wars IX"],
        "prequels": ["Star Wars I", "Star Wars II", "Star Wars III"]
    }
]


# print(favorite_movies)


# total_favorite_movies = len(favorite_movies)
# print("How many total favorite movies do we have?", total_favorite_movies)


# print(type(favorite_movies), type(favorite_movies[0]))


# print('Enter your favorite movie from the last year:')
# recent_favorite_movie = input()
# print('Your favorite movie from the last year is:', recent_favorite_movie)

#---------------------------------------------------------------------------------------------------

# Create a function that takes a movie as an argument. Inside the function, it should check if the movie was released before 2000. If it was, it should print a string that says “This movie was released before 2000”. If it wasn’t, it should print a string that says “This movie was released after 2000”. The function should only return the movie name if it was released after 2000.
# Below the function create an empty list called recent_movies.
# Outside and below the function and recent_movies, use a for loop to loop through all the movies in your list of favorite movies. For each movie, call the function and save its returned value in a variable. If that value is not None, append the returned movie name to the recent_movies list.
# Finally, outside of the loop, print out the recent_movies list.

# Assignment Code

#1.
def releasedBefore2000(movie):
    if movie["release_year"] <= 2000:
        return movie
    
    else:
        return None

#2.
recent_movies = []


#3.
for movie in favorite_movies:
    if releasedBefore2000(movie) != None:
        recent_movies.append(movie)

#4.
print(recent_movies)