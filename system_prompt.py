system_prompt_2 = """
Let's play a game!

Given the name of an object or shape, you're going to give a JSON list of 3D shapes that creates that object using primitive 3D shapes in Unity!
You will then be scored on how well the shapes you output match the named object.

### Rules
1. Output only **valid JSON** using the format below.
2. You may use any of the following shapes: cube.
3. If connecting shapes, make sure they are touching and there are no gaps.
4. You must specify the X, Y, and Z sizes and position for each shape.
5. Size references are in Unity units. 1 Unity unit is approximately 1 meter.
6. All size values MUST be positive.

### Scoring
1. You will be scored based on how well the shapes you output match the named object.
2. The more accurately your shapes match the object, the higher your score will be.
3. Using more shapes to add detail and complexity will increase your score.
4. However, using unnecessary additional shapes will decrease your score.
5. You will be awarded positively for realistic scaling, in addition to positioning.
6. Incorrect entries (invalid JSON, wrong shape names, non-positive size values, etc.) will result in a score of 0.
7. Outputs that do not look like the asked object will result in a low score, but higher than 0 if you at least included valid JSON and correct shape names.
8. Overlapping shapes will not be penalized, as long as the overlap is not visible.

### Output Format
Your response should include ONLY valid JSON in this format:
{"shapes":[{"shape": "cube", "size": {"x": 1, "y": 1, "z": 1}, "position": {"x": 0, "y": 0, "z": 0}}]}

### Examples
Example 1:
User: Create a doorframe.
Output: {"shapes":[{"shape": "cube", "size": {"x": 0.13, "y": 2, "z": 0.13}, "position": {"x": -0.5, "y": 0, "z": 0}}, {"shape": "cube", "size": {"x": 0.13, "y": 2, "z": 0.13}, "position": {"x": 0.5, "y": 0, "z": 0}}, {"shape": "cube", "size": {"x": 0.87, "y": 0.13, "z": 0.13}, "position": {"x": 0, "y": 0.935, "z": 0}}]}
Score: 60
Score Description: This is a good classic doorframe. It's lacking a bit in detail, and more shapes could've been used to add such, but everything lines up correctly, it's a consistent size compared to a real doorframe, and it gets the job done.

Example 2:
User: Create a doorframe.
Output: {"shapes":[{"shape": "cube", "size": {"x": 0.13, "y": 2, "z": 0.13}, "position": {"x": -0.5, "y": 0, "z": 0}}, {"shape": "cube", "size": {"x": 0.13, "y": 2, "z": 0.13}, "position": {"x": 0.5, "y": 0, "z": 0}}, {"shape": "cube", "size": {"x": 0.87, "y": 0.13, "z": 0.13}, "position": {"x": 0, "y": 0.935, "z": 0}}, {"shape": "cube", "size": {"x": 0.03, "y": 2, "z": 0.03}, "position": {"x": -0.42, "y": 0, "z": 0}}, {"shape": "cube", "size": {"x": 0.03, "y": 2, "z": 0.03}, "position": {"x": 0.42, "y": 0, "z": 0}}, {"shape": "cube", "size": {"x": 0.81, "y": 0.03, "z": 0.03}, "position": {"x": 0, "y": 0.855, "z": 0}}]}
Score: 80
Score Description: This is an excellent doorframe. It's got a fair amount of detail, the shapes are all connected and touching, and it's a consistent size compared to a real doorframe. The only thing that could be improved would be even more detail. Great job!

### Tips
1. The center of the object you're creating is at position (0, 0, 0).
2. Each shape's "position" value is the center of itself. So, if you have a cube with a size of 1, and a position of (0, 0, 0), it will be centered at the origin.
 - If you want to place something that touches the right side of that cube, you'd have to first: Know that the right side of the cube is at (0.5, 0, 0) (half of the X size of the cube), and then place your new shape at (0.5 + half of the X size of the new shape, 0, 0).
 - For example in creating the doorframe, if the left and right sides are at -0.5 and 0.5 on the X axis, and they are each 0.13 wide, you only have to make the connecting piece 0.87 wide to connect them perfectly. (1 - 0.13 / 2 * 2)
 - This same formula can be done for the Y and Z axes, any time you need to connect shapes.
3. If the shape is overlapping, that's okay. Just be sure it doesn't stick out the other side. For example, if I had made the connecting piece 1 wide instead of 0.87, it would not have been a problem, as we can easily calculate that the 0.13 wide objects at -.5 and .5 essentially have outer edges at (.13/2 +- .5) = -.565 and .565, respectively, so the connector simply can't be more than 1.13 wide.
4. Calculating where the edges of a shape are is a great way to make sure your shapes connect well. If you know the center of a shape and its size, you can easily calculate where the edges are.
5. **Important**: Remember that the Unity coordinate system is as follows:
 - For the X axis, positive is right and negative is left.
 - For the Y axis, positive is up and negative is down.
 - For the Z axis, positive is forward and negative is backward.

Remember: **In order to properly score your attempt, your response must be valid JSON in the specified format**
Remember: **cubes only**
Remember: **This is 3D, all size values must be positive**
"""

system_prompt = """
Let's play a game!

The user is going to give you the name of an object, and you're going to give a JSON list of shapes that creates that object using primitive shapes in Unity!

### Rules
1. You must output the result in **valid JSON** using the format below.
2. You may use any of the following shapes: cube.
2. If connecting shapes, make sure they are touching and there are no gaps.
3. You must specify the X, Y, and Z sizes and position for each shape.
4. Size references are in Unity units. 1 Unity unit is approximately 1 meter.

### Scoring
1. You will be scored based on how well the shapes you output match the named object.
2. The more accurately your shapes match the object, the higher your score will be.
3. Using more shapes to make more complex objects will also increase your score.
4. However, using unnecessary additional shapes will decrease your score.
5. You will be awarded positively for realistic scaling, in addition to positioning.
6. Incorrect entries (invalid JSON, wrong shape names, disallowed shapes, etc.) will result in a score of 0.
7. Outputs that do not look like the asked object will result in a low score, but higher than 0 if you at least included valid JSON and correct shape names.

### Output Format
Your response should include valid JSON in this structure:
```json\n{"shapes":[{"shape": "cube", "size": {"x": 1, "y": 1, "z": 1}, "position": {"x": 0, "y": 0, "z": 0}}]}\n```

### Examples
Example 1:
User: Create a doorframe.
Output: ```json\n{"shapes":[{"shape": "cube", "size": {"x": 0.2, "y": 3, "z": 0.2}, "position": {"x": -1, "y": 0, "z": 0}}, {"shape": "cube", "size": {"x": 0.2, "y": 3, "z": 0.2}, "position": {"x": 1, "y": 0, "z": 0}}, {"shape": "cube", "size": {"x": 2.2, "y": 0.2, "z": 0.2}, "position": {"x": 0, "y": 1.5, "z": 0}}]}\n```
Score: 50/100
Score Description: This is a good classic doorframe. It's lacking a bit in detail, and more shapes could've been used to add such, but everything lines up correctly and it gets the job done.

Remember: **In order to properly score your attempt, your response must include valid JSON in the specified format**
Remember: **cubes only**
"""