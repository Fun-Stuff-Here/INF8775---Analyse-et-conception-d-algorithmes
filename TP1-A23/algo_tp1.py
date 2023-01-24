import numpy as np

def conv(mat1, mat2, size):
    mat1 = np.linalg.inv(mat1)
    matRes = np.empty([size,size])
    lineRes = np.empty([size])
    res = 0
    for iColMat1 in range(len(mat1)):
        for iLineMat2 in range(len(mat2)):
            for index in range(len(mat1[iColMat1])):
                res += mat1[iColMat1][index] * mat2[iLineMat2][index]
            
            lineRes = np.insert(lineRes, iLineMat2, res)

        matRes = np.insert(matRes, iColMat1, lineRes)
    
    return matRes
        

