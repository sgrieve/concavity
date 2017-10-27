import rasterio

with rasterio.open('tmpfiles/ndvs_final.tif', 'r+') as r:
    arr = r.read()

    # Cs
    arr[arr == 9] = 8

    # Cw
    arr[arr == 12] = 11
    arr[arr == 13] = 11

    # Cf
    arr[arr == 15] = 14
    arr[arr == 16] = 14

    # Ds
    arr[arr == 18] = 17
    arr[arr == 19] = 17
    arr[arr == 20] = 17

    # Dw
    arr[arr == 22] = 21
    arr[arr == 23] = 21
    arr[arr == 24] = 21

    # Df
    arr[arr == 26] = 25
    arr[arr == 27] = 25
    arr[arr == 28] = 25

    r.write(arr)
