import os
import sys
from astroquery.sdss import SDSS

## M/(10**7 M_☉) = 1.9*[s/(200 km/s)]**5.1

query = """
SELECT TOP 100
    specObjID, z, velDisp, velDispErr
FROM SpecObj
WHERE 
    class = 'GALAXY'          -- Ensure we are getting galaxies
    AND z < 0.1               -- Your redshift constraint
    AND z > 0                 -- Remove any potential bad data/erroneous 0s
    AND zwarning = 0          -- Only reliable measurements
    AND velDisp > 70           -- Ensure velocity dispersion was actually measured
    AND velDispErr<10         -- Ensure the estimates are somewhat accurate
    AND velDisp!=850         -- Remove the upper limit placeholder for velocity dispersion
"""
def fetch_data(output_path=None):
    if output_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, 'datatr', 'my_data.csv')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    results = SDSS.query_sql(query)
    results.write(output_path, format='csv', overwrite=True)
    print(f'Data saved to: {output_path}')
    return output_path


def main():
    csv_path = fetch_data()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    import actual_code
    actual_code.main(data_path=csv_path)


if __name__ == '__main__':
    main()
