AMPLITUDE_MULTIPLIER = 4
X_STEP = 10
GRID_DENSITY = 1

class WaveDeformer:

    def __init__(self, function, xOffset) -> None:
        self.function = function
        self.xOffset = xOffset

    def transform(self, x, y):
        y = y + AMPLITUDE_MULTIPLIER*self.function(self.xOffset + x/X_STEP)
        return x, y

    def transform_rectangle(self, x0, y0, x1, y1):
        return (*self.transform(x0, y0),
                *self.transform(x0, y1),
                *self.transform(x1, y1),
                *self.transform(x1, y0),
                )

    def getmesh(self, img):
        self.w, self.h = img.size
        gridspace = 1

        target_grid = []
        for x in range(0, self.w, gridspace):
            for y in range(0, self.h, gridspace):
                target_grid.append((x, y, x + gridspace, y + gridspace))

        source_grid = [self.transform_rectangle(*rect) for rect in target_grid]

        return [t for t in zip(target_grid, source_grid)]