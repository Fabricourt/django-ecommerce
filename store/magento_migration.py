import argparse
import csv
import sqlite3

from collections import namedtuple


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
                client = namedtuple('Client', row)
                is_header = False
                continue

            c = client(*row)

            db = db_conn.cursor()
            db.execute(
                "INSERT INTO store_client VALUES "
                "(%(first_name)s, %(last_name)s, %(email)s, %(creation_date)s,"
                " %(gender)s, %(password_hash)s, %(password_salt)s)" %
                {
                    'email': c.email,
                    'creation_date': c.created_at,
                    'first_name': c.firstname,
                    'gender': c.gender,
                    'last_name': c.lastname,
                    'password_hash': c.password_hash.split(':')[0],
                    'password_salt': c.password_hash.split(':')[1]
                }
            )
            db_conn.commit()
            counter += 1
            if last_date != c.created_at:
                last_date = c.created_at
                print('\r%s' % last_date),

        print('\nFinished client accounts file, checking result :')
        db = db_conn.cursor()
        db.execute("SELECT COUNT(*) from store_client")
        db_count = db.fetchone()
        print('%d lines in the file, %d rows in the database' % (counter, db_count))
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
                address = namedtuple('Address', row)
                is_header = False
                continue

            c = address(*row)

            db = db_conn.cursor()
            email = (c._email,)
            db.execute('SELECT id FROM store_client WHERE email=?', email)
            client_id = db.fetchone()

            if client_id is None:
                print('contact info but no matching email (%s), skipping' % c._email)
                count_skipped += 1
                continue

            db = db_conn.cursor()
            db.execute(
                "INSERT INTO store_contactinfo VALUES "
                "(%(city)s, %(company)s, %(country_id)s, %(fax)s, %(first_name)s, %(last_name)s, %(postcode)s, "
                "%(region)s, %(street)s, %(telephone)s, %(vat_id)s, %(address_default_billing)s, "
                "%(address_default_shipping)s, %(client_id)s)" %
                {
                    'city': c.city,
                    'company': c.company,
                    'country_id': c.country_id,
                    'fax': c.fax,
                    'first_name': c.firstname,
                    'last_name': c.lastname,
                    'postcode': c.postcode,
                    'region': c.region,
                    'street': c.street,
                    'telephone': c.telephone,
                    'vat_id': c.vat_id,
                    'address_default_billing': c._address_default_billing_,
                    'address_default_shipping': c._address_default_shipping_,
                    'client_id': client_id
                }
            )
            db_conn.commit()
            counter += 1

            if last_date != c.vat_request_date:
                last_date = c.vat_request_date
                print('\r%s' % last_date),

        print('\nFinished client addresses file, checking result :')
        db = db_conn.cursor()
        db.execute("SELECT COUNT(*) from store_contactinfo")
        db_count = db.fetchone()
        print('%d lines in the file (and %d skipped), %d rows in the database' % (counter, count_skipped, db_count))
        if counter != db_count:
            print('Error processing client addresses, exiting.')
            exit()


# TODO
def products(file_name, db_conn):
    pass


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

    parser.add_argument("--db", dest="db", help="database name (mandatory)",
                        default=None)

    args = parser.parse_args()

    if not args.client or not args.adress or not args.product or not args.db:
        print('Missing argument, use -h to print help')
        exit()

    return args

# main
args = parse_args()
conn = sqlite3.connect('example.db')

client_accounts(args.client, conn)
client_addresses(args.client, conn)
products(args.client, conn)

conn.close()
