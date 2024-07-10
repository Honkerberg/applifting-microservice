# Offers Microservice

#### TODO:
-[ ] Implement Alembic
-[ ] Make tests
## Setup

1. Create a virtual environment and activate it.
2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```
3. Set up your database and run migrations:
    ```sh
    alembic upgrade head
    ```
4. Start the FastAPI server:
    ```sh
    uvicorn app.main:app --reload
    ```

## Endpoints

- `POST /products/` - Create a new product.
- `GET /products/` - Get a list of products.
- `GET /products/{product_id}` - Get a specific product.
- `PUT /products/{product_id}` - Update a product.
- `DELETE /products/{product_id}` - Delete a product.
- `GET /products/{product_id}/offers/` - Get offers for a product.

## Running Tests

Run the tests using pytest:
```sh
pytest
```