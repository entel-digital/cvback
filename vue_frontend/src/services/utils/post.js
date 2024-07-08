import axios from "axios";
import { getToken } from "src/services/utils/getToken";

const token = getToken("csrfmiddlewaretoken");

export const Post = async (path, body) => {
  try {
    console.log("document", document);
    // const url = `${process.env.CV_API}/${path}/graphql`;
    const url = `http://0.0.0.0:8000/${path}/graphql/`;

    console.log("token del post", token);

    const { data, status } = await axios.post(url, JSON.stringify(body), {
      // mode: "cors",
      headers: {
        "Content-Type": "application/json",
        "X-Csrftoken":
          "4TC5pQO4XNTe5YGOGtQUtKRzmvdwOuQzEr6qx2xgl4rhqK359PjVX6vD2NGC2xau",
        // "X-CSRFToken": token,
      },
    });
    if (Array.isArray(data.errors) && data.errors.length > 0) {
      const [err] = data.errors;
      const { message } = err;
      throw new Error(`invalid error message=${message}`);
    }

    if (data.data == null) {
      throw new Error("invalid null data response");
    }

    if (status !== 200) {
      throw new Error(`invalid request status=${status}`);
    }

    return data;
  } catch (err) {
    console.log("HERE IN ERROR POST", err);
    throw err;
  }
};
