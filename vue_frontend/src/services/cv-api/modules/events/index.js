import { queries } from "src/services/cv-api/graphql/";
import { Post } from "src/services/utils/post";

export const getAllEvents = async (from, skip) => {
  const path = "events";
  const body = {
    query: queries.allEvents,
    varibles: {first: from, skip: skip},
  };
  const { data } = await Post(path, body);
  return data;
};
