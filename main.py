import argparse
import sys
import painting
import cv2
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN


if __name__ == "__main__":
    # arguments parse
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', nargs='?', default='imgs/4.jpg')
    parser.add_argument('pcount', nargs='?', default='2')
    parser.add_argument('dbscan', nargs='?', default='no')
    args = parser.parse_args(sys.argv[1:])

    # filepath validate
    img = cv2.imread(args.filepath)
    if img is None:
        exit("This file doesn't exist")

    # count validate
    if not args.pcount.isdigit():
        exit("Wrong count")

    # KMeans and save
    x, y, z = img.shape
    X = img.reshape((x*y, z))
    KM_model = KMeans(n_clusters=int(args.pcount), n_jobs=-1)
    y_KM = KM_model.fit_predict(X)
    new_img = painting.fill_color(X, y_KM).reshape((x, y, z))
    dot_ind = args.filepath.rfind(".")
    new_filename = args.filepath[:dot_ind] + "_kmeans" + args.filepath[dot_ind:]
    painting.draw_picture(new_img, save=True, filename=new_filename)
    # DBSCAN if needed and save
    if args.dbscan == "yes":
        DB_model = DBSCAN(n_jobs=-1)
        y_DB = DB_model.fit_predict(X)
        k = pd.Series(y_DB).nunique()
        print(f"Count of clusters is {k}")
        new_img = painting.fill_color(X, y_DB, dbscan=True).reshape((x, y, z))
        new_filename = args.filepath[:dot_ind] + "_dbscan" + args.filepath[dot_ind:]
        painting.draw_picture(new_img, save=True, filename=new_filename)

    # exit
    input("Done, type any key to exit...")
