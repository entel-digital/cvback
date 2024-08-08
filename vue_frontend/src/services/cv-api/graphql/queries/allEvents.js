export default `
query filteredAndPaginatedEvents($offset: Int, $rowsPerPage: Int) {
  filteredAndPaginatedEvents(offset: $offset, rowsPerPage: $rowsPerPage) {
    filtered
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
    }
    typesSummary
    globalTotalNumber
    labelsSummary
    labelTextFilter
    queryTotalNumber
  }
}
`