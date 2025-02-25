import regex as re
import json
from enum import Enum

class ModelResponseStatus(Enum):
    ONLY_JSON = 0
    BLOCK_JSON = 1
    INCLUDE_JSON = 2

### for prompts that specify INCLUDE json
def extract_json_from_response(response:str):
    
    # match a code block with json content
    fence_match = re.search(r"```json\s*(\{[\s\S]*?\})\s*```", response)
    if fence_match:
        json_str = fence_match.group(1).strip()
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Regex extraction succeeded, but JSON decoding failed: {e}")
    
    # attempt to return entire response as json
    try:
        return json.loads(response.strip())
    except json.JSONDecodeError as e:
        pass
    
    # search for json within the response
    curly_match = re.search(r"(\{(?:[^{}]|(?R))*\})", response, flags=re.DOTALL)
    if curly_match:
        json_str = curly_match.group(1).strip()
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Loose curly-brace extraction succeeded, but JSON decoding failed: {e}")

    # no json found
    raise ValueError("Failed to locate valid JSON in the response.")


### for prompts that specify returning ONLY json
def extract_json(response:str):
    
    # attempt to return entire response as json
    try:
        json_data = json.loads(response.strip())
        return json_data, ModelResponseStatus.ONLY_JSON
    except json.JSONDecodeError as e:
        pass
    
    # match a code block with json content
    fence_match = re.search(r"```json\s*(\{[\s\S]*?\})\s*```", response)
    if fence_match:
        json_str = fence_match.group(1).strip()
        try:
            return json.loads(json_str), ModelResponseStatus.BLOCK_JSON
        except json.JSONDecodeError as e:
            raise ValueError(f"Regex extraction succeeded, but JSON decoding failed: {e}")
    
    # search for json within the response
    curly_match = re.search(r"(\{(?:[^{}]|(?R))*\})", response, flags=re.DOTALL)
    if curly_match:
        json_str = curly_match.group(1).strip()
        try:
            return json.loads(json_str), ModelResponseStatus.INCLUDE_JSON
        except json.JSONDecodeError as e:
            raise ValueError(f"Loose curly-brace extraction succeeded, but JSON decoding failed: {e}")

    # no json found
    raise ValueError("Failed to locate valid JSON in the response.")