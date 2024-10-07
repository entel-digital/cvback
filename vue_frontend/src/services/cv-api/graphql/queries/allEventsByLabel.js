export default `
query filteredAndPaginatedEvents($offset: Int, $rowsPerPage: Int,$labelIdFilter: String, $sortedBy: String, $asc: Boolean ) {
  filteredAndPaginatedEvents(offset: $offset, rowsPerPage: $rowsPerPage,  labelIdFilter: $labelIdFilter, sortedBy: $sortedBy, asc: $asc) {
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
      }
      keyFrames {
        id
        name
        frames {
          id
          imageUrl
        }
      }
      videos {
        id
        videoUrl
      }
      keyVideos {
        id
        name
        videos {
          id
          videoUrl
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
      inferenceClassification {
        id
        label{
          name
        }
      }
    }
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
