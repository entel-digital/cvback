import { queries } from "@/services/cv-api/graphql/";
import { Post } from "@/services/utils/post";

export const getAllEvents = async (skip, rows) => {
  const body = {
    query: queries.allEvents,
    varibles: {offset: skip, rowsPerPage: rows, },
  };
  const { data } = await Post(body);
  return data;
};

