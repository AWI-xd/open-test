from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import uvicorn

app = FastAPI()

device_commands: Dict[str, str] = {
    "1": "",
}


class CommandRequest(BaseModel):
    command: str


@app.get("/check_command")
async def check_command(device_id: str):
    """
    Проверяет команды для указанного устройства.
    Ардуино будет опрашивать этот endpoint.
    """
    if device_id not in device_commands:
        raise HTTPException(status_code=404, detail="Device not found")

    command = device_commands[device_id]
    # Очищаем команду после чтения
    if command:
        device_commands[device_id] = ""
        print(device_commands[device_id])
        return {"command": command}
    return {"command": ""}


@app.post("/send_command/{device_id}")
async def send_command(device_id: str, request: CommandRequest):
    """
    Отправляет команду на указанное устройство.
    Используется администратором/клиентом для управления.
    """
    if device_id not in device_commands:
        raise HTTPException(status_code=404, detail="Device not found")

    valid_commands = ["SOL1_ON", "SOL2_ON", "SOL3_ON", "SOL4_ON"]  # Если надо увеличить кол-во солиноидов, то добавь с список этот
    if request.command not in valid_commands:
        raise HTTPException(status_code=400, detail="Invalid command")

    device_commands[device_id] = request.command
    return {"status": "success", "device": device_id, "command": request.command}


@app.get("/devices")
async def list_devices():
    """
    Возвращает список всех устройств и их текущие команды.
    """
    return device_commands


if __name__ == "__main__":
    uvicorn.run(app, port=80)