# Receipt Points Calculator

This service calculates points based on receipt data provided by users. Points are awarded based on retailer name, total amount, items, purchase date, and purchase time.

## Features

- Process receipts and generate unique IDs
- Retrieve points based on receipt data

## Setup Instructions

### Prerequisites

- Python 3.9+
- Flask

### Installation

1. Clone the repository:
    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2. Run the application:
    ```bash
    python app.py
    ```

The application will start on `http://127.0.0.1:5000`.

## API Endpoints

### Process Receipt

- **URL:** `/receipts/process`
- **Method:** `POST`
- **Request Body:** JSON containing receipt data with fields: `retailer`, `total`, `items`, `purchaseDate`, `purchaseTime`.
- **Response:** JSON with `id` (unique receipt ID).

### Get Points

- **URL:** `/receipts/<receipt_id>/points`
- **Method:** `GET`
- **Response:** JSON with `points` (total points for the receipt).

## Testing

To test, use the provided sample data, or customize receipts to validate each points rule.
