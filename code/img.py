import math


def blend_normal(dst: float, dst_a: float, src: float, src_a: float):
    """standard alpha: (out, out_a)"""
    out = src * src_a + dst * (1 - src_a)
    out_a = src_a + dst_a * (1 - src_a)
    return out, out_a


def intensity_to_digit(val: float) -> str:
    """0=white, 1=black -> '0'..'9'"""
    v = max(0.0, min(1.0, val))
    return str(int(round(v * 9)))


def ascii_art_from_grid(grid: list[list[float]]) -> str:
    return "\n".join("".join(intensity_to_digit(v) for v in row) for row in grid)


class Layer:
    def __init__(self, intensity_fn, alpha_fn=None, blend_mode="normal"):
        self.intensity_fn = intensity_fn
        self.alpha_fn = alpha_fn if alpha_fn else (lambda i, j: 1.0)
        self.blend_mode = blend_mode


class RasterImage:
    def __init__(self, width: int, height: int):
        self.w, self.h = width, height
        self.layers: list[Layer] = []

    def add_layer(self, layer: Layer):
        self.layers.append(layer)

    def render(self) -> list[list[float]]:
        canvas = [[0.0] * self.w for _ in range(self.h)]
        alpha_canvas = [[0.0] * self.w for _ in range(self.h)]
        for layer in self.layers:
            for j in range(self.h):
                for i in range(self.w):
                    a = layer.alpha_fn(i, j)
                    if a <= 0:
                        continue
                    src = layer.intensity_fn(i, j)
                    dst, dst_a = canvas[j][i], alpha_canvas[j][i]
                    out, out_a = blend_normal(dst, dst_a, src, a)
                    canvas[j][i], alpha_canvas[j][i] = out, out_a
        return canvas


class Circle:
    def __init__(self, cx, cy, r, fill_intensity=1.0):
        self.cx, self.cy, self.r, self.fill_intensity = cx, cy, r, fill_intensity

    def contains(self, x, y) -> bool:
        return math.hypot(x - self.cx, y - self.cy) <= self.r


class VectorImage:
    def __init__(self, width: float, height: float):
        self.w, self.h = width, height
        self.layers: list[tuple[list[object], float, str]] = []

    def add_layer(self, shapes: list[object], alpha=1.0, blend="normal"):
        self.layers.append((shapes, alpha, blend))

    def rasterize(self, target_w: int, target_h: int, samples: int = 1) -> list[list[float]]:
        grid = [[0.0] * target_w for _ in range(target_h)]
        alpha_grid = [[0.0] * target_w for _ in range(target_h)]
        step = 1.0 / samples
        offset = step / 2.0

        for shapes, layer_alpha, blend in self.layers:
            for j in range(target_h):
                for i in range(target_w):
                    acc_intensity, acc_alpha = 0.0, 0.0
                    for sj in range(samples):
                        for si in range(samples):
                            x = (i + offset + si * step) * (self.w / target_w)
                            y = (j + offset + sj * step) * (self.h / target_h)
                            src, found = 0.0, False
                            for shape in shapes:
                                if isinstance(shape, Circle) and shape.contains(x, y):
                                    src = shape.fill_intensity
                                    found = True
                            if found:
                                out, out_a = blend_normal(0.0, 0.0, src, layer_alpha)
                                acc_intensity += out
                                acc_alpha += out_a

                    avg_intensity = acc_intensity / (samples * samples)
                    avg_alpha = acc_alpha / (samples * samples)
                    dst, dst_a = grid[j][i], alpha_grid[j][i]
                    out, out_a = blend_normal(dst, dst_a, avg_intensity, avg_alpha)
                    grid[j][i], alpha_grid[j][i] = out, out_a
        return grid


if __name__ == "__main__":
    W, H = 10, 10
    cx, cy = 5, 5
    r_outer, r_inner = 3.0, 2.5

    raster = RasterImage(W, H)
    raster.add_layer(Layer(lambda i, j: 0.0, lambda i, j: 1.0))
    raster.add_layer(
        Layer(
            lambda i, j: 1.0 if math.hypot(i + 0.5 - cx, j + 0.5 - cy) <= r_outer else 0.0,
            lambda i, j: 1.0 if math.hypot(i + 0.5 - cx, j + 0.5 - cy) <= r_outer else 0.0,
        )
    )
    raster.add_layer(
        Layer(
            lambda i, j: 0.0,
            lambda i, j: 1.0 if math.hypot(i + 0.5 - cx, j + 0.5 - cy) <= r_inner else 0.0,
        )
    )

    print("Raster (10x10):")
    print(ascii_art_from_grid(raster.render()))

    vector = VectorImage(W, H)
    vector.add_layer([Circle(cx, cy, 1000.0, 0.0)], alpha=1.0)
    vector.add_layer([Circle(cx, cy, r_outer, 1.0)], alpha=1.0)
    vector.add_layer([Circle(cx, cy, r_inner, 0.0)], alpha=1.0)

    print("\nVector rasterized 10x10 (samples=1):")
    print(ascii_art_from_grid(vector.rasterize(10, 10, samples=1)))

    print("\nVector rasterized 10x10 (samples=4):")
    print(ascii_art_from_grid(vector.rasterize(10, 10, samples=4)))
