USE production;
CREATE TABLE IF NOT EXISTS productsdata AS
SELECT products.product_id,products.product_name,categories.category_id,categories.category_name,brands.brand_id,brands.brand_name
FROM products 
INNER JOIN categories ON products.category_id = categories.category_id  
INNER JOIN brands ON products.brand_id = brands.brand_id ORDER BY products.product_id;
ALTER TABLE productsdata ADD PRIMARY KEY (product_id);
ALTER TABLE productsdata CHANGE product_id product_id INT AUTO_INCREMENT;
ALTER TABLE productsdata ADD FOREIGN KEY (category_id) REFERENCES production.categories(category_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE productsdata ADD FOREIGN KEY (brand_id) REFERENCES production.brands(brand_id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE productsdata ADD FOREIGN KEY (product_id) REFERENCES production.products(product_id) ON DELETE CASCADE ON UPDATE CASCADE
