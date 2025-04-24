# -*- coding: utf-8 -*-
"""
Original credit to Conner and Mengjie, and Dylan for initial refactor + J0

Refactored on Mon Nov 25 13:36:57 2024

@author: Brent Thompson
"""

import matplotlib.pyplot as plt
#import file_management as fm
#import image as pvim
#import rawpy as rp
import numpy as np
import math


def validate_pixel_metrics_pair(el_pair):
    """
    Creates a list of ordered dictionaries of metadata for a pair of EL images
    used for pixel-level metrics. The function expects one low-current
    (0.1 Isc) and one high-current (1 Isc) image in .NEF format.

    Parameters
    ----------
    EL_images : list of str(filepaths)
        Filepaths to the EL images provided.

    Returns
    -------
    list
        A list of metadata dictionaries for EL images used during analysis
    """

    pixel_metrics_pair = el_pair
    if len(pixel_metrics_pair) == 2 and [i for i in pixel_metrics_pair if i.endswith(".NEF")]:
        for filename in pixel_metrics_pair:
            #EL_metadata = fm.get_filename_metadata(filename, 'el')
          #  EL_metadata["filename"] = filename
            if pixel_metrics_pair['tenth_isc']['current'] > pixel_metrics_pair['one_isc']['current']:
                pixel_metrics_pair.reverse()

        return pixel_metrics_pair
    else:
        print("Too many images selected or not NEF images, please try again.")
        exit(77)


def process_EL_images_for_pixel_analysis(pixel_metrics_pair):
    """
    Processes EL images to prepare data for pixel-level analysis, including
    extracting gridpoints, perspective correction, calibrating images,
    and parsing cell-level data.

    Parameters
    ----------
    pixel_metrics_pair : list of dictionaries
        Contains metadata for the low-current and High-current images.

    Returns
    -------
    dict
        A dictionary containing processed image data, metadata, and constants.
    """
"""
    el_metadata = pvim.FSEC_data_formatting(EL_images)
    low_current_filepath = pixel_metrics_pair[0]['filename']
    high_current_filepath = pixel_metrics_pair[1]['filename']

    # Processed images are used for opencv functions
    processed_low_current = rp.imread(low_current_filepath).postprocess()
    processed_high_current = rp.imread(high_current_filepath).postprocess()

    # Get Corners, Gridpoints, Cell-Iv-Data, Calibration Constant
    corners = pvim.get_module_corners(processed_high_current, manual=False)
    gridpoints = pvim.extract_gridpoints(corners, cell_columns, cell_rows)

    cell_iv_data = pvim.EL_sweep_analysis(
        EL_metadata=el_metadata,
        gridpoints=gridpoints,
        percent=0.01,
        bit_depth=14,
        image_32F=False)
    calibration_constant, highest_pixels = pvim.calibration(
        processed_low_current, gridpoints, el_metadata['voltage'][0], 14)

    # Raw images used for image.py functions
    raw_low_current = rp.imread(low_current_filepath).raw_image
    raw_high_current = rp.imread(high_current_filepath).raw_image

    # Perspective Correction and extracting cells

    raw_low_current = pvim.perspective_correction(
        raw_low_current, corners, orientation='landscape')
    raw_high_current = pvim.perspective_correction(
        raw_high_current, corners, orientation='landscape')

    corners = pvim.get_boundary_corners(raw_high_current)

    gridpoints = pvim.extract_gridpoints(corners, cell_columns, cell_rows)

    low_current_cells = pvim.cell_parsing(raw_low_current, gridpoints)
    high_current_cells = pvim.cell_parsing(raw_high_current, gridpoints)

    # Add arrays to appropriate metadata dictionary
    pixel_metrics_pair[0]['raw_low'] = raw_low_current
    pixel_metrics_pair[0]['processed_low'] = processed_low_current
    pixel_metrics_pair[0]['low_current_cells'] = low_current_cells

    pixel_metrics_pair[1]['raw_high'] = raw_high_current
    pixel_metrics_pair[1]['processed_high'] = processed_high_current
    pixel_metrics_pair[1]['high_current_cells'] = high_current_cells

    pixel_metrics_processed_object = {}
    pixel_metrics_processed_object['0.1Isc Image'] = pixel_metrics_pair[0]
    pixel_metrics_processed_object['1Isc Image'] = pixel_metrics_pair[1]
    pixel_metrics_processed_object['Cell_Iv_Data'] = cell_iv_data
    pixel_metrics_processed_object['Calibration_Cst'] = calibration_constant
    pixel_metrics_processed_object['Highest_Pixels'] = highest_pixels

    return pixel_metrics_processed_object

"""

