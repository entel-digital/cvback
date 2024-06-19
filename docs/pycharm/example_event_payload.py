payload = {
    "timestamp": "2024-06-18T09:54:54Z", # no se si ese es el formato que pide el back?
    "event_type": "vehicle_tracking_completed",
    "label": "non_compliant",
    "confidence": 0,
    "labels_detected": [0, 2, 3, 4], # ID del cvback
    "labels_missing": [1], # ID del cvback
    "cameras": [0, 1],  # quemadisimo por ahora
    "frames": [
    {
      "id": 0,
      "path": "/mnt/Data/Compliance_Status/non_compliance/415_main_20240618_095454.jpg"
    }],
    "inference_detection_classification_tracker": [
    {
      "label": "vehicle",
      "track_id": 415, # id de seguimiento interno
      "history": [
        {"previous_center": 0.84427083, "current_center": 0.84296875, "line_position": 0.82291667, "frame_index": 123}
      ]
    }
    ],
    "key_inference_detection_classification_tracker":{
        "selected_track_id": 415,
    },
    "inference_detection_classification": [
    {
      "label": 0,
      "bounding_box": {
        "x1": 0.1,
        "y1": 0.15,
        "x2": 0.2,
        "y2": 0.25
      },
      "confidence": 0.98,
      "frame_index": 123,
      "timestamp": "2024-06-18T09:54:20Z"
    },
    {
      "label": "baliza",
      "bounding_box": {
        "x1": 0.21,
        "y1": 0.16,
        "x2": 0.26,
        "y2": 0.27
      },
      "confidence": 0.95,
      "frame_index": 123,
      "timestamp": "2024-06-18T09:54:30Z"
    },
    {
      "label": "banderín",
      "bounding_box": {
        "x1": 0.12,
        "y1": 0.18,
        "x2": 0.19,
        "y2": 0.29
      },
      "confidence": 0.92,
      "frame_index": 123,
      "timestamp": "2024-06-18T09:54:35Z"
    },
    {
      "label": "pértiga",
      "bounding_box": {
        "x1": 0.15,
        "y1": 0.14,
        "x2": 0.23,
        "y2": 0.26
      },
      "confidence": 0.87,
      "frame_index": 123,
      "timestamp": "2024-06-18T09:54:40Z"
    },
    {
      "label": "placa_patente",
      "bounding_box": {
        "x1": 0.05,
        "y1": 0.10,
        "x2": 0.20,
        "y2": 0.15
      },
      "confidence": 0.99,
      "frame_index": 123,
      "timestamp": "2024-06-18T09:54:45Z"
    }
    ],
    "key_inference_detection_classification": {
      "main_image": 123,
      "lpr_successful_image": 123,
      "lpr_middle_image": 132
    },
    "inference_detection_ocr": [
    {
      "name": "license_plate",
      "value": "TJYB39",
      "confidence": 0.99,
      "frame_index": 123
    }],
    "key_inference_ocr": {
        "selected_license_plate": 420, # ID del cvback
        "main_image": 123,
        "lpr_successful_image": 123,
        "lpr_middle_image": 132
    },
}
