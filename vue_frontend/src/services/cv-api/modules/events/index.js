import { queries } from "src/services/cv-api/graphql/";
import { Post } from "src/services/utils/post";

export const getAllEvents = async () => {
  const path = "events";
  const body = {
    query: queries.allEvents,
  };
  const { data } = await Post(path, body);
  return data;
};
