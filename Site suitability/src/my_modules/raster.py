class Raster:
    """Raster class represents a matrix."""
    
    
    def __init__(self,environment,name):
        """
        Initialize the Raster object.

        Parameters
        ----------
        environment : list
            A 2D grid representing the raster data.
        name : str
            A descriptive name for the raster.

        Returns
        -------
        None.

        """
        self.environment=environment
        self.name=name
        self.rows=len(self.environment)
        self.cols=len(self.environment[0])
        
    def multiply(self,weight):
        """
        Multiplies each cell in the raster by the given weight and returns a new Raster instance.

        Parameters
        ----------
        weight : float
            The weight to multiply each cell by.

        Returns
        -------
        Object
            A new Raster instance with the multiplied values.

        """
        a=[]
        for r in range(self.rows):
            b=[]
            for c in range(self.cols):
                b.append(self.environment[r][c]*weight)
            a.append(b)
        return Raster(a,'weight')
    
    def normalize(self):
        """
        Normalizes the raster data by scaling the values to the range [0, 255]

        Returns
        -------
        None.

        """
        min_val = min(map(min, self.environment))
        max_val = max(map(max, self.environment))
        
        for r in range(self.rows):
            for c in range(self.cols):
                if min_val!=max_val:
                    self.environment[r][c] = int((self.environment[r][c] - min_val) / (max_val - min_val) * 255)
                     
       
    @staticmethod
    def add_rasters(dem_list):
        """
        Adds the corresponding cells of a list of Raster instances and returns a new Raster instance.
        If the dimensions of the rasters do not match, returns None.

        Parameters
        ----------
        dem_list : list
            A list of Raster instances to be added.

        Returns
        -------
        Object
            A new Raster instance with the sum of the input rasters, or None if dimensions do not match.

        """
        if len(dem_list) == 0:
            return None
        rows = len(dem_list[0].environment)
        cols = len(dem_list[0].environment[0])
        for d in dem_list:
            if len(d.environment) != rows or len(d.environment[0]) != cols:
                return None
        result = [[0 for c in range(cols)] for r in range(rows)]
        for d in dem_list:
            for r in range(rows):
                for c in range(cols):
                    result[r][c] += d.environment[r][c]
        return Raster(result, 'sum')
       
                
