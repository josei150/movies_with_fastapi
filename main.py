from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse


app = FastAPI()

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Vengadores',
        'overview': "los heroes más poderosos del planeta tendrán que enfrentar su más grande amenaza ...",
        'year': '2019',
        'rating': 8.2,
        'category': 'Acción'    
    },
    {
        'id': 3,
        'title': 'Avatar: el último maestro aire',
        'overview': "Una mala adaptación de lo que fue una de las mejores series animadas de mi infancia ...",
        'year': '2009',
        'rating': 1.8,
        'category': 'Fantasía'    
    },
]

#Metodo GET
@app.get("/", tags=["Home"])
def gretting():
    return {"Saludo" : "Hola"}

#Respondiendo con HTML
@app.get("/contact", tags=["Contact"])
def contact():
    return HTMLResponse("""
        <h1>Contacto</h1>
        <p> Yo seré la página de contacto </p>
    """)

#Metodo GET
@app.get("/movies", tags=["Movies"])
def get_movies():
    return movies

#Usando paths
@app.get("/movies/{id}", tags=["Movies"])
def get_movie(id: int):
    finded_movie = list(filter(lambda mov: mov["id"] == id, movies))
    return "No se encontró la película" if not finded_movie else finded_movie[0]

#Usando querys
@app.get("/movies/", tags=["Movies"])
def get_movies_by_category(category: str):
    finded_movie = list(filter(lambda mov: mov["category"] == category, movies))
    return "No existe esa categoría" if not finded_movie else finded_movie

#Usando POST
@app.post("/movies", tags=["Movies"])
def set_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(),
    category: str = Body()):
    finded_movie = list(filter(lambda mov: mov["id"] == id, movies))
    
    if finded_movie:
        return "Error: Ya existe la película"
    
    movies.append({
        'id': id,
        'title': title,
        'overview': overview,
        'year': year,
        'rating': rating,
        'category': category
    })

    return movies

#Usando PUT
@app.put("/movies/{id}", tags=["Movies"])
def update_movie(id: int, title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), 
    category: str = Body()):
    for movie in movies:
        if movie["id"] == id:
            movie['title'] = title
            movie['overview'] = overview
            movie['year'] = year
            movie['rating'] = rating,
            movie['category'] = category
            return movies
    
    return "Error: No existe la película"

#Usando DELETE
@app.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int):
    for movie in movies:
        if movie["id"] == int(id):
            movies.remove(movie)
            return movies

    return "Error: No existe la película"