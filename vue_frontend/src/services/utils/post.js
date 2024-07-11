import {api} from "src/boot/axios";
import { getToken } from "src/services/utils/getToken";

export const Post = async (path, body) => {
  try {
    // const url = `${process.env.CV_API}/${path}/graphql`;
    const url = `${window.location}/${path}/graphql/`;

    const { data, status } = await api.post(url, JSON.stringify(body), {
      // mode: "cors",
      headers: {
        "Content-Type": "application/json",
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
