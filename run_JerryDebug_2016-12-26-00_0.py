#! /usr/bin/env python
#coding=utf-8
#version: 2017-04-01-00

import sys, os
import shutil
from logger import Logger

logger = Logger(Logger.LEVEL_INFO, 'dll_maker')

def DoClean(path):
    for f in os.listdir(path):
        sf = os.path.join(path, f)
        if os.path.isfile(sf):
            os.remove(sf)
        if os.path.isdir(sf):
            shutil.rmtree(sf)

def Replace(text, pattern, target):
    if text.count(pattern) > 0:
        text = text.replace(pattern, target)
    return text

def DoSln(project_name):
    text = ''
    with open('./template/template.sln', 'r') as f:
        text = f.read()
        text = Replace(text,'{PROJECT_NAME}', project_name)
    with open('./project/{}.sln'.format(project_name),'w') as f:
        f.write(text)

def CopyBuildFiles(sDir, tDir):
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
        if os.path.isdir(sf):
            CopyBuildFiles(sf, tf)

def GetDLLFiles(path):
    ret = ''
    for f in os.listdir(path):
        sf = os.path.join(path, f)
        if os.path.isfile(sf):
            if f.find('.dll') != -1 or f.find('.DLL') != -1:
                ret = ret + '\n    <Reference Include="' + os.path.splitext(os.path.split(f)[1])[0] + '">\n     <HintPath>.' + sf + '</HintPath>\n    </Reference>'
        if os.path.isdir(sf):
            ret = ret + GetDLLFiles(sf)
    return ret

def GetBuildFiles(path, path2):
    ret = ''
    for f in os.listdir(path):
        if f.find('.meta') != -1 or f.find('.cs') == -1: # 去除Unity的meta文件，只要CS文件
            continue
        sf = os.path.join(path, f)
        sf2 = os.path.join(path2, f)
        if os.path.isfile(sf):
            ret = ret + '\n    <Compile Include="' + sf2 + '" />'
        if os.path.isdir(sf):
            ret = ret + GetBuildFiles(sf, sf2)
    return ret

def DoCsproj(project_name, is_editor):
    text = ''
    buld_files = GetBuildFiles('./code/', '')
    dll_files = GetDLLFiles('./dll/')
    
    with open('./template/template.csproj', 'r') as f:
        text = f.read()
        out_dll_name = project_name
        if is_editor == '1':
            out_dll_name = out_dll_name + '_Editor'    
        text = Replace(text,'{PROJECT_NAME}', out_dll_name)
        text = Replace(text,'{BUILD_FILES}', buld_files)
        text = Replace(text,'{DLL_FILES}', dll_files)
        if is_editor == '1':
            text = Replace(text,'{DEFINE_CONSTANTS}', 'UNITY_EDITOR')
        else:
            text = Replace(text,'{DEFINE_CONSTANTS}', '')
    with open('./project/{}.csproj'.format(project_name),'w') as f:
        f.write(text)

def DoAssemblyInfo(project_name, project_version):
    text = ''
    with open('./template/AssemblyInfo.cs', 'r') as f:
        text = f.read()
        text = Replace(text,'{PROJECT_NAME}', project_name)
        text = Replace(text,'{BUILD_DATE}', project_version)
    os.makedirs('./project/Properties')
    with open('./project/Properties/{}.cs'.format('AssemblyInfo'),'w') as f:
        f.write(text)

def ParseArg(argv):
    project_name = ''
    project_version = ''
    is_editor = '0'
    
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
        is_editor = file_names[3]
    elif len(argv) == 4:
        project_name = argv[1]
        project_version = argv[2]
        is_editor = argv[3]

    if project_name == '' or project_version == '':
        return False, None
    else:
        project_version = project_version.replace('-','.')
        return True, [project_name, project_version, is_editor]

def Usage():
    print 'this is Usage()'
    print 'run_XXX_2016-12-26-00_0.py'
    print 'run.py XXX 2016-12-26-00 0'

if __name__ == '__main__':
    logger.reset()

    success, args = ParseArg(sys.argv)
    if not success:
        Usage()
        exit(-1)
        
    logger.info('start')
    
    project_name = args[0]
    project_version = args[1]
    is_editor = args[2]
    devenv_path = 'E:\Program Files\VS2010\Common7\IDE\devenv.com' # home
    # 'C:\Program Files (x86)\VS2010\Common7\IDE\devenv.com' # company

    # 清理旧工程
    DoClean('./project/')

    CopyBuildFiles('./code/', './project/')

    DoSln(project_name)
    DoCsproj(project_name, is_editor)
    DoAssemblyInfo(project_name, project_version)

    os.system('"{}" ./project/{}.sln /build Release /out ./project/build_log.log'.format(devenv_path, project_name))

    logger.info('finish')
