import product_api
import brand_api
import category_api
from app import app


@app.route("/")
def main_page():
    return "<center><h1>*** API making in almost DONE ***</h1></center>"

app.run(debug=True)