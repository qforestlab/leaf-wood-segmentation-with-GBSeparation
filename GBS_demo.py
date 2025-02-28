import datetime
import numpy as np
import open3d as o3d
import networkx as nx
from GBSeparation.Graph_Path import array_to_graph, extract_path_info
from GBSeparation.LS_circle import getRootPt
from GBSeparation.ExtractInitWood import extract_init_wood
from GBSeparation.ExtractFinalWood import extract_final_wood
import os
import laspy

# the input files path
pathin = "C:/Users/lmterryn/GBS_test/in/" #change to your input folder 
# the output files path
outpath = "C:/Users/lmterryn/GBS_test/out/"  #change to your output folder

files = os.listdir(pathin)

for i in range(0, len(files)):
    filename = files[i]
    out_name = filename.split('.')[0]
    format_pc = filename.split('.')[-1]

    # load single tree point cloud.
    if format_pc == 'txt':
        pcd = o3d.io.read_point_cloud(pathin + filename, format = 'xyz')
        pcd = np.asarray(pcd.points)
    elif format_pc == 'las':
        pcd = laspy.read(pathin + filename)
        pcd = np.vstack((pcd.x, pcd.y, pcd.z)).transpose()
    else: #pcd, ply
        pcd = o3d.io.read_point_cloud(pathin + filename, format = format_pc)
        pcd = np.asarray(pcd.points)

    # Please ensure that the growth direction of the tree is parallel to the Z coordinate axis.
    treeHeight = np.max(pcd[:, 2])-np.min(pcd[:, 2])

    # fit the root point.
    root, fit_seg = getRootPt(pcd, lower_h=0.0, upper_h=0.2)
    pcd = np.append(pcd, root, axis=0)
    root_id = pcd.shape[0]-1
    print("root_ID:", root_id)
    # show_pcd(pcd)

    # construct networkx Graph.
    print(str(datetime.datetime.now()) + ' | >>>constructing networkx Graph...')
    G = array_to_graph(pcd, root_id, kpairs=3, knn=300, nbrs_threshold=treeHeight/30, nbrs_threshold_step=treeHeight/60)

    # # save/read already constructed Graph to reduce processing time.
    print(">>>connected components of constructed Graph: ", nx.number_connected_components(G))
    # show_graph(pcd, G)

    # extract path info information from graph
    print(str(datetime.datetime.now()) + ' | >>>extracting shortest path information...')
    path_dis, path_list = extract_path_info(G, root_id, return_path=True)
    # show_graph(pcd, sp_graph(path_list, root_id))

    # extract initial wood points.
    print(str(datetime.datetime.now()) + ' | >>>extracting initial wood points...')
    init_wood_ids = extract_init_wood(pcd, G, root_id, path_dis, path_list,
                                  split_interval=[0.1, 0.2, 0.3, 0.5, 1], max_angle=0.15*np.pi)

    # extract final wood points.
    print(str(datetime.datetime.now()) + ' | >>>extracting final wood points...')
    final_wood_mask = extract_final_wood(pcd, root_id, path_dis, path_list, init_wood_ids, G)

    # remove the inserted root point and extract wood/leaf points by mask index.
    final_wood_mask[-1] = False
    wood = pcd[final_wood_mask]
    final_wood_mask[-1] = True
    leaf = pcd[~final_wood_mask]

    # write separation result with .txt format.
    np.savetxt(outpath+out_name+"_wood"+".txt", wood, fmt='%1.6f')
    np.savetxt(outpath+out_name+"_leaf"+".txt", leaf, fmt='%1.6f')