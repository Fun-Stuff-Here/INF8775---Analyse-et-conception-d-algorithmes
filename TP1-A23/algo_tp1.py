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






def strassen(mat1, mat2, size):

    if size == 1:
        return np.array([[mat1[0][0] * mat2[0][0]]])
    mid_point = size//2
    A11 = mat1[0:mid_point, 0:mid_point]
    A12 = mat1[0:mid_point, mid_point:size]
    A21 = mat1[mid_point:size, 0:mid_point]
    A22 = mat1[mid_point:size, mid_point:size]
    B11 = mat2[0:mid_point, 0:mid_point]
    B12 = mat2[0:mid_point, mid_point:size]
    B21 = mat2[mid_point:size, 0:mid_point]
    B22 = mat2[mid_point:size, mid_point:size]

    M1 = strassen(A11 + A22, B11 + B22, mid_point)
    M2 = strassen(A21 + A22, B11, mid_point)
    M3 = strassen(A11, B12 - B22, mid_point)
    M4 = strassen(A22, B21 - B11, mid_point)
    M5 = strassen(A11 + A12, B22, mid_point)
    M6 = strassen(A21 - A11, B11 + B12, mid_point)
    M7 = strassen(A12 - A22, B21 + B22, mid_point)

    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6

    return np.concatenate((np.concatenate((C11, C12), axis=1), np.concatenate((C21, C22), axis=1)), axis=0)


def strassenSeuil(mat1, mat2, size, seuil=1):
    if size <= seuil:
        return conv(mat1, mat2, size)
