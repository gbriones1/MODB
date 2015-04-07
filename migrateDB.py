import csv
import pdb

import sqlite3
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

codes = []
brands = []
providers = []
classifications = []
appliances = []
products = []

def get_object_id(name, objects, table):
    if not name in objects:
        cursor.execute('INSERT INTO database_'+table+' (`name`) VALUES ("'+name+'")')
        objects.append(name)
    cursor.execute('SELECT * FROM database_'+table+' WHERE name="'+name+'"')
    return cursor.fetchone()[0]

print "Parsing seed"
with open('seedDB.csv', 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        code = row['code'].strip()
        if code:
            storage = row['storage'].strip()
            amount = int(row['in'].strip()) if row['in'].strip() else 0
            tobe = int(row['tobe'].strip()) if row['tobe'].strip() else 0
            if code in codes:
                assignment = ''
                if storage == "Consignación":
                    assignment = 'in_consignment='+str(amount)+', consignment_tobe='+str(tobe)
                elif storage == "PROPIO":
                    assignment = 'in_stock='+str(amount)+', stock_tobe='+str(tobe)
                elif storage == "OBSOLETO":
                    assignment = 'in_used='+str(amount)+', used_tobe='+str(tobe)
                query = 'UPDATE database_product SET '+assignment+' WHERE code="'+code+'"'
                print query
                cursor.execute(query)
            else:
                codes.append(code)
                name = row['name'].strip()
                description = row['description'].strip().replace('"', ' pulg')
                provider_id = get_object_id(row['provider'].strip(), providers, "provider")
                brand_id = get_object_id(row['brand'].strip(), brands, "brand")
                appliance_id = get_object_id(row['appliance'].strip(), appliances, "appliance")
                classification_id = get_object_id(row['classification'].strip(), classifications, "classification")
                fields = '(`code`, `name`, `description`, `price`, `provider_id`, `classification_id`, `brand_id`, `in_consignment`, `in_stock`, `in_used`, `consignment_tobe`, `stock_tobe`, `used_tobe`)'
                values = '("'+code+'", "'+name+'", "'+description+'", 0, '+str(provider_id)+', '+str(classification_id)+', '+str(brand_id)+', '
                if storage == "Consignación":
                    values += str(amount)+', 0, 0, '+str(tobe)+', 0, 0'
                elif storage == "PROPIO":
                    values += '0, '+str(amount)+', 0, 0, '+str(tobe)+', 0'
                elif storage == "OBSOLETO":
                    values += '0, 0, '+str(amount)+', 0, 0, '+str(tobe)
                values += ')'
                query = 'INSERT INTO database_product '+fields+' VALUES '+values
                print query
                cursor.execute(query)
                query2 = 'INSERT INTO database_product_appliance (`product_id`, `appliance_id`) VALUES '+'("'+code+'", '+str(appliance_id)+')'
                print query2
                cursor.execute(query2)
    conn.commit()

pdb.set_trace()

conn.close()