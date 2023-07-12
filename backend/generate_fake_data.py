import csv
import faker
import random

fake = faker.Faker()

# Generate the data for the CSV
data = []
id_set = set()

for id in range(100000):
    # Generate a unique ID
    while True:
        id_ = fake.random_int(min=1, max=110000)
        if id_ not in id_set:
            id_set.add(id_)
            break

    # Generate product name and price
    name = fake.random_element(elements=('Food', 'Beverage')) + ' ' + fake.word()

    price = round(random.uniform(1, 100), 2)
    
    if id_ in [13, 63, 5434, 8289, 444]:
        price = 'string instead of number'
    if id_ in [234, 2134, 3939]:
        price = ''
    if id_ in [9993, 12]:
        name = ''


    # Add the row to the data list
    data.append((id_, name, price))

# Write the data to a CSV file
filename = 'product_data.csv'
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['ID', 'name', 'price'])  # Write the header
    writer.writerows(data)  # Write the data rows

print(f"CSV file '{filename}' has been generated.")
