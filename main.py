import pydantic
from datetime import datetime
from fastapi import FastAPI, exceptions
from starlette.middleware.cors import CORSMiddleware
import mongoengine


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongoengine.connect('store')


class RecordDocument(mongoengine.Document):
    data = mongoengine.DictField()
    created_at = mongoengine.DateTimeField()


class Record(pydantic.BaseModel):
    data: dict


def insert_record(data) -> str:
    record = RecordDocument(data=data, created_at=datetime.now()).save()
    return str(record.id)


@app.post("/")
async def index(record: Record):
    id = insert_record(record.data)
    return {"id": id}


@app.get("/{id}")
async def retrieve(id: str):
    try:
        record = RecordDocument.objects.get(id=id)
    except RecordDocument.DoesNotExist:
        raise exceptions.HTTPException(status_code=404)
    except mongoengine.errors.ValidationError:
        raise exceptions.HTTPException(status_code=400)
    return record.data
