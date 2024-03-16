import { FORTUNA_API_BASE } from "@/lib/constants";

export async function sendTask(message, jwt) {
  const url = new URL(`${FORTUNA_API_BASE}/task/`);
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-fortuna-jwt": jwt
      },
      body: JSON.stringify({
        type: "spot",
        text: message,
      }),
    });
    if (response.ok) {
      const responseData = await response.json();
      console.log(responseData);
      return responseData;
    } else {
      console.warn(await response.text());
      return {response: "Sorry I couldn't quite handle that, lets try again"};
    }
  } catch (e) {
    console.log(e);
    return {
      response: "Sorry looks like there was an issue, please try again later",
    };
  }
}
