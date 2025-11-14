import ifcopenshell
import ifcopenshell.geom
import numpy as np
import csv

# ================= SETTINGS + LOAD IFC =================
ifc = ifcopenshell.open("IFC_File_Path") # <------------------- IFC file here
settings = ifcopenshell.geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)

OUTPUT_CSV = "columns_output.csv" ####### You can delete this line if you dont want to save it as a CSV file

# ================= GET COLUMNS =================
# ------ List of columns ------
columns = ifc.by_type("IfcColumn")
print(f"Found {len(columns)} columns in the model.\n")

# ------ List of columns formatted later for csv ------
columns_data = [] ####### You can delete this line if you dont want to save it as a CSV file

# ================= EXTRACTION =================
    # Extract width/length/height for each column
for col in columns:
    try:
        width = length = height = None
        
        # ------ Create mesh bounding box ------
        shape = ifcopenshell.geom.create_shape(settings, col)
        verts = np.array(shape.geometry.verts, dtype=float).reshape(-1, 3)
        min_xyz = verts.min(axis=0)
        max_xyz = verts.max(axis=0)
        bbox = max_xyz - min_xyz

        
        # ------ Column coordinates used for calculation ------
        ####### You can delete this part if you are not interested in saving the coords #######
        min_x = min_xyz[0]
        min_y = min_xyz[1]
        min_z = min_xyz[2]
        
        max_x = max_xyz[0]
        max_y = max_xyz[1]
        max_z = max_xyz[2]
        
        print(f"Column {col.GlobalId}:")
        print(f"bbox: {bbox}")
        print(f"min xyz: {min_xyz}")
        print(f"max xyz: {max_xyz}")
        print(f"min x: {min_x}     y: {min_y}    z: {min_z}")
        print(f"max x: {max_x}     y: {max_y}    z: {max_z}")
        print()
        #####################################################################################
        
        # ------ Make length the larger side ------
        height = bbox[2]
        if bbox[0]<bbox[1]:
            width = bbox[0]
            length = bbox[1]
        else:
            width = bbox[1]
            length = bbox[0]
        
        # ------ Convert from m to mm ------
        height *= 1000
        width *= 1000
        length *= 1000
        
        # ------ Displays each column's info ------
        print(f"Column {col.GlobalId}: width={width}, length={length}, height={height}")
        print("---------------------------------------")
        print()

        ####### You can delete this part if you dont want to save it as a CSV file #######
        # ------ Add to list ------
        columns_data.append({
            "GlobalId": col.GlobalId,
            "Width_mm": width,
            "Length_mm": length,
            "Height_mm": height,
        })
        #####################################################################################
        
    except Exception as e:
        print(f"Error with column {col.GlobalId}: {e}")
        print("---------------------------------------")
        print()
    
# ================= CSV CREATION =================
with open(OUTPUT_CSV, "w", newline="") as csvfile:
    fieldnames = ["GlobalId", "Width_mm", "Length_mm", "Height_mm"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(columns_data)

print(f"CSV file '{OUTPUT_CSV}' created with {len(columns_data)} columns.")
