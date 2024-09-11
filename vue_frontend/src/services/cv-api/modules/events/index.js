import { queries } from '@/services/cv-api/graphql/'
import { Post } from '@/services/utils/post'

export const getAllEvents = async (offset, rowsPerPage, sortBy, asc) => {
  const body = {
    query: queries.allEvents,
    variables: { offset, rowsPerPage, sortBy, asc}
  }
  const { data } = await Post(body)
  return data
}

export const getAllEventsByDate = async (
  offset,
  rowsPerPage,
  dateGreaterThanEqual,
  dateLowerThan,
  sortBy,
  asc
) => {
  const body = {
    query: queries.allEventsByDate,
    variables: { offset, rowsPerPage, dateGreaterThanEqual, dateLowerThan, sortBy, asc }
  }
  const { data } = await Post(body)
  return data
}

export const getAllEventsByDateAndLabel = async (
  offset,
  rowsPerPage,
  dateGreaterThanEqual,
  dateLowerThan,
  labelIdFilter,
  sortBy,
  asc
) => {
  const body = {
    query: queries.allEventsByDateAndLabel,
    variables: { offset, rowsPerPage, dateGreaterThanEqual, dateLowerThan, labelIdFilter, sortBy, asc }
  }
  const { data } = await Post(body)
  return data
}

export const getAllEventsByLabel = async (offset, rowsPerPage, labelIdFilter, sortBy, asc) => {
  const body = {
    query: queries.allEventsByLabel,
    variables: { offset, rowsPerPage, labelIdFilter, sortBy, asc }
  }
  const { data } = await Post(body)
  return data
}

export const getAllEventsById = async (idEqualsTo) => {
  const body = {
    query: queries.allEventsById,
    variables: { idEqualsTo }
  }
  const { data } = await Post(body)
  return data
}

export const getSummary = async () => {
  const body = {
    query: queries.summaryEvents
  }
  const { data } = await Post(body)
  return data
}
