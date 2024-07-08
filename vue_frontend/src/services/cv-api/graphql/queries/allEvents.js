export default `
query allEvents {
  allEvents {
    addedDate
    id
    confidence
    eventType {
      name
    }
    labelsDetected {
      id
      colorGroup
      name
    }
    labelsMissing {
      colorGroup
      id
      name
    }
    inferenceDetectionClassification {
      boundingBoxes {
        bottomRight
        topLeft
      }
      algorithm {
        kind
        name
        boundingboxSet {
          bottomRight
          topLeft
        }
      }
    }
  }
}
`;
