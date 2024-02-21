import sys
import numpy as np
import nibabel as nib

def h2c(img, is_inverse=False):
    """
    Transforms a numeric array (image) using invertible transform.
    Raw CT data uses Hounsfield units based on XRay attenuation where:
    air = -1000 (transparent), water = 0, bone ~1000 (relatively opaque)
    Most soft tissue (gray/white matter, CSF) is in the range 0..50
    In contrast, MR magnitude images only have positive values
    Dynamic range for most MR modalities spans most of the intensity range.
    This 'Hounsfield-To-Cormack' conversion aids tools with MR assumptions.  

    Parameters:
    img (array): A numeric array representing an image.
    is_inverse (bool, optional): Flag to indicate if the inverse transformation
                                 should be applied. Defaults to False.

    Returns:
    array: Transformed numeric array.
    """
    # Constants for value thresholds and scaling
    k_min = -1000
    k_uninteresting_dark_units = 900
    k_interesting_mid_units = 200
    k_scale_ratio = 10
    if is_inverse:
        # Calculate scaled interesting mid units for inverse operation
        k_interesting_mid_units_scaled = k_interesting_mid_units * k_scale_ratio
        # Translate image values and apply boosting to the mid-range
        base = img + k_min
        boost = img - k_uninteresting_dark_units
        boost[boost < 0] = 0
        boost[boost > k_interesting_mid_units_scaled] = k_interesting_mid_units_scaled
        boost = (boost / k_scale_ratio) * (k_scale_ratio - 1)
        return base - boost
    else:
        # Convert image by setting minimum and boosting mid-range values
        img[img < k_min] = k_min
        img = img - k_min
        boost = img - k_uninteresting_dark_units
        boost[boost < 0] = 0
        boost[boost > k_interesting_mid_units] = k_interesting_mid_units
        boost = boost * (k_scale_ratio - 1)
        return img + boost


def modify_nifti(input_file):
    # Load NIfTI image
    nifti_image = nib.load(input_file)

    # Get voxel intensities
    voxel_intensities = nifti_image.get_fdata()

    # Add 1000 to each voxel intensity
    modified_voxels = h2c(voxel_intensities, True)

    # Create a new NIfTI image with modified voxel intensities
    modified_nifti_image = nib.Nifti1Image(modified_voxels, nifti_image.affine, header=nifti_image.header)

    # Save the modified NIfTI image with 'c' prefix
    output_file = 'h' + input_file
    nib.save(modified_nifti_image, output_file)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_nifti_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    modify_nifti(input_file)