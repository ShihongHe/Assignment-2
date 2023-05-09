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
        #Define a list of all zeros with the same dimension
        result = [[0 for c in range(self.cols)] for r in range(self.rows)]
        #Traversing the list
        for r in range(self.rows):
            for c in range(self.cols):
                result[r][c]+=self.environment[r][c]*weight
        return Raster(result,'multiply')
    
    def normalize(self):
        """
        Normalizes the raster data by scaling the values to the range [0, 255]

        Returns
        -------
        None.

        """
        #Find maximum and minimum values
        min_val = min(map(min, self.environment))
        max_val = max(map(max, self.environment))
        #Traversing the list
        for r in range(self.rows):
            for c in range(self.cols):
                #Constant when maximum and minimum values are the same, standardised when different
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
        #Get the number of rows and columns
        rows = len(dem_list[0].environment)
        cols = len(dem_list[0].environment[0])
        #Define a list of all zeros with the same dimension
        result = [[0 for c in range(cols)] for r in range(rows)]
        #Iterate through the list of all documents
        for d in dem_list:
            for r in range(rows):
                for c in range(cols):
                    result[r][c] += d.environment[r][c]
        return Raster(result, 'Site suitability')
    
    @staticmethod
    def check_dimensions(rasters):
        """
        Check if all the rasters in the list have the same dimensions.

        Parameters
        ----------
        rasters : list
            A list of Raster instances.

        Returns
        -------
        bool
            True if all rasters have the same dimensions, False otherwise.

        """
        #Determine if it is empty
        if not rasters:
            return False
        first_raster = rasters[0]
        for raster in rasters[1:]:
            #Determine if the number of rows and columns are the same
            if raster.rows != first_raster.rows or raster.cols != first_raster.cols:
                return False
        return True
    
    
    def check_data_integrity(self):
        """
        Checks the integrity of the raster data.

        Returns
        -------
        bool
            True if the raster data is valid, False otherwise.
        """
        #Check if self.environment is a non-empty list
        if not isinstance(self.environment, list) or len(self.environment) == 0:
            return False
        
        #Check that each row of the matrix is a list and of the same length
        row_length = len(self.environment[0])
        if not all(isinstance(row, list) and len(row) == row_length for row in self.environment):
            return False
        
        # Check if each element of the matrix is an integer or a floating point number
        for row in self.environment:
            if not all(isinstance(value, (int, float)) for value in row):
                return False
            
        # If all the above conditions are met, return True
        return True
                
