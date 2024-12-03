from flask import Flask, request, Response
import requests

app = Flask(__name__)

# Service URLs (using Docker's DNS)
BOOK_SERVICE_URL = "http://book-service:5001"
REVIEW_SERVICE_URL = "http://review-service:5002"


def forward_request(url):
    print(f"Forwarding request to: {url}")  
    print(f"Method: {request.method}")
    print(f"Data: {request.get_data()}")

    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers={key: value for key, value in request.headers if key != "Host"},
            json=request.get_json() if request.is_json else None,
        )

        print(f"Response status: {resp.status_code}")  
        print(f"Response content: {resp.content}")

        return Response(resp.content, resp.status_code, resp.headers.items())
    except requests.RequestException as e:
        print(f"Error: {str(e)}")  
        return {"error": str(e)}, 500


@app.route("/api/books", methods=["GET", "POST"])
def books():
    url = f"{BOOK_SERVICE_URL}/api/books"
    return forward_request(url)


@app.route("/api/books/<int:book_id>", methods=["GET", "PUT", "DELETE"])
def book_by_id(book_id):
    url = f"{BOOK_SERVICE_URL}/api/books/{book_id}"
    return forward_request(url)


@app.route("/api/reviews", methods=["GET", "POST"])
def reviews():
    url = f"{REVIEW_SERVICE_URL}/api/reviews"
    return forward_request(url)


@app.route("/api/reviews/<int:book_id>", methods=["GET", "PUT", "DELETE"])
def review_by_id(book_id):
    url = f"{REVIEW_SERVICE_URL}/api/reviews/{book_id}"
    return forward_request(url)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
