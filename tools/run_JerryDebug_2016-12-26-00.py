#! /usr/bin/env python
#coding=utf-8
#version: 2016-12-26-00

import sys, os
import shutil
from logger import Logger

logger = Logger(Logger.LEVEL_INFO, 'dll_maker')

def NotClean(fname, pattern):
    for p in pattern:
        if fname.find(p) != -1:
            return True
    return False

def DoClean(path, pattern):
    for f in os.listdir(path):
        if NotClean(f, pattern) == True:
            continue
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
    with open('template.sln', 'r') as f:
        text = f.read()
        text = Replace(text,'{PROJECT_NAME}', project_name)
    with open('{}.sln'.format(project_name),'w') as f:
        f.write(text)

def CopyBuildFiles(sDir, tDir):
    for f in os.listdir(sDir):
        if f.find('.meta') != -1: # 去除Unity的meta文件
            continue
        sf = os.path.join(sDir, f)
        tf = os.path.join(tDir, f)
        if os.path.isfile(sf):
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
            ret = ret + '\n    <Reference Include="' + os.path.splitext(os.path.split(f)[1])[0] + '">\n     <HintPath>' + sf + '</HintPath>\n    </Reference>'
        if os.path.isdir(sf):
            ret = ret + GetDLLFiles(sf)
    return ret

def GetBuildFiles(path, path2):
    ret = ''
    for f in os.listdir(path):
        if f.find('.meta') != -1: # 去除Unity的meta文件
            continue
        sf = os.path.join(path, f)
        sf2 = os.path.join(path2, f)
        if os.path.isfile(sf):
            ret = ret + '\n    <Compile Include="' + sf2 + '" />'
        if os.path.isdir(sf):
            ret = ret + GetBuildFiles(sf, sf2)
    return ret

def DoCsproj(project_name):
    text = ''
    buld_files = GetBuildFiles('data', '')
    dll_files = GetDLLFiles('DLL')
    
    with open('template.csproj', 'r') as f:
        text = f.read()
        text = Replace(text,'{PROJECT_NAME}', project_name)
        text = Replace(text,'{BUILD_FILES}', buld_files)
        text = Replace(text,'{DLL_FILES}', dll_files)
    with open('{}.csproj'.format(project_name),'w') as f:
        f.write(text)

def DoAssemblyInfo(project_name, project_version):
    text = ''
    with open('template.cs', 'r') as f:
        text = f.read()
        text = Replace(text,'{PROJECT_NAME}', project_name)
        text = Replace(text,'{BUILD_DATE}', project_version)
    os.makedirs('./Properties')
    with open('Properties/{}.cs'.format('AssemblyInfo'),'w') as f:
        f.write(text)

def ParseArg(argv):
    project_name = ''
    project_version = ''
    
    if len(argv) < 1:
        return False, None
    elif len(argv) == 1:
        file_name = argv[0]
        file_name = os.path.split(file_name)[1]
        file_name = file_name.split('.')[0]

        file_names = file_name.split('_', 2)
        if len(file_names) != 3:
            return False, None
        project_name = file_names[1]
        project_version = file_names[2]
    elif len(argv) == 3:
        project_name = argv[1]
        project_version = argv[2]

    if project_name == '' or project_version == '':
        return False, None
    else:
        project_version = project_version.replace('-','.')
        return True, [project_name, project_version]

def Usage():
    print 'this is Usage()'
    print 'run_XXX_2016-12-26-00.py'
    print 'run.py XXX 2016-12-26-00'

if __name__ == '__main__':
    logger.reset()

    success, args = ParseArg(sys.argv)
    if not success:
        Usage()
        exit(-1)
        
    logger.info('start')
    
    project_name = args[0]
    project_version = args[1]

    DoClean('./', ['.py', 'DLL', '.bat', '.pyc', 'template', 'dll_make', 'data'])

    CopyBuildFiles('data', './')

    DoSln(project_name)
    DoCsproj(project_name)
    DoAssemblyInfo(project_name, project_version)

    os.system('"{}" {}.sln /build Release /out build_log.log'.format('C:\Program Files (x86)\VS2010\Common7\IDE\devenv.com', project_name))

    logger.info('finish')