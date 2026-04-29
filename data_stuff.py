import astropy as ap
import astroquery as aq

## M/(10**7 M_☉) = 1.9*[s/(200 km/s)]**5.1

from astroquery.sdss import SDSS

# The SQL Query
# We select redshift, velocity dispersion, and some ID info for context
query = """
SELECT TOP 500
    specObjID, z, velDisp, velDispErr
FROM SpecObj
WHERE 
    class = 'GALAXY'          -- Ensure we are getting galaxies
    AND z < 0.01               -- Your redshift constraint
    AND z > 0                 -- Remove any potential bad data/erroneous 0s
    AND zwarning = 0          -- Only reliable measurements
    AND velDisp > 70           -- Ensure velocity dispersion was actually measured
    AND velDispErr<10         -- Ensure the estimates are somewhat accurate
    AND velDisp!=850         -- Remove the upper limit placeholder for velocity dispersion
"""

# Execute the query
result = SDSS.query_sql(query)

result.write('my_data.csv', format='csv', overwrite=True)
print("Data saved!")
