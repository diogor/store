import uvicorn
import pydantic
from fastapi import FastAPI, exceptions
import mongoengine


app = FastAPI()
mongoengine.connect('store')


class RecordDocument(mongoengine.Document):
    data = mongoengine.DictField()


class Record(pydantic.BaseModel):
    data: dict


def insert_record(data) -> str:
    record = RecordDocument(data=data).save()
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