def calculate_pixel_metrics(pixel_metrics_processed_object):
    """
    Calculates pixel-level metrics, including series resistance (Rs) and dark
    saturation current density (J0), for each photovoltaic cell in the EL
    images. These metrics are computed based on high and low current EL images

    Parameters
    ----------
    pixel_metrics_processed_object : dict
        A dictionary containing processed EL image data, including:
        - Low and high current cells (pixel data)
        - Cell IV data
        - Calibration constant

    Returns
    -------
    Values at the pixel level
    rs_values : list of numpy arrays
        Series resistance values for each cell, in ohms per cm²
    j0_values : list of numpy arrays
        Dark saturation current density values for each cell, in fA per cm²
    """

    vt = 25.85e-3

    # Construct data structure to contain metrics values
    # Redundant calls to data for clarity and readability
    low_current_cells = pixel_metrics_processed_object[
        '0.1Isc Image']['low_current_cells']
    high_current_cells = pixel_metrics_processed_object[
        '1Isc Image']['high_current_cells']
    cell_iv_data = pixel_metrics_processed_object['Cell_Iv_Data']
    calibration_constant = pixel_metrics_processed_object['Calibration_Cst']

    rs_values = [cell.astype(float) for cell in high_current_cells]
    j0_values = [cell.astype(float) for cell in high_current_cells]
    low_pixel_voltages = [cell.astype(float) for cell in high_current_cells]
    high_pixel_voltages = [cell.astype(float) for cell in high_current_cells]

    def pixel_level_calculations():
        """
   Performs pixel-level calculations for a specific pixel (i, j) within a cell
   to compute high and low injection pixel voltages, series resistance (Rs),
   and dark saturation current density (J0).

   Parameters
   ----------
   i : int
       Row index of the pixel within the cell.
   j : int
       Column index of the pixel within the cell.
   cell_number : int
       Index of the current cell being processed.
   high_current_cell : numpy array
       Pixel data for the high-current EL image of the cell.
   low_current_cell : numpy array
       Pixel data for the low-current EL image of the cell.
   calibration_constant : float
       Calibration constant used for voltage calculations.
   vt : float
       Thermal voltage constant.
   cell_high_voltage : float
       Maximum voltage for the high-current IV data.
   cell_high_current_distributed : float
       Distributed high-current density (mA/cm²).
   cell_low_current_distributed : float
       Distributed low-current density (mA/cm²).
   high_pixel_voltages : list of numpy arrays
       List storing high-injection pixel voltages for each cell.
   low_pixel_voltages : list of numpy arrays
       List storing low-injection pixel voltages for each cell.
   rs_values : list of numpy arrays
       List storing series resistance values for each cell.
   j0_values : list of numpy arrays
       List storing dark saturation current density values for each cell.
      """

        high_pixel_voltages[cell_number][i][j] = np.log(
            high_current_cell[i][j] / calibration_constant) * vt

        # Calculate pixel voltage for low injection image of cell
        low_pixel_voltages[cell_number][i][j] = np.log(
            low_current_cell[i][j] / calibration_constant) * vt

        # Series resistance distribution in ohms per cm^2
        rs_values[cell_number][i][j] = (
            (cell_high_voltage - high_pixel_voltages[
                cell_number][i][j]) * 1000) / cell_high_current_distributed

        # Dark saturation current density (J0) in fA per cm^2
        j0_values[cell_number][i][j] = (
            cell_low_current_distributed / math.exp(low_pixel_voltages[
                cell_number][i][j] / (vt))) * 10e12

    for cell_number, (high_current_cell, low_current_cell) in enumerate(
            zip(high_current_cells, low_current_cells)):

        # cell_high - voltage and current for Rs
        # cell_low - current for J0
        cell_high_voltage = max(cell_iv_data[:, 1, cell_number])
        cell_high_current = max(cell_iv_data[:, 0, cell_number])
        cell_low_current = min(cell_iv_data[:, 0, cell_number])
        print(cell_number)

        # Getting J_distributed [mA/cm2]
        cell_high_current_distributed = cell_high_current / (cell_area) * 1000
        cell_low_current_distributed = cell_low_current / (cell_area) * 1000

        # Iterate through each i,j pixel in cell number cell_number
        for i in range(high_current_cell.shape[0]):
            for j in range(high_current_cell.shape[1]):
                pixel_level_calculations()

    return rs_values, j0_values


