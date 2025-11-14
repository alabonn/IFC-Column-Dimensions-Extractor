# IFC Column Dimension Extractor

This script extracts the width, length, and height of each IfcColumn by generating its geometric mesh using ifcopenshell.geom.  
It does not rely on IFC parameters like XDim, YDim, or ZDim; instead, it computes dimensions directly from the bounding box created from the column's geometry.

The script works even when explicit dimensions are missing or when the column shape cannot be obtained from predefined IFC properties.

## How it works

- Loads the IFC file and enables world-coordinate geometry extraction.
- Iterates through all IfcColumn elements in the model.

### For each column:
- Creates a mesh geometry using ifcopenshell.geom.create_shape().
- Extracts all vertex coordinates of the mesh.
- Computes the minimum and maximum XYZ values.
- Calculates a geometric bounding box as:
  - **width** → the smaller side of the column  
  - **length** → the larger side of the column  
  - **height** → the Z extent  
  *(Note: if you are dealing with circular columns, you can replace the width variable to diameter since it has the same process as tested)*

- Converts all values from meters (m) to millimeters (mm).  
  *(Note: ifcopenshell.geom always outputs geometry in meters regardless of IFC project units.)*

- Prints the extracted dimensions.
- Saves the results into a CSV file named **columns_output.csv** with columns:  
  `["GlobalId", "Width_mm", "Length_mm", "Height_mm"]`.
