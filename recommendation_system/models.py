from django.db import models
import numpy as np
from scipy.sparse import csr_matrix
import io
# Create your models here.
class TfidfMatrixModel(models.Model):
    data = models.BinaryField()

    def save_matrix(self, matrix):
        self.data = matrix_to_binary(matrix)
        self.save()

    def get_matrix(self):
        return binary_to_matrix(self.data)
    
def matrix_to_binary(matrix):
    # Tạo một đối tượng file-like trong bộ nhớ
    with io.BytesIO() as memfile:
        # Lưu trữ ma trận sparse dưới dạng file nén
        np.savez_compressed(memfile, data=matrix.data, indices=matrix.indices, indptr=matrix.indptr, shape=matrix.shape)
        # Lấy nội dung nhị phân từ file-like
        memfile.seek(0)
        return memfile.read()

def binary_to_matrix(binary_data):
    # Tạo một đối tượng file-like từ dữ liệu nhị phân
    with io.BytesIO(binary_data) as memfile:
        with np.load(memfile) as loader:
            matrix = csr_matrix(
                (loader['data'], loader['indices'], loader['indptr']),
                shape=loader['shape']
            )
    return matrix