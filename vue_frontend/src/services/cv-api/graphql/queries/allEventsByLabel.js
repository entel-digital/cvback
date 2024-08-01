export default `
query filteredAndPaginatedEvents($offset: Int, $rowsPerPage: Int,$labelTextFilter: String, ) {
  filteredAndPaginatedEvents(offset: $offset, rowsPerPage: $rowsPerPage,  labelTextFilter: $labelTextFilter) {
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
