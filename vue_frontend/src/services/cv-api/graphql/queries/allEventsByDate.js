export default `
query filteredAndPaginatedEvents($offset: Int, $rowsPerPage: Int, $dateGreaterThanEqual: DateTime, $dateLowerThan: DateTime) {
  filteredAndPaginatedEvents(offset: $offset, rowsPerPage: $rowsPerPage, dateGreaterThanEqual: $dateGreaterThanEqual, dateLowerThan: $dateLowerThan) {
    filtered
    events {
      addedDate
      confidence
      id
      informedDate
      eventLabel {
        colorGroup
        id
        name
      }
      eventType {
        addedDate
        id
        name
      }
      frames {
        imageUrl
        id
      }
      inferenceDetectionClassification {
        boundingBoxes {
          bottomRight
          topLeft
          id
        }
      }
      labelsMissing {
        colorGroup
        id
        name
      }
      labelsDetected {
        name
        id
        colorGroup
      }
      keyFrames {
        frames {
          id
          imageUrl
        }
        id
        name
      }
    }
    typesSummary
    globalTotalNumber
    labelsSummary
    labelTextFilter
    queryTotalNumber
}
}
`
