import csv


def read_data(f):
    """
    Reading data from the local 

    Parameters
    ----------
    f : str
        File address.

    Returns
    -------
    data : list
        File data.
    n_rows : number
        number of rows.
    n_cols : number
        number of cols.

    """
    # Read input data
    f = open(f, newline='')
    data = []
    for line in csv.reader(f, quoting=csv.QUOTE_NONNUMERIC):
        row = []
        for value in line:
            row.append(value)
            #print(value)
        data.append(row)
    f.close()
    
    # n_rows=len(row)
    # n_cols=len(data)
    return data

def write_data(address,data):
    """
    Writing to local 


    Parameters
    ----------
    address : str
        File address.
    data : list
        File data.

    Returns
    -------
    None.

    """
    f = open(address, 'w', newline='')
    writer = csv.writer(f, delimiter=',')
    for row in data:
        writer.writerow(row) # List of values.
    f.close()