export default `
query filteredAndPaginatedEvents() {
  filteredAndPaginatedEvents() {
    filtered
    typesSummary
    globalTotalNumber
    labelsSummary
    labelTextFilter
    queryTotalNumber
    uniqueLabelsCount
    queryTotalEventsYear
    queryTotalEventsWeek
    queryTotalEventsMonth
    queryTotalEventsDay
}
}
`
