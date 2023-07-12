from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from arq import create_pool
from io import BytesIO
from query import get_all_data, insert_task, get_task_info, create_product_table, create_task_table

app = FastAPI()
pool = None  # Global variable to hold the Arq worker pool

origins = [
    "http://localhost",
    "http://localhost:8888",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    global pool
    pool = await create_pool()
    create_product_table()
    create_task_table()


@app.on_event("shutdown")
async def shutdown_event():
    global pool
    if pool:
        await pool.close()


@app.post("/upload")
async def upload_csv(file: UploadFile):
    file_data = await file.read()
    file_data = file_data.decode("utf-8")
    num_rows = len(file_data.split('\n'))
    # Pass the file data to the worker without writing it to disk
    task_id = insert_task({'name': file.filename, 'total_rows': num_rows})
    await pool.enqueue_job("upload_csv", file_data, task_id)

    return {"message": "CSV file upload started", 'task_id': task_id}

@app.get("/data")
async def get_data():
    data = get_all_data()

@app.get("/status/{id}")
async def get_data(id: int):
    print(id)
    task_info = get_task_info(id)
    return {'data': task_info}


@app.get("/test")
async def test():
    await pool.enqueue_job("test")
    return {"message": "Job queued"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8888, log_level="info")
