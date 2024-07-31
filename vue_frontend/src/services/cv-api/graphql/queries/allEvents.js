export default `
query paginatedEvents(first: 10, skip: 10) {
    edges {
      node {
        eventType {
          id
          name
        }
        eventLabel {
          id
          name
        }
        id
        informedDate
        addedDate
        labelsDetected {
          colorGroup
          id
          name
        }
        labelsMissing {
          colorGroup
          id
          name
        }
        keyInferenceDetectionClassification {
          name
          id
        }
        keyInferenceOcr {
          id
          name
        }
        frames {
          id
          imageUrl
          imageWithBoundingboxesUrl
        }
      }
    }
  }
}
`;
