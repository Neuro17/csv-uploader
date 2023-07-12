from arq.connections import RedisSettings
import sqlite3
import csv
from io import StringIO
from query import insert_product, get_last_id, update_task

SETTINGS = RedisSettings(host='localhost', port=6379)

async def upload_csv(ctx, file_content, task_id):
    csv_file = StringIO(file_content)
    csv_reader = csv.reader(csv_file)
    
    header = next(csv_reader)
    
    udpated_rows = 0
    created_rows = 0
    rows_with_errors = []
    last_id = get_last_id() or 0

    print(f'task_id is: {task_id}')

    for i, row in enumerate(csv_reader):
        id_ = row[0]
        product_name = row[1]
        price = row[2]

        if not product_name or not price:
            print('found malformed row')
            rows_with_errors.append(','.join(row))
            continue
        try:
            float(price)
        except Exception as e:
            print(e)
            print('found malformed row')
            rows_with_errors.append(','.join(row))
            continue

        if not id_:
            print('ID not found, generating one')
            last_id += 1
            id_ = last_id
            created_rows +=1
        else:
            udpated_rows += 1
            last_id = max(last_id, int(id_))

        
        new_product = {
            'id': id_,
            'name': product_name,
            'price': float(price)
        }
        try:
            insert_product(new_product)
        except Exception as e:
            print(e)
            rows_with_errors.append(','.join(row))

        if i % 25 == 0:
            print('updating task info')
            task_info = dict(
                id=task_id,
                records_updated=udpated_rows,
                records_created=created_rows,
                is_completed=False,
                rows_with_errors='|'.join(rows_with_errors)
            )
            update_task(task_info)
    
    # update with the remaining rows
    task_info = dict(
        id=task_id,
        records_updated=udpated_rows,
        records_created=created_rows,
        is_completed=True,
        rows_with_errors='|'.join(rows_with_errors)
    )
    update_task(task_info)

    return {'message': 'CSV file uploaded and processed successfully'}

async def test(ctx):
    print('worker is up and running')

FUNCTIONS = [upload_csv, test]

class WorkerSettings:
    '''
    Settings for the ARQ worker.
    '''
    redis_settings = SETTINGS
    functions: list = FUNCTIONS
