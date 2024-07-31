export default `
query filteredAndPaginatedEvents($dateGreaterThanEqual: DateTime, $dateLowerThan: DateTime) {
  filteredAndPaginatedEvents( dateGreaterThanEqual: $dateGreaterThanEqual, dateLowerThan: $dateLowerThan) {
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
        imageWithBoundingboxesUrl
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
          imageWithBoundingboxesUrl
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
