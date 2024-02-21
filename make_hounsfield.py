import numpy as np
import nibabel as nib

# Define image dimensions
dim_x, dim_y, dim_z = 14, 14, 14

# Generate voxel intensities as float32
voxel_intensities = np.arange(-1024, 1720, dtype=np.float32)

# Reshape voxel intensities to match image dimensions
voxel_intensities = voxel_intensities.reshape((dim_x, dim_y, dim_z))

# Create NIfTI image with float32 data type
nifti_image = nib.Nifti1Image(voxel_intensities, np.eye(4), dtype=np.float32)

# Save NIfTI image to file
nib.save(nifti_image, 'hounsfield.nii')