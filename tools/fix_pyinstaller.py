import os

'''
The first argument is the location the resource will be available at in the packaged application
and the second is the location of the resource in the source directory.
This is not limited to just images either. Any file can be packaged along with the source code.
a.datas += [('images/icon.ico', 'D:\\[workspace]\\App\\src\\images\\icon.ico',  'DATA')]

# TO USE
Run this scripts, and copy paste output to the *.spec file. Do clean the old fix.
'''

os.chdir("..")
rootdir = os.path.dirname(os.path.realpath(__file__))
prefix_len = len(rootdir) + 1

print("a.datas += [")
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        res = os.path.join(subdir, file)
        if "assets" in res:
            first = res[prefix_len:].replace("\\", "/")
            second = res.replace("\\", "\\\\")
            res_str = "('" + first + "','" + second + "','DATA'),"
            print(res_str)
print("]")