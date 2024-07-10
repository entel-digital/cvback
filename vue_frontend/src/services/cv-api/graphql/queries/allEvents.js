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
   		image
      addedDate
    }
    confidence
  }
}
`;
