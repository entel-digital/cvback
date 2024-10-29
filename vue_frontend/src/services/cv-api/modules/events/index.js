import { queries } from '@/services/cv-api/graphql/'
import { Post } from '@/services/utils/post'

export const getAllEvents = async (offset, rowsPerPage, sortedBy, asc) => {
  const body = {
    query: queries.allEvents,
    variables: { offset, rowsPerPage, sortedBy, asc}
  }
  const { data } = await Post(body)
  return data
}

export const getAllEventsByDate = async (
  offset,
  rowsPerPage,
  dateGreaterThanEqual,
  dateLowerThan,
  sortedBy,
  asc
) => {
  const body = {
    query: queries.allEventsByDate,
    variables: { offset, rowsPerPage, dateGreaterThanEqual, dateLowerThan, sortedBy, asc }
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
  sortedBy,
  asc
) => {
  const body = {
    query: queries.allEventsByDateAndLabel,
    variables: { offset, rowsPerPage, dateGreaterThanEqual, dateLowerThan, labelIdFilter, sortedBy, asc }
  }
  const { data } = await Post(body)
  return data
}

export const getAllEventsByLabel = async (offset, rowsPerPage, labelIdFilter, sortedBy, asc) => {
  const body = {
    query: queries.allEventsByLabel,
    variables: { offset, rowsPerPage, labelIdFilter, sortedBy, asc }
  }
  const { data } = await Post(body)
  return data
}

export const getAllEventsById = async (token, idEqualsTo) => {
  const body = {
    query: queries.allEventsById,
    variables: { idEqualsTo }
  }
  const { data } = await Post(body, token)
  return data
}

export const getSummary = async () => {
  const body = {
    query: queries.summaryEvents
  }
  const { data } = await Post(body)
  return data
}
