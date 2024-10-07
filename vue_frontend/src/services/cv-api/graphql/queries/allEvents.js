export default `
query filteredAndPaginatedEvents($offset: Int, $rowsPerPage: Int, $sortedBy: String, $asc: Boolean) {
  filteredAndPaginatedEvents(offset: $offset, rowsPerPage: $rowsPerPage, sortedBy: $sortedBy, asc: $asc) {
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
    events {
      id
      addedDate
      informedDate
      confidence
      eventLabel {
        id
        name
      }
      eventType {
        id
        name
        addedDate
      }
      frames {
        id
        imageUrl
      }
      videos {
        id
        videoUrl
      }
      labelsDetected {
        id
        name
      }
      labelsMissing {
        id
        name
      }
      inferenceDetectionClassification {
        id
        confidence
        frame {
          id
          imageUrl
        }
        labels {
          id
          name
        }
        boundingBoxes {
          id
          topLeft
          bottomRight
        }
      }
      inferenceOcr {
        id
        name
        value
        confidence
      }
      inferenceOcr {
        id
        name
        value
        confidence
      }
      inferenceClassification {
        id
        label{
          name
        }
      }
    }
  }
}
`
