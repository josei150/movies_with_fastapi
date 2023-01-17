from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

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

class User(BaseModel):
    email: str
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "email": "jose@gmail.com",
                "password": "2150jose"
            }
        }

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "jose@gmail.com":
            raise HTTPException(status_code=403, detail="Error: Credenciales inválidas")

class Response_movie(BaseModel):
    message: str
    data: Optional[Movie]


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

#Login user
@app.post("/login", tags=["Auth"], status_code=200)
def login(user: User):
    if user.email == "jose@gmail.com" and user.password == "2150jose":
        token: str = create_token(user.dict())
        return JSONResponse(content=token, status_code=200)
    return JSONResponse(content={"Error": "Email o contraseña incorrecta"}, status_code=403)

#Respondiendo con HTML
@app.get("/contact", tags=["Contact"])
def contact():
    return HTMLResponse("""
        <h1>Contacto</h1>
        <p> Yo seré la página de contacto </p>
    """)

#Metodo GET
@app.get("/movies", tags=["Movies"], response_model = List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

#Usando paths
@app.get("/movies/{id}", tags=["Movies"], response_model = Movie, status_code=200)
def get_movie(id: int = Path(le=2000, gt=0)) -> Movie:
    finded_movie = list(filter(lambda mov: mov["id"] == id, movies))
    return JSONResponse(content={"Error": "No se encontró la película"}, status_code=404) if not finded_movie else JSONResponse(content=finded_movie[0], status_code=200)

#Usando querys
@app.get("/movies/", tags=["Movies"], response_model = List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length = 3, max_length = 30)) -> List[Movie]:
    finded_movie = list(filter(lambda mov: mov["category"] == category, movies))
    return JSONResponse(content={"Error": "No existe esa categoría"}, status_code=404) if not finded_movie else JSONResponse(content=finded_movie, status_code=200)

#Usando POST
@app.post("/movies", tags=["Movies"], response_model = Response_movie, status_code=201)
def set_movie(movie: Movie = Body()) -> Response_movie:
    finded_movie = list(filter(lambda mov: mov["id"] == movie.id, movies))
    
    if finded_movie:
        return JSONResponse(content={"Error": "Ya existe la película"}, status_code=409)
    
    movies.append({
        'id': movie.id,
        'title': movie.title,
        'overview': movie.overview,
        'year': movie.year,
        'rating': movie.rating,
        'category': movie.category
    })

    return JSONResponse(
        content = {
            "message":"Se ha agregado un nuevo registro",
            "data": movies[-1]
        }, 
        status_code=201
    )

#Usando PUT
@app.put("/movies/{id}", tags=["Movies"], response_model = dict, status_code=200)
def update_movie(id: int, movie: Movie = Body()) -> dict:
    for mov in movies:
        if mov["id"] == id:
            mov['title'] = movie.title
            mov['overview'] = movie.overview
            mov['year'] = movie.year
            mov['rating'] = movie.rating
            mov['category'] = movie.category
            return JSONResponse(
                content={
                    "message": "Se ha actualizado un registro",
                    "data": movies[id - 1]
                },
                status_code=200
            )
    
    return JSONResponse(content={"Error": "No existe la película"}, status_code=404)

#Usando DELETE
@app.delete("/movies/{id}", tags=["Movies"], response_model = dict, status_code=200)
def delete_movie(id: int) -> dict:
    for movie in movies:
        if movie["id"] == int(id):
            movie_deleted = movie
            movies.remove(movie)
            return JSONResponse(
                content={
                    "message": "Se ha eliminado un registro",
                    "data": movie_deleted
                }, status_code=200
            )

    return JSONResponse(content={"Error": "No existe la película"}, status_code=404)