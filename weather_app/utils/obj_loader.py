def load_obj(file_path):
    vertices = []
    texcoords = []
    normals = []
    faces = []

    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.strip().split()
                vertices.append(tuple(map(float, parts[1:4])))
            elif line.startswith('vt '):
                parts = line.strip().split()
                texcoords.append(tuple(map(float, parts[1:3])))
            elif line.startswith('vn '):
                parts = line.strip().split()
                normals.append(tuple(map(float, parts[1:4])))
            elif line.startswith('f '):
                parts = line.strip().split()[1:]
                face = []
                for p in parts:
                    vals = p.split('/')
                    v_idx = int(vals[0]) - 1
                    vt_idx = int(vals[1]) - 1 if len(vals) > 1 and vals[1] != '' else None
                    vn_idx = int(vals[2]) - 1 if len(vals) > 2 and vals[2] != '' else None
                    face.append((v_idx, vt_idx, vn_idx))
                faces.append(face)

    return vertices, texcoords, normals, faces
