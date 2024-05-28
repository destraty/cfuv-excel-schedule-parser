import uvicorn
from fastapi import FastAPI, HTTPException

from schedule_parser.schedule_filler import schedule_handler, get_group_list
from schedule_parser.data_caching import *
from common import ROOT_DIR

teachers_in_json_file = f"{ROOT_DIR}/storage/teachers_in_json.json"
groups_in_json_file = f"{ROOT_DIR}/storage/groups_in_json.json"
groups_list_file = f"{ROOT_DIR}/storage/groups_list.json"

groups_in_json, teachers_in_json = {}, {}
groups_list = []

if check_file_age(teachers_in_json_file) and check_file_age(groups_in_json_file) and check_file_age(groups_list_file):
    print('loaded from model')
    teachers_in_json = load_data_from_file(teachers_in_json_file)
    groups_in_json = load_data_from_file(groups_in_json_file)
    groups_list = load_data_from_file(groups_list_file)

else:
    print('gen new')
    groups_in_json, teachers_in_json = schedule_handler()
    groups_list = get_group_list()
    save_data_to_file(teachers_in_json, teachers_in_json_file)
    save_data_to_file(groups_in_json, groups_in_json_file)
    save_data_to_file(groups_list, groups_list_file)

teachers_list = [teacher for teacher in teachers_in_json]

app = FastAPI()


@app.get("/api/groups_list", tags=["Группы"])
async def get_group_list() -> list[str]:
    return groups_list


@app.get("/api/", tags=["Группы"])
async def get_group_schedule(group: str = None) -> list[list[list[str]]]:
    if group is None:
        raise HTTPException(status_code=422, detail="Не передан параметр группы")
    elif group not in groups_in_json:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    else:
        return groups_in_json[group]


@app.get("/api/teacher/teacher_list", tags=["Преподаватели"])
async def get_teacher_list() -> list[str]:
    return teachers_list


@app.get("/api/teacher/", tags=["Преподаватели"])
async def get_teacher_schedule(teacher: str = None):
    if teacher is None:
        raise HTTPException(status_code=422, detail="Не передан параметр преподавателя")
    elif teacher not in teachers_in_json:
        raise HTTPException(status_code=404, detail="Преподаватель не найден")
    else:
        return teachers_in_json[teacher]


# Запуск сервера
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
