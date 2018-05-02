
**Backup Fixtures**

`python manage.py dumpdata products.Product --format json --indent 4 > products/fixtures/products.json`


**Load Fixtures**

`python manage.py loaddata products/fixtures/products.json`