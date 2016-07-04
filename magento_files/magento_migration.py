import argparse
import csv
import sqlite3

from collections import namedtuple


def remove_underscore(t):
    while t[0] == '_' and len(t) > 2:
        t = t[1:]
    if t == '_':
        return ''
    return t


def client_accounts(file_name, db_conn):
    with open(file_name, 'rb') as csv_file:
        client_reader = csv.reader(csv_file, delimiter=',', quotechar='"')

        is_header = True
        client = None
        last_date = None
        counter = 0
        print('Starting client accounts file')
        for row in client_reader:
            if is_header:
                client = namedtuple('Client', map(remove_underscore, row))
                is_header = False
                continue

            c = client(*row)

            db = db_conn.cursor()
            email = (c.email,)
            db.execute('SELECT id FROM store_client WHERE email=?', email)
            client_id = db.fetchone()

            if client_id is not None:
                print('\nDuplicate client line for {}, only last insert will be saved'.format(c.email))
                db = db_conn.cursor()
                db.execute("DELETE FROM store_client WHERE id=?", client_id)
                db_conn.commit()

            db = db_conn.cursor()
            db.execute(
                "INSERT INTO store_client "
                "(first_name, last_name, email, creation_date, gender, password_hash, password_salt) "
                "VALUES (?,?,?,?,?,?,?)",
                (c.firstname, c.lastname, c.email, c.created_at,
                 c.gender, c.password_hash.split(':')[0], c.password_hash.split(':')[1], )
            )
            db_conn.commit()
            counter += 1
            if last_date != c.created_at:
                last_date = c.created_at
                print('\r{}'.format(last_date)),

        print('\nFinished client accounts file, checking result :')
        db = db_conn.cursor()
        db.execute("SELECT COUNT(*) from store_client")
        db_count = db.fetchone()[0]
        print('{} lines in the file, {} rows in the database'.format(counter, db_count))
        if counter != db_count:
            print('Error processing client data, exiting.')
            exit()


def client_addresses(file_name, db_conn):
    with open(file_name, 'rb') as csv_file:
        address_reader = csv.reader(csv_file, delimiter=',', quotechar='"')

        is_header = True
        address = None
        last_date = None
        counter = 0
        count_skipped = 0
        print('Starting client accounts file')
        for row in address_reader:
            if is_header:
                address = namedtuple('Address', map(remove_underscore, row))
                is_header = False
                continue

            c = address(*row)

            db = db_conn.cursor()
            email = (c.email,)
            db.execute('SELECT id FROM store_client WHERE email=?', email)
            client_id = db.fetchone()

            if client_id is None:
                print('contact info but no matching email ({}), skipping'.format(c.email))
                count_skipped += 1
                continue

            client_id = client_id[0]

            db = db_conn.cursor()
            db.execute(
                "SELECT COUNT(*) from store_contactinfo WHERE "
                "city=? AND company=? AND country_id=? AND fax=? AND first_name=? AND last_name=? AND postcode=? AND "
                "region=? AND street=? AND telephone=? AND vat_id=? AND address_default_billing=? AND "
                "address_default_shipping=? AND client_id=?",
                (
                    c.city,
                    c.company,
                    c.country_id,
                    c.fax,
                    c.firstname,
                    c.lastname,
                    c.postcode,
                    c.region,
                    c.street,
                    c.telephone,
                    c.vat_id,
                    c.address_default_billing_,
                    c.address_default_shipping_,
                    client_id,
                )
            )
            exists = db.fetchone()

            if exists is not None and exists[0] != 0:
                print('duplicate address, skipping')
            else:
                db = db_conn.cursor()
                db.execute(
                    "INSERT INTO store_contactinfo "
                    "(city, company, country_id, fax, first_name, last_name, postcode, region, street, telephone, "
                    "vat_id, address_default_billing, address_default_shipping, client_id) "
                    "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (
                        c.city,
                        c.company,
                        c.country_id,
                        c.fax,
                        c.firstname,
                        c.lastname,
                        c.postcode,
                        c.region,
                        c.street,
                        c.telephone,
                        c.vat_id,
                        c.address_default_billing_,
                        c.address_default_shipping_,
                        client_id,
                    )
                )
                db_conn.commit()

            counter += 1

            if last_date != c.vat_request_date:
                last_date = c.vat_request_date
                print('\r{}'.format(last_date)),

        print('\nFinished client addresses file, checking result :')
        db = db_conn.cursor()
        db.execute("SELECT COUNT(*) from store_contactinfo")
        db_count = db.fetchone()[0]
        print('{} lines in the file (and {} skipped), {} rows in the database'.format(counter, count_skipped, db_count))


