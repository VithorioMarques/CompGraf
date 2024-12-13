import sys
import open3d as o3d

class PLYRenderer:
    def __init__(self, path):
        self.path = path

    def renderizar_ply(self):
        try:
            mesh = o3d.io.read_triangle_mesh(self.path)
            if not mesh.is_empty():
                o3d.visualization.draw_geometries([mesh])
        except:
            pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    renderer = PLYRenderer(sys.argv[1])
    renderer.renderizar_ply()
