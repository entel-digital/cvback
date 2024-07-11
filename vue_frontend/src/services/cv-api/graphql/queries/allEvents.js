export default `
query allEvents {
  allEvents {
    id
    eventType {
      id
      name
    }
    eventLabel {
      id
      name
      colorGroup
    }
    informedDate
    addedDate
    keyFrames {
      id
      name
      frames {
        id
        image
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
        image
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
    frames {
      id
      imageUrl
      imageWithBoundingboxesUrl
    }
    confidence
  }
}
`;
