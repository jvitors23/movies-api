# Movies API

Django application for managing movies stored on an external data provider service.

## Running the project (Docker)

Most of the project configuration comes from environment variables, see ``local.env`` file. You can run the project by executing:

```
   docker compose up
```

Tested with:

  - Docker version 27.5.1, build ed223bc

The application will be available on [http://localhost:8000/](http://localhost:8000/)

## Running tests

To run tests, use:

```
 docker compose exec -it app bash -c "pytest movies_api/apps --cov ."
```

A coverage report will be displayed (only few tests for the authentication endpoints were done):

![test report](/assets/test-report.jpeg)

## API docs

Swagger api docs are available on [http://localhost:8001/api/schema/swagger-ui/](http://localhost:8001/api/schema/swagger-ui/) application will be available on [localhost:8000](http://localhost:8000/)

![API docs](/assets/api.png)

## Application details

The django application has 4 django apps:

- authentication: Auth endpoints for JWT authentication
  * POST ```/api/v1/auth/token/```: Takes a set of user credentials and returns an access and refresh JSON web token;
  * POST ```/api/v1/auth/refresh/```: Takes a refresh type JSON web token and returns an access type JSON web token;
  * POST ```/api/v1/auth/refresh/```: Takes a token and indicates if it is valid. This view provides no information about a token's fitness for a particular use;
- core: Responsible for core functionalities used by other apps. e.g BaseModel
- users: Users related stuff, such as custom user model and api endpoints for registering new user
  * POST ```/api/v1/users/register/```: Registers a new users;
- movies: API endpoints for interacting with external data provider for searching and voting on movies.
  * GET ```/api/v1/movies/```: Searches for movies matching a given query;
  * POST ```/api/v1/movies/ratings/```: Creates a new movie rating (either an Upvote or a Downvote);
  * GET ```/api/v1/movies/ratings/```: List rating of the logged-in user;
  * GET ```/api/v1/movies/ratings/<id>```: Retrieves a rating by id;
  * PUT ```/api/v1/movies/ratings/<id>```: Updates a rating by id (changes the rating type UPVOTE/DOWNVOTE);
  * PATCH ```/api/v1/movies/ratings/<id>```: Updates a rating by id (changes the rating type UPVOTE/DOWNVOTE);
  * DELETE ```/api/v1/movies/ratings/<id>```: Deletes a rating by id;


## External data provider - [November 7](https://november7-730026606190.europe-west1.run.app/docs#/)

In order to interact and get data from the external data provider, a Python client was generated using
[openapi-python-client](https://github.com/openapi-generators/openapi-python-client) library. This lib generates a
modern Python client from OpenAPI specification.

## Deployment strategy

The recommended deployment strategy for this application is based on containers, since the application is already dockerized.
A container based deployment of public cloud, like AWS or GCP, could be used.

I would also use components like Load Balancers and managed database services (to simplify backups and version upgrades). The following infrastructure
diagram exemplifies a possible deployment using AWS cloud:

![Infra](/assets/infra.png)

## Future improvements

Improvements I would've done if I had more time:

- Use of cache to avoid unnecessary requests to the external data provider - How to invalidate the cache would be a tricky part.
- Return the movie rating counter alongside with movies data (count of all upvotes and downvotes for a given movie)
- Implement more tests for all the endpoints
- Implement CI pipelines to build docker image, test and lint code

## Technologies

- [Python](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [Django](https://www.djangoproject.com/)
- [Django rest framework](https://www.django-rest-framework.org/)
- [Django rest framework SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- [Pytest](https://docs.pytest.org/en/8.2.x/)
- [Black](https://pypi.org/project/black/)
- [Poetry](https://python-poetry.org/)
- [openapi-python-client](https://github.com/openapi-generators/openapi-python-client)
