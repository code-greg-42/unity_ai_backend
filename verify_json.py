import difflib

def verify_json_schema(json_data):
    """
    Verifies that json_data adheres to the expected Unity shapes schema.
    
    Expected schema:
      - Top-level: a dictionary with exactly one key: "shapes".
      - "shapes": a non-empty list.
      - Each element (shape) is a dictionary with exactly the keys:
            "shape", "size", and "position".
         - "shape" must equal "cube" (all lowercase).
         - "size" is a dictionary with keys "x", "y", and "z" (each numeric and > 0).
         - "position" is a dictionary with keys "x", "y", and "z" (each numeric; values may be negative).
    
    Returns:
      (True, None) if valid,
      (False, error_message) if invalid.
      
    The error_message will be one of the following fixed strings:
      - "Overall formatting is incorrect"
      - "Top-level key 'shapes' not found"
      - "Mispelled key in JSON"
      - "Missing property key in shape"
      - "Missing key or value in shape property"
      - "Invalid type error"
      - "Non-positive size value"
    """
    # 1. Overall formatting: must be a dict.
    if not isinstance(json_data, dict):
        return False, "Overall formatting is incorrect"
    
    # 2. Top-level key check:
    if "shapes" not in json_data:
        # If any key lowercased equals "shapes" but is not exactly "shapes", flag it as a mispelling.
        for key in json_data.keys():
            if key.lower() == "shapes" and key != "shapes":
                return False, "Mispelled key in JSON"
        return False, "Top-level key 'shapes' not found"
    
    shapes = json_data["shapes"]
    if not isinstance(shapes, list) or not shapes:
        return False, "Overall formatting is incorrect"
    
    # 3. Check each shape.
    for shape in shapes:
        # Each shape must be a dict.
        if not isinstance(shape, dict):
            return False, "Missing property key in shape"
        
        required_keys = {"shape", "size", "position"}
        actual_keys = set(shape.keys())
        if actual_keys != required_keys:
            # For each expected key, if it's missing, try to see if a close match exists.
            for req in required_keys:
                if req not in shape:
                    # Look for a key with high similarity.
                    for key in shape.keys():
                        if key != req and difflib.SequenceMatcher(None, key.lower(), req).ratio() > 0.8:
                            return False, "Mispelled key in JSON"
                    return False, "Missing property key in shape"
        
        # 4. Check that "shape" equals "cube".
        if shape.get("shape") != "cube":
            return False, "Missing property key in shape"
        
        # 5. Validate "size".
        if "size" not in shape or not isinstance(shape["size"], dict):
            return False, "Missing property key in shape"
        size = shape["size"]
        if set(size.keys()) != {"x", "y", "z"}:
            return False, "Missing key or value in shape property"
        for coord in ["x", "y", "z"]:
            value = size.get(coord)
            if not isinstance(value, (int, float)):
                return False, "Invalid type error"
            if value <= 0:
                return False, "Non-positive size value"
        
        # 6. Validate "position".
        if "position" not in shape or not isinstance(shape["position"], dict):
            return False, "Missing property key in shape"
        position = shape["position"]
        if set(position.keys()) != {"x", "y", "z"}:
            return False, "Missing key or value in shape property"
        for coord in ["x", "y", "z"]:
            value = position.get(coord)
            if not isinstance(value, (int, float)):
                return False, "Invalid type error"
    
    return True, None
