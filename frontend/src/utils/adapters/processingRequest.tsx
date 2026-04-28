import { message } from "antd";
import { getCookie } from "../../components/CSRF";
import config from "../../config.json";
import lang from "../../lang.json";
import fetch from "node-fetch";

type form_values = {
    analyzer: string;
    fileId: string;
    rcsbPdbId: string;
    settings: {
        reorder: boolean;
        g4Limited: boolean;
        model: number;
    };
};
export function processingRequest(data: form_values, setLoading: any) {
    const requestOptions = {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "X-CSRFToken": getCookie(),
        },
    };
    requestOptions.headers["Access-Control-Allow-Origin"] = "*";
    fetch(config.SERVER_URL + "/api/process/request/", requestOptions)
        .then((response: any) => {
            if (response.status == 404) {
                message.error(lang.rcsb_error);
                setLoading(false);
                return "";
            } else {
                return response.json();
            }
        })
        .then((response: any) => {
            if (response != "") {
                window.open(
                    config.FRONTEND_URL + "/result/" + response.orderId,
                    "_self"
                );
                setLoading(false);
            }
        })
        .catch((error: any) => message.error("Something went wrong, try again"));
}
