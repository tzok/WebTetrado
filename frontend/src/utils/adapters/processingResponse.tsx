import { message } from "antd";
import { getCookie } from "../../components/CSRF";
import config from "../../config.json";
import fetch from "node-fetch";

function getWebSocketUrl() {
  if (config.SERVER_WEB_SOCKET_URL) {
    return config.SERVER_WEB_SOCKET_URL;
  }

  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  return `${protocol}//${window.location.host}/ws/`;
}

export function processingResponse(
  orderId: any,
  setResultSet: any,
  result: any,
  setLoading: any
) {
  const requestOptions = {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "X-CSRFToken": getCookie(),
    },
  };
  let socket = new WebSocket(getWebSocketUrl());
  let timer: any = null;

  socket.onopen = () => {
    socket.send(orderId);
    timer = setInterval(() => {
      socket.send(orderId);
    }, 5000);
  };
  socket.onmessage = (event) => {
    if (event.data === "5" || event.data === "4") {
      clearInterval(timer);
      fetch(
        config.SERVER_URL + "/api/process/result/" + orderId,
        requestOptions
      )
        .then((response: any) => response.json())
        .then((response: any) => {
          setResultSet(response);
          setLoading(false);
          socket.close();
        })
        .catch((error: any) => {
          message.error("Processing error");
          clearInterval(timer);
          socket.close();
        });
    } else {
      setResultSet({
        ...result,
        status: parseInt(event.data),
      });
      if (event.data == "0") {
        setLoading(false);
      }
    }
  };
  socket.onclose = socket.onerror = () => {
    clearInterval(timer);
  };
}
