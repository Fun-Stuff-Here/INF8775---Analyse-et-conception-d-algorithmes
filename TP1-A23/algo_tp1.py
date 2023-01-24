import numpy as np

def conv(mat1, mat2, size):
    mat1 = np.transpose(mat1)
    matRes = np.empty([size,size])
    for iColMat1 in range(len(mat1)):
        for iLineMat2 in range(len(mat2)):
            res = 0
            
            for index in range(len(mat1[iColMat1])): 
                res += mat1[iColMat1][index] * mat2[iLineMat2][index]
            
            matRes[iColMat1, iLineMat2] = res
    
    return matRes
        

