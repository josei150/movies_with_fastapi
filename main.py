from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class Movie(BaseModel):
    id: Optional[int] | None = None
    title: str = Field(min_length = 3, max_length=30)
    overview: str = Field(min_length = 15, max_length = 80)
    year: int = Field(le = 2023, gt = 1900)
    rating: float = Field(le = 10, gt = 0)
    category: str = Field(min_length = 3, max_length = 30)

    #Esta clase sirve para configurar los valores por defecto del Schema
    class Config:
        schema_extra = {
            "example": {
                "id": 12,
                "title": "La película",
                "overview": "Transcurre en el año 2050 cuando los autos son capaces de volar...",
                "year": 2014,
                "rating": 8.7,
                "category": "Ciencia Ficción"
            }
        }

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
def get_movie(id: int = Path(le=2000, gt=0)):
    finded_movie = list(filter(lambda mov: mov["id"] == id, movies))
    return "No se encontró la película" if not finded_movie else finded_movie[0]

#Usando querys
@app.get("/movies/", tags=["Movies"])
def get_movies_by_category(category: str = Query(min_length = 3, max_length = 30)):
    finded_movie = list(filter(lambda mov: mov["category"] == category, movies))
    return "No existe esa categoría" if not finded_movie else finded_movie

#Usando POST
@app.post("/movies", tags=["Movies"])
def set_movie(movie: Movie = Body()):
    finded_movie = list(filter(lambda mov: mov["id"] == movie.id, movies))
    
    if finded_movie:
        return "Error: Ya existe la película"
    
    movies.append({
        'id': movie.id,
        'title': movie.title,
        'overview': movie.overview,
        'year': movie.year,
        'rating': movie.rating,
        'category': movie.category
    })

    return movies

#Usando PUT
@app.put("/movies/{id}", tags=["Movies"])
def update_movie(id: int, movie: Movie = Body()):
    for mov in movies:
        if mov["id"] == id:
            mov['title'] = movie.title
            mov['overview'] = movie.overview
            mov['year'] = movie.year
            mov['rating'] = movie.rating
            mov['category'] = movie.category
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