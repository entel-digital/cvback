import { queries } from "@/services/cv-api/graphql/";
import { Post } from "@/services/utils/post";

export const getAllEvents = async (offset, rowsPerPage) => {
  const body = {
    query: queries.allEvents,
    varibles: {offset,  rowsPerPage },
  };
  const { data } = await Post(body);
  return data;
};

export const getAllEventsByDate = async (dateGreaterThanEqual, dateLowerThan) => {
  const body = {
    query: queries.allEventsByDate,
    varibles: {dateGreaterThanEqual,  dateLowerThan },
  };
  const { data } = await Post(body);
  return data;
};

export const getAllEventsByDateAndLabel = async (dateGreaterThanEqual, dateLowerThan, labelTextFilter) => {
  const body = {
    query: queries.allEventsByDateAndLabel,
    varibles: {dateGreaterThanEqual,  dateLowerThan, labelTextFilter },
  };
  const { data } = await Post(body);
  return data;
};

export const getAllEventsByLabel = async (labelTextFilter) => {
  const body = {
    query: queries.allEventsByLabel,
    varibles: {labelTextFilter },
  };
  const { data } = await Post(body);
  return data;
};

export const getAllEventsById = async (idEqualsTo) => {
  const body = {
    query: queries.allEventsById,
    varibles: {idEqualsTo },
  };
  const { data } = await Post(body);
  return data;
};

export const getSummary = async () => {
  const body = {
    query: queries.summaryEvents,
  };
  const { data } = await Post(body);
  return data;
};
