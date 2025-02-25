VALID_TEST_CASES = [
    (
        "Valid: Single shape",
        {
            "shapes": [
                {"shape": "cube", "size": {"x": 1, "y": 2, "z": 3}, "position": {"x": 0, "y": 0, "z": 0}}
            ]
        }
    ),
    (
        "Valid: Multiple shapes",
        {
            "shapes": [
                {"shape": "cube", "size": {"x": 2, "y": 3, "z": 4}, "position": {"x": 1, "y": 1, "z": 1}},
                {"shape": "cube", "size": {"x": 1, "y": 1, "z": 1}, "position": {"x": -1, "y": -1, "z": -1}}
            ]
        }
    )
]

MISSING_PROPERTY_TEST_CASES = [
    (
        "Missing 'shape' key",
        {
            "shapes": [
                {"size": {"x": 1, "y": 2, "z": 3}, "position": {"x": 0, "y": 0, "z": 0}}
            ]
        },
    ),
    (
        "Missing 'size' key",
        {
            "shapes": [
                {"shape": "cube", "position": {"x": 0, "y": 0, "z": 0}}
            ]
        }
    ),
    (
        "Missing 'position' key",
        {
            "shapes": [
                {"shape": "cube", "size": {"x": 1, "y": 2, "z": 3}}
            ]
        },
    )
]

MISPELLED_KEY_TEST_CASES = [
    (
        "Mispelled top-level key",
        {
            "Shapes": [
                {"shape": "cube", "size": {"x": 1, "y": 2, "z": 3}, "position": {"x": 0, "y": 0, "z": 0}}
            ]
        }
    ),
    (
        "Mispelled property key in shape",
        {
            "shapes": [
                {"shap": "cube", "size": {"x": 1, "y": 2, "z": 3}, "position": {"x": 0, "y": 0, "z": 0}}
            ]
        }
    )
]

INCORRECT_TYPE_TEST_CASES = [
    (
        "Non-numeric value in size",
        {
            "shapes": [
                {"shape": "cube", "size": {"x": "1", "y": 2, "z": 3}, "position": {"x": 0, "y": 0, "z": 0}}
            ]
        }
    ),
    (
        "Non-numeric value in position",
        {
            "shapes": [
                {"shape": "cube", "size": {"x": 1, "y": 2, "z": 3}, "position": {"x": "0", "y": 0, "z": 0}}
            ]
        }
    )
]

NON_POSITIVE_SIZE_TEST_CASES = [
    (
        "Negative size value",
        {
            "shapes": [
                {"shape": "cube", "size": {"x": -1, "y": 2, "z": 3}, "position": {"x": 0, "y": 0, "z": 0}}
            ]
        }
    ),
    (
        "Size value of zero",
        {
            "shapes": [
                {"shape": "cube", "size": {"x": 1, "y": 2, "z": 0}, "position": {"x": 0, "y": 0, "z": 0}}
            ]
        }
    )
]

OVERALL_FORMATTING_TEST_CASES = [
    (
        "Top-level is not a dictionary",
        [
            {"shape": "cube", "size": {"x": 1, "y": 2, "z": 3}, "position": {"x": 0, "y": 0, "z": 0}}
        ]
    ),
    (
        "Shapes is not a list",
        {
            "shapes": {"shape": "cube", "size": {"x": 1, "y": 2, "z": 3}, "position": {"x": 0, "y": 0, "z": 0}}
        }
    )
]
