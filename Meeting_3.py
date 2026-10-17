movie = {
    'title' : 'Jumanji : The Next Level',
    'year' : 2017,
    'genre' : 'Adventure'
}

print(movie['title'])

movie.update({'viewers' : 44324578})
movie["genre"] = "Adventure/Comedy"
del movie['year']

print(movie)

Games = {
    'title' : 'Call of Duty',
    'genre' : 'Action',
    'year' : 2019,
    'platform' : 'PC'
}

print(Games.get('title'))

print(Games.keys())
print(Games.values())

Games.update({'publisher' : 'Activision'})

print(Games)

games_copy = Games.copy()

print(games_copy)

games_copy.pop('platform')
print(games_copy)

games_copy.popitem()
print(games_copy)

games_copy.clear()
print(games_copy)


"""
Problem 1!
"""

birth_day = {
    "John" : "2003-01-01",
    "David" : "2005-03-02",
    "Maria" : "2002-05-01",
    "Peter" : "2001-01-01",
}
print(birth_day)

birth_day["David"] = "2004-03-02"
birth_day.update({"Jessica": "2003-09-14"})
del birth_day["Maria"]
print(birth_day)

"""
Problem 2!
"""

Fruits_Prices = {
    'banana' : 1,
    'grapes' : 2,
    'apple' : 2.4,
    'milk' : 5,
}

print(Fruits_Prices)

print(Fruits_Prices.get('banana')*2 + Fruits_Prices.get('apple')*3)

Fruits_Prices.update({'Chocolate' : 7})

"""
Practice!
"""

songs = [
    {
        "title" : "Happy",
        "genre" : "Pop",
        "year" : 2013,
        "artist" : "Pharrell Williams",
        "songwriter" : [
            "Pharrell Williams",
            "Robin Thicke",
        ],
    }, {
        "title" : "Rolling in the Deep",
        "genre" : "Pop",
        "year" : 2010,
        "artist" : "Adele",
        "songwriter" : [
            "Adele Adkins",
            "Paul Epworth",
        ],
    }, {
        "title" : "Blank Space",
        "genre" : "Pop",
        "year" : 2014,
        "artist" : "Taylor Swift",
        "songwriter" : [
            "Taylor Swift",
            "Max Martin",
        ],
    }
]

print(
    songs[0]["title"]
    + " by "
    + songs[0]["artist"]
    + " is written by "
    + songs[0]["songwriter"][0]
    + " and "
    + songs[0]["songwriter"][1]
)

songs.append(
    {
        "title" : "Somebody That I Used to Know",
        "genre" : "Pop",
        "year" : 2011,
        "artist" : "Gotye",
        "songwriter" : [
            "Gotye",
            "Kimbra",
        ],
    }
)
print(songs[3])

"""
Practice 2!
"""

import random

# List of dictionaries representing movies
movies = [
    {
        "title": "The Shawshank Redemption",
        "genre": "Drama",
        "year": 1994,
        "director": "Frank Darabont",
        "rating": 9.3,
    },
    {
        "title": "The Godfather",
        "genre": "Crime",
        "year": 1972,
        "director": "Francis Ford Coppola",
        "rating": 9.2,
    },
    {
        "title": "The Dark Knight",
        "genre": "Action",
        "year": 2008,
        "director": "Christopher Nolan",
        "rating": 9.0,
    },
    {
        "title": "Pulp Fiction",
        "genre": "Crime",
        "year": 1994,
        "director": "Quentin Tarantino",
        "rating": 8.9,
    },
    {
        "title": "Forrest Gump",
        "genre": "Drama",
        "year": 1994,
        "director": "Robert Zemeckis",
        "rating": 8.8,
    },
]

new_movie = {
    "title": input("Enter the title of the movie: "),
    "genre": input("Enter the genre of the movie: "),
    "year": int(input("Enter the year of the movie: ")),
    "director": input("Enter the director of the movie: "),
    "rating": float(input("Enter the rating of the movie: ")),
}

movies.append(new_movie)

# Get a random movie recommendation
random_movie = random.choice(movies)

# Print the recommended movie with all properties
print("Recommended Movie:")
print("Title:", random_movie["title"])
print("Genre:", random_movie["genre"])
print("Year:", random_movie["year"])
print("Director:", random_movie["director"])
print("Rating:", random_movie["rating"])
