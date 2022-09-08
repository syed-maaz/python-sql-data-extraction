import sql_flask_connection
from sql_flask_connection import app    
import products
import categories
import brands

def main():
    app.run(debug=True)


    
if __name__=="__main__":
    main()