def map_pixel_metrics(rs_values, j0_values):  # TODO For data visualization lib
    """
    Generates spatial visualizations for pixel-level metrics (Rs and J0)
    derived from EL image analysis. The function maps series resistance (Rs)
    and dark saturation current density (J0) values across the photovoltaic
    module and saves the results as images.

    Parameters
    ----------
    Values at the pixel level
    rs_values : list of numpy arrays
        Series resistance values for each cell, in ohms per cm².
    j0_values : list of numpy arrays
        Dark saturation current density values for each cell, in fA per cm².

    Returns
    -------
    Plots saved at the target destination

    int
        Returns 0 to indicate successful execution.
    """
    figures = []

    units = {'rs': '$R_S$ (ohm⋅$cm^2$)', 'j0': '$J_0$ (fA/$cm^2$)'}

    for pixel_data, datatype in zip((rs_values, j0_values), ('rs', 'j0')):

        # Remove infinite values
        for i, cell in enumerate(pixel_data):
            cell[cell == np.inf] = 0
            cell[cell < 0] = 0
            pixel_data[i] = cell

        # build module image
        module_image = []
        for row_i in range(0, cell_rows):
            row = np.hstack(
                pixel_data[row_i*cell_columns:(row_i+1)*cell_columns])
            module_image.append(row)
        module_image = np.vstack(module_image)

        # Display and save figure plots
        mean_values = np.mean(module_image[module_image > 0])
        standard_deviation = np.std(module_image[module_image > 0])

        if datatype == 'rs':
            vmin = mean_values - 3*standard_deviation
            vmax = mean_values + 3*standard_deviation
            plt.imshow(module_image, cmap='inferno', vmin=vmin, vmax=vmax)
        else:
            x = 3
            vmin = mean_values - x*standard_deviation
            while vmin < 0:
                x = x - 0.25
                vmin = mean_values - x*standard_deviation

            vmax = mean_values + 1*standard_deviation
            plt.imshow(module_image, cmap='inferno', vmin=vmin, vmax=vmax)

        cbar = plt.colorbar()
        cbar.ax.tick_params(
            color='k', labelcolor='k')
        cbar.set_label(
            units[datatype], rotation=270, color='k', labelpad=20)
        figures.append([f"{datatype}", plt])
        #plt.savefig(f"{dst}/spatial-{datatype}.jpg",
                    #bbox_inches='tight', pad_inches=0.1, dpi=600)
        #plt.close()

    return figures

# These values can be pulled from module metadata soon
# TODO add calls to database to pull x, y, cell area data


cell_area = float(243.36)
cell_columns = 12
cell_rows = 6


# Demonstration
"""
EL_images = fm.get_files(
    "Select the 2 files to be used: (Select 1Isc and 0.1 Isc of same module.)")

dst = fm.get_dir()

# Check that required images are present and properly formatted
pixel_metrics_pair = create_pixel_metrics_pair(EL_images)

# Build data structure containing all required data and metadata
pixel_metrics_processed_object = process_EL_images_for_pixel_analysis(
    pixel_metrics_pair)

# Run analysis on dataset
rs_values, j0_values = calculate_pixel_metrics(
    pixel_metrics_processed_object)

# Save and display plots
figures = map_pixel_metrics(rs_values, j0_values)
"""