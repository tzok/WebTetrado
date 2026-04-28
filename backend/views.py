from time import sleep
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from backend.request_handler.result_request import get_result_action
from backend.request_handler.request_setter import set_user_request_action
from backend.file_processor.form_file_handler import handle_uploaded_file
from backend.models import TetradoRequest
from asgiref.sync import sync_to_async
from django.views.decorators.http import require_POST
from django.shortcuts import render
import json
import requests
from backend.web_push.subscription_handler import (
    save_notification_subscription_action,
    link_notification_to_task_action,
)
from WebTetrado.settings import FRONTEND_LOCATION, WEBTETRADO_BACKEND_URL


@csrf_exempt
def set_user_request_endpoint(request):
    return set_user_request_action(json.loads(request.body.decode("utf-8")))


@csrf_exempt
def file_handler_endpoint(request):
    if request.FILES["structure"]:
        return HttpResponse(
            status=200,
            content=bytes(
                '{"id": "%s", "models": %d,"error":"%s"}'
                % (handle_uploaded_file(request.FILES["structure"])),
                "UTF-8",
            ),
            content_type="application/json",
        )
    return HttpResponse(status=500)


def user_request_result_endpoint(request, order_id):
    return HttpResponse(
        status=200,
        content=bytes(get_result_action(order_id), "UTF-8"),
        content_type="application/json",
    )


def analyzers_endpoint(request):
    response = requests.get(WEBTETRADO_BACKEND_URL + "/v1/analyzers", timeout=30)
    return HttpResponse(
        status=response.status_code,
        content=response.content,
        content_type="application/json",
    )


@sync_to_async
def get_request_status(hash_id):
    return TetradoRequest.objects.get(hash_id=hash_id)


async def websocket_endpoint(socket):
    await socket.accept()
    try:
        while True:
            hash_id = await socket.receive_text()
            try:
                status = str((await get_request_status(hash_id)).status)
            except Exception:
                await socket.send_text("0")
                await socket.close()
                break
            await socket.send_text(status)
            if status == "5" or status == "4":
                await socket.close()
                break
            sleep(2)
    except AssertionError:
        pass


def link_notification_to_task_endpoint(request):
    try:
        return HttpResponse(
            status=(
                200
                if link_notification_to_task_action(
                    json.loads(request.body.decode("utf-8"))
                )
                else 400
            )
        )
    except ValueError:
        return HttpResponse(status=400)


@require_POST
def save_notification_subscription_endpoint(request):
    try:
        status, response = save_notification_subscription_action(
            json.loads(request.body.decode("utf-8")), request.headers["user-agent"]
        )
        return HttpResponse(status=status, content=response)
    except ValueError:
        return HttpResponse(status=400)


@ensure_csrf_cookie
def index(request):
    try:
        with open(FRONTEND_LOCATION) as react_frontend:
            return HttpResponse(content=bytes(react_frontend.read(), "UTF-8"))
    except FileNotFoundError:
        return render(request, "server_starting.html")
