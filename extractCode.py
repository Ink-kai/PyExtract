import os
import sys
from shutil import copyfile

from pyinstxtractor import PyInstArchive

MAGIC_HEAD = b'o\r\r\n\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
exe_dir = os.getcwd()
source_dir = os.path.join(exe_dir,'sourceCode')
backup_dir = os.path.join(exe_dir, 'backup')


def dispose_dir(directory: str):
    if not os.path.exists(directory):
        sys.stderr.write(f"Directory {directory} Privileges Error.")
        return
    if not os.path.isdir(directory):
        sys.stderr.write(f"Directory {directory} Error.")
        return

    count = 0
    extract_Folder = None
    main_name = None
    main_name = directory.split(".exe_extracted")[0]

    # if os.path.exists(os.path.join(directory,"PYZ-00.pyz_extracted")):
    #     walk_dir=os.path.join(directory,"PYZ-00.pyz_extracted")
    # else:
    #     walk_dir=directory
    global source_dir
    global backup_dir
    source_dir = directory+'_sourceCode'
    backup_dir = directory+'backup'
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.find(main_name):
                if dispose_file(os.path.join(root, file)):
                    count += 1
    sys.stdout.write(f"[*] Usage: Total {count} files to extract.")


def dispose_file(file_path: str):
    # 存在?
    if not os.path.exists(file_path):
        sys.stderr.write(f"FILE {file_path} Privileges Error.")
        return

    # 文件名称
    file_name = os.path.basename(file_path).split(".pyc")[0]
    # 文件所在目录
    current_dir = os.path.dirname(file_path)
    content = None

    os.makedirs(source_dir, exist_ok=True)
    with open(file_path, "rb") as o_f:
        o_f.seek(os.SEEK_SET)
        if o_f.read(os.SEEK_CUR) == b'\xe3':
            sys.stdout.write(f"MAGIC NUMBER Not Found,Auto repair.\n")
            o_f.seek(os.SEEK_SET)
            content = o_f.read()
        o_f.seek(12)
        if o_f.read(os.SEEK_CUR) == b'\xe3':
            o_f.seek(12)
            content = o_f.read()
            sys.stdout.write(f"MAGIC NUMBER Not Found,Auto repair.\n")

    if content:
        new_file = file_path
        # 备份源文件
        os.makedirs(backup_dir, exist_ok=True)
        try:
            copyfile(file_path, os.path.join(backup_dir, os.path.basename(file_path)))
            sys.stdout.write(f"Backup {file_path} to {backup_dir}")
        except Exception as e:
            sys.stderr.write(f"Backup File Error: {e}\n")

        with open(new_file, "wb") as n_f:
            n_f.seek(os.SEEK_SET)
            new_content = MAGIC_HEAD + content
            n_f.write(new_content)
    generate_py_file = os.path.join(source_dir, file_name + ".py")
    exec_convert_cmd = "pycdc %s -o %s" % (file_path, generate_py_file)
    try:
        exec_res = os.popen(exec_convert_cmd).read()
    except Exception as e:
        sys.stderr.write(f"Convert Fail.",e)
    if not exec_res:
        sys.stdout.write(f"convert {file_path} to {generate_py_file}\n")
        sys.stdout.write("Execute convert cmd successful.\n")
        return True
    else:
        sys.stdout.write("[ERROR]: Execute convert cmd filed, please check it.\n")
        return False


def dispose_exe_file(exe_path):
    # 存在?
    if not os.path.exists(exe_path):
        sys.stderr.write(f"FILE {exe_path} Privileges Error.")
        return
    arch = PyInstArchive(sys.argv[1])
    if arch.open():
        if arch.checkFile():
            if arch.getCArchiveInfo():
                arch.parseTOC()
                arch.extractFiles()
                arch.close()
                print('[*] Successfully extracted pyinstaller archive: {0}'.format(sys.argv[1]))
                print('')
                print('You can now use a python decompiler on the pyc files within the extracted directory')
        arch.close()
    # extracted_dir = os.path.join(os.getcwd())
    # dispose_dir(extracted_dir)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        print("current dir:",exe_dir)
        if os.path.isdir(sys.argv[1]):
            dispose_dir(sys.argv[1])
        elif os.path.isfile(sys.argv[1]) and os.path.basename(sys.argv[1]).endswith(".exe"):
            dispose_exe_file(sys.argv[1])
        elif os.path.isfile(sys.argv[1]) and os.path.basename(sys.argv[1]).endswith(".pyc"):
            dispose_file(sys.argv[1])
        else:
            sys.stderr.write('[*] Usage: invalid parameter value.')
    else:
        sys.stderr.write('[*] Usage: extract.exe <filename>/<directory>/*.exe')
