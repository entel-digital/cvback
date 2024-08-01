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
        colorGroup
      }
      eventType {
        id
        name
        addedDate
      }
      frames {
        id
        imageUrl
        imageWithBoundingboxesUrl
      }
      keyFrames {
        id
        name
        frames {
          id
          imageUrl
          imageWithBoundingboxesUrl
        }
      }
      videos {
        id
        video
        addedDate
        informedDate
      }
      keyVideos {
        id
        name
        videos {
          id
          video
        }
      }
      labelsDetected {
        id
        name
        colorGroup
      }
      labelsMissing {
        id
        name
        colorGroup
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
      inferenceDetectionClassificationTracker {
        id
        confidence
        trackingIds
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