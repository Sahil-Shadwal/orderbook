# Orderbook Project

This repository contains a backend orderbook implementation using Python (Flask) and a frontend (if present) using Node.js/TypeScript. The backend provides RESTful APIs for order management and orderbook state.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Sahil-Shadwal/orderbook.git
cd orderbook
```

### 2. Set Up Python Virtual Environment

Navigate to the backend directory and create a virtual environment:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Backend Server

```bash
python3 -m app.main
```

The backend server will start on `http://0.0.0.0:3000`.

## API Endpoints

### Create Order

-   **POST** `/api/v1/order`
-   Request JSON:
    ```json
    {
        "base_asset": "BTC",
        "quote_asset": "USD",
        "price": 50000,
        "quantity": 1.5,
        "side": "buy",
        "kind": "ioc" // optional
    }
    ```
-   Response JSON:
    ```json
    {
      "orderId": "...",
      "status": "accepted",
      "executedQty": 1.5,
      "fills": [ ... ]
    }
    ```

### Get Orderbook Snapshot

-   **GET** `/api/v1/orderbook`
-   Response JSON:
    ```json
    {
      "bids": [ ... ],
      "asks": [ ... ],
      "bids_by_price": { ... },
      "asks_by_price": { ... }
    }
    ```

## Project Structure

```
orderbook/
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── orderbook.py
│       ├── redis.py
│       ├── types.py
│       └── __pycache__/
└── .gitignore
```

## Development Notes

-   The backend uses Flask for API endpoints and a custom `OrderbookManager` for order logic.
-   All orderbook state is in-memory; persistence is not implemented by default.
-   For development, use the provided virtual environment and requirements file.
-   The code is modular and can be extended for additional asset pairs, order types, or persistence.

## Frontend (Optional)

If you have a frontend (Node.js/TypeScript):

-   See the frontend directory for setup instructions.
-   The backend API is compatible with typical REST clients.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License.

## Contact

For questions, open an issue or contact Sahil Shadwal via GitHub.
