export default `
query filteredAndPaginatedEvents($offset: Int, $rowsPerPage: Int) {
  filteredAndPaginatedEvents(offset: $offset, rowsPerPage: $rowsPerPage) {
    totalNumber
    offset
    rowsPerPage
    filtered
    events {
      addedDate
      confidence
      eventLabel {
        colorGroup
        id
        name
      }
      eventType {
        id
        name
      }
      id
      informedDate
      labelsMissing {
        id
        name
        colorGroup
      }
      labelsDetected {
        name
        id
        colorGroup
      }
      inferenceDetectionClassification {
        boundingBoxes {
          topLeft
          bottomRight
          id
        }
      }
      keyFrames {
        id
        name
        frames {
          imageWithBoundingboxesUrl
          imageUrl
          id
        }
      }
      frames {
        imageUrl
        imageWithBoundingboxesUrl
        id
      }
    }
  }
}
`;