def products(file_name, db_conn):
    with open(file_name, 'rb') as csv_file:
        product_reader = csv.reader(csv_file, delimiter=',', quotechar='"')

        is_header = True
        product = None
        last_date = None
        product_counter = 0
        picture_counter = 0
        warehouse_counter = 0
        stock_counter = 0
        print('Starting client accounts file')
        for row in product_reader:
            if is_header:
                product = namedtuple('Product', map(remove_underscore, row))
                is_header = False
                continue

            c = product(*row)

            # Saving product object
            db = db_conn.cursor()
            ref = (c.sku,)
            db.execute('SELECT id FROM store_product WHERE reference=?', ref)
            product_id = db.fetchone()

            if product_id is not None:
                print('\nDuplicate product line for {}, only last insert will be saved'.format(c.sku))
                db = db_conn.cursor()
                db.execute("DELETE FROM store_product WHERE reference=?", ref)
                db_conn.commit()

            db = db_conn.cursor()
            db.execute(
                "INSERT INTO store_product "
                "(reference, name, description, price, weight, tax_class_name, product_type, categories, "
                "product_online, creation_date) VALUES (?,?,?,?,?,?,?,?,?,?)",
                (
                    c.sku,
                    c.name,
                    c.description,
                    c.price,
                    c.weight,
                    c.tax_class_name,
                    c.product_type,
                    c.categories,
                    c.product_online,
                    c.created_at,
                )
            )

            db_conn.commit()
            product_counter += 1

            db = db_conn.cursor()
            ref = (c.sku,)
            db.execute('SELECT id FROM store_product WHERE reference=?', ref)
            product_id = db.fetchone()

            if product_id is None:
                print('\nCould not retrieve product id for {}, exiting.'.format(c.sku))
                exit()

            product_id = product_id[0]

            # Creating/fetching warehouse
            db = db_conn.cursor()
            warehouse = (c.product_websites,)
            db.execute('SELECT id FROM store_warehouse WHERE name=?', warehouse)
            warehouse_id = db.fetchone()

            if warehouse_id is None:
                db = db_conn.cursor()
                db.execute("INSERT INTO store_warehouse (name, description) VALUES (?,?)", (c.product_websites, '',))
                db_conn.commit()
                warehouse_counter += 1

                db.execute('SELECT id FROM store_warehouse WHERE name=?', warehouse)
                warehouse_id = db.fetchone()
                if warehouse_id is None:
                    print('\nCould not retrieve warehouse id for {}, exiting.'.format(c.product_websites))
                    exit()

            warehouse_id = warehouse_id[0]

            # Saving stock
            db = db_conn.cursor()
            ids = (product_id, warehouse_id,)
            db.execute('SELECT id FROM store_stock WHERE product_id=? AND warehouse_id=?', ids)
            stock_id = db.fetchone()

            if stock_id is not None:
                print('\nDuplicate stock line for {}, only last insert will be saved'.format(c.sku))
                db = db_conn.cursor()
                db.execute("DELETE FROM store_stock WHERE product_id=? AND warehouse_id=?", ids)
                db_conn.commit()

            db = db_conn.cursor()
            db.execute(
                "INSERT INTO store_stock (product_count, product_id, warehouse_id) "
                "VALUES (?,?,?)", (c.qty, product_id, warehouse_id,)
            )
            db_conn.commit()
            stock_counter += 1

            # Saving pictures
            if c.base_image:
                db = db_conn.cursor()
                db.execute(
                    "INSERT INTO store_productpicture (picture_url, picture_type, product_id) "
                    "VALUES (?,?,?)", (c.base_image, 'base', product_id,)
                )
                db_conn.commit()
                picture_counter += 1

            if c.small_image:
                db = db_conn.cursor()
                db.execute(
                    "INSERT INTO store_productpicture (picture_url, picture_type, product_id) "
                    "VALUES (?,?,?)", (c.base_image, 'small', product_id,)
                )
                db_conn.commit()
                picture_counter += 1

            if c.thumbnail_image:
                db = db_conn.cursor()
                db.execute(
                    "INSERT INTO store_productpicture (picture_url, picture_type, product_id) "
                    "VALUES (?,?,?)", (c.base_image, 'thumbnail', product_id,)
                )
                db_conn.commit()
                picture_counter += 1

            if c.swatch_image:
                db = db_conn.cursor()
                db.execute(
                    "INSERT INTO store_productpicture (picture_url, picture_type, product_id) "
                    "VALUES (?,?,?)", (c.base_image, 'swatch', product_id,)
                )
                db_conn.commit()
                picture_counter += 1

            if last_date != c.created_at:
                last_date = c.created_at
                print('\r{}'.format(last_date)),

        print('\nFinished product file, checking result :')
        db = db_conn.cursor()
        db.execute("SELECT COUNT(*) from store_product")
        db_product_counter = db.fetchone()[0]
        db = db_conn.cursor()
        db.execute("SELECT COUNT(*) from store_warehouse")
        db_warehouse_counter = db.fetchone()[0]
        db = db_conn.cursor()
        db.execute("SELECT COUNT(*) from store_stock")
        db_stock_counter = db.fetchone()[0]
        db = db_conn.cursor()
        db.execute("SELECT COUNT(*) from store_productpicture")
        db_picture_counter = db.fetchone()[0]
        print('product: {} lines in the file, {} rows in the database'.format(product_counter, db_product_counter))
        print('warehouse: {} found in the file, {} rows in the database'.format(warehouse_counter, db_warehouse_counter))
        print('stock count: {} found in the file, {} rows in the database'.format(stock_counter, db_stock_counter))
        print('pictures: {} found in the file, {} rows in the database'.format(picture_counter, db_picture_counter))


def parse_args():
    """
    Parse all arguments passed to this program
    """
    parser = argparse.ArgumentParser(
            description="Loads Magento exported data to Django db"
    )

    parser.add_argument("--client", dest="client", help="The client information file (mandatory, emails are unique)",
                        default=None)

    parser.add_argument("--adress", dest="adress", help="The client adress information file (mandatory)",
                        default=None)

    parser.add_argument("--product", dest="product", help="The product information file (mandatory)",
                        default=None)

    parser.add_argument("--date", dest="date", help="Minimal creation date (optional)",
                        default=None)

    parser.add_argument("--db", dest="db", help="database file (mandatory)",
                        default=None)

    arguments = parser.parse_args()

    if not arguments.client or not arguments.adress or not arguments.product or not arguments.db:
        print('Missing argument, use -h to print help')
        exit()

    return arguments

# main
args = parse_args()
conn = sqlite3.connect(args.db)

client_accounts(args.client, conn)
client_addresses(args.adress, conn)
products(args.product, conn)

conn.close()
