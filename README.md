# Manual to run the GBSeparation algorithm for leaf-wood separation

The GBSeparation folder was downloaded in july 2023 from https://zenodo.org/record/6837613. Some slight modification have been done.

## Steps
### Get the code

1. Download this Github repo. OR download the original code (rar file on https://zenodo.org/record/6837613) and unzip, and download the GBS_demo.py file from this repo.

### Set a conda environment
There are some environment requirements to be able to run the code
* Python 3.7 and above (The code is compatible with Python 3.7);
* Other 3rd party packages (numpy, networkx,sklearn,open3d ...).

Therefore you should make a new conda environment:

1. Open Anaconda Prompt 
2. Run 

    ```conda create --name GBSeparation python=3.7```

3. Activate this environment

    ```conda activate GBSeparation```

4. Install the required packages (numpy, open3d, networkx, scikit-learn, laspy)
    ``` 
    conda install -c anaconda numpy
    conda install -c open3d-admin open3d
    conda install -c anaconda networkx
    conda install -c anaconda scikit-learn 
    conda install -c conda-forge laspy
    conda install -c conda-forge matplotlib
    pip install pillow==9.0.0
    ```

### Input data requirements
There are also some data requirements to be able to run the code
* The input data should be a single tree 3D point cloud and no large gaps in existence.
* The input tree data should be in .pcd, .txt, .las or .ply format

### Run the code
1. Modify the GBS_demo.py file by chaning the input and output paths to your paths:
    ```
    # the input files path
    pathin = "F:/EUCFACE/trees/" #change to your input folder 
    # the output files path
    outpath = "F:/EUCFACE/leaf-wood/wood/" #change to your output folder
    ```
2. Navigate to the folder where the GBSeparation folder is at: 

    ```cd ….```
3. Run the GBS_demo script: 

    ```python GBS_demo.py```
4. Check the separation results which should appear in your output folder.

### Tips
* Downsampling and filtering (for reflectance) before running GBSeparation can improve the results.