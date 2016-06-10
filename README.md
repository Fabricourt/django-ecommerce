# django-ecommerce
A simple ecommerce site in Django

This is a work in progress to create a simple ecommerce site.
Demo data will be included for selling goggles (hense the name of the project)

Instructions for installing will come soon, with a live demo.

For the moment, only the models are defined as to test migration scripts from other plateforms.
You can create the db.sqlite3 by running the command from the project root:
``` 
python manage.py makemigrations store && python manage.py migrate
```

To test the migration script, the best is to delete the db.sqlite3 file first and re-generate it
with the above command (not mandatory but you will get a lot of prints in the console for 
duplicate lines otherwise) and then launch from the project root:
```
python store/magento_migration.py --client magento_files/customer_20160607_181035.csv --adress magento_files/customer_address_20160602_165847.csv --product magento_files/catalog_product_20160602_165007.csv --db db.sqlite3
```
