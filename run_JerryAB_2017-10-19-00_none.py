#! /usr/bin/env python
#coding=utf-8
#version: 2017-10-23-00

import sys, os
import shutil
from logger import Logger

logger = ''
enter_cwd_path = ''


def do_clean(path):
    for f in os.listdir(path):
        sf = os.path.join(path, f)
        if os.path.isfile(sf):
            os.remove(sf)
        if os.path.isdir(sf):
            shutil.rmtree(sf)


def do_replace(text, pattern, target):
    if text.count(pattern) > 0:
        text = text.replace(pattern, target)
    return text


def do_sln(project_name):
    text = ''
    with open(get_exe_path('./template/template.sln'), 'r') as f:
        text = f.read()
        text = do_replace(text,'{PROJECT_NAME}', project_name)
    with open('{}{}.sln'.format(get_exe_path('./project/'), project_name), 'w') as f:
        f.write(text)


def copy_build_files(sDir, tDir):
    for f in os.listdir(sDir):
        if f.find('.meta') != -1: # 去除Unity的meta文件
            continue
        sf = os.path.join(sDir, f)
        tf = os.path.join(tDir, f)
        if os.path.isfile(sf):
            if f.find('.cs') == -1: # 只要CS文件
                continue
            if not os.path.exists(tDir):
                os.makedirs(tDir)
            open(tf, 'wb').write(open(sf, 'rb').read())
        elif os.path.isdir(sf):
            copy_build_files(sf, tf)


def get_dll_files(path):
    ret = ''
    for f in os.listdir(path):
        sf = os.path.join(path, f)
        if os.path.isfile(sf):
            if f.find('.dll') != -1 or f.find('.DLL') != -1:
                ret = ret + '\n    <Reference Include="' + os.path.splitext(os.path.split(f)[1])[0] + '">\n     <HintPath>' + sf + '</HintPath>\n    </Reference>'
        elif os.path.isdir(sf):
            ret = ret + get_dll_files(sf)
    return ret


def get_build_files(path, path2):
    ret = ''
    for f in os.listdir(path):
        if f.find('.meta') != -1: # 去除Unity的meta文件
            continue
        sf = os.path.join(path, f)
        sf2 = os.path.join(path2, f)
        if os.path.isfile(sf):
            if f.find('.cs') != -1: # 只要CS文件
                ret = ret + '\n    <Compile Include="' + sf2 + '" />'
        elif os.path.isdir(sf):
            ret = ret + get_build_files(sf, sf2)
    return ret


def do_csproj(project_name, define_str):
    build_files = get_build_files(get_exe_path('./code/'), get_exe_path('./project/'))
    dll_files = get_dll_files(get_exe_path('./dll/'))
    
    with open(get_exe_path('./template/template.csproj'), 'r') as f:
        text = f.read()
        out_dll_name = project_name
        #if define_str != '':
        #    out_dll_name = out_dll_name + '-' + define_str
        text = do_replace(text, '{PROJECT_NAME}', out_dll_name)
        text = do_replace(text, '{BUILD_FILES}', build_files)
        text = do_replace(text, '{DLL_FILES}', dll_files)
        text = do_replace(text, '{DEFINE_CONSTANTS}', define_str.replace('-', ';'))
    with open('{}{}.csproj'.format(get_exe_path('./project/'), project_name), 'w') as f:
        f.write(text)


def do_assembly_info(project_name, project_version):
    text = ''
    with open(get_exe_path('./template/AssemblyInfo.cs'), 'r') as f:
        text = f.read()
        text = do_replace(text,'{PROJECT_NAME}', project_name)
        text = do_replace(text,'{BUILD_DATE}', project_version)
    os.makedirs(get_exe_path('./project/Properties/'))
    with open('{}{}.cs'.format(get_exe_path('./project/Properties/'), 'AssemblyInfo'), 'w') as f:
        f.write(text)


def parse_arg(argv):
    project_name = ''
    project_version = ''
    define_str = ''
    
    if len(argv) < 1:
        return False, None
    elif len(argv) == 1:
        file_name = argv[0]
        file_name = os.path.split(file_name)[1]
        file_name = file_name.split('.')[0]

        file_names = file_name.split('_', 3)
        if len(file_names) != 4:
            return False, None
        project_name = file_names[1]
        project_version = file_names[2]
        define_str = file_names[3]
    elif len(argv) == 4:
        project_name = argv[1]
        project_version = argv[2]
        define_str = argv[3]

    if project_name == '' or project_version == '':
        return False, None
    else:
        if define_str == 'none':
            define_str = ''
        project_version = project_version.replace('-', '.')
        return True, [project_name, project_version, define_str]


def usage():
    print 'this is usage()'
    print 'run_XXX_2016-12-26-00_UNITY_EDITOR-UNITY_IOS.py'
    print 'run_XXX_2016-12-26-00_none.py'
    print 'run.py XXX 2016-12-26-00 UNITY_EDITOR-UNITY_IOS'
    print 'run.py XXX 2016-12-26-00 none'


def get_exe_path(simple_path):
    global enter_cwd_path
    return os.path.join(enter_cwd_path, os.path.dirname(sys.argv[0]), simple_path)

if __name__ == '__main__':
    success, args = parse_arg(sys.argv)
    if not success:
        usage()
        exit(-1)
    enter_cwd_path = os.getcwd()

    logger = Logger(Logger.LEVEL_INFO, get_exe_path('./dll_maker'))
    logger.reset()
    logger.info('start')
    logger.info(enter_cwd_path)

    project_name = args[0]
    project_version = args[1]
    define_str = args[2]
    devenv_path = 'C:\Program Files (x86)\VS2010\Common7\IDE\devenv.com' # company
    # 'E:\Program Files\VS2010\Common7\IDE\devenv.com' # home
    # 'C:\Program Files (x86)\VS2010\Common7\IDE\devenv.com' # company

    # 清理旧工程
    do_clean(get_exe_path('./project/'))

    copy_build_files(get_exe_path('./code/'), get_exe_path('./project/'))

    do_sln(project_name)
    do_csproj(project_name, define_str)
    do_assembly_info(project_name, project_version)

    os.system('"{}" {}{}.sln /build Release /out {}build_log.log'.format(get_exe_path(devenv_path), get_exe_path('./project/'), project_name, get_exe_path('./project/')))

    logger.info('finish')
