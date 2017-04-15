项目 | 内容
---|---
标题 | DllMaker
目录 | Github
标签 | Github、dll-maker、DllMaker
备注 | [GitHub](https://github.com/laijingfeng/DllMaker)
创建 | 2016-12-25
更新 | 2017-04-15 14:41:05

[TOC]

# 使用

给定代码文件，设置版本号，一键生成Dll文件

## 步骤

- 代码放到code目录，只会拿里边的`.cs`文件
- 依赖的dll放到dll目录，只会拿`.dll`和`.DLL`文件
- 执行`run_工程名_版本号_是否编辑器用.py`
    - 示例：
        - `run_JerryDebug_2016-12-26-00_none.py`
        - `run_JerryDebug_2016-12-26-00_UNITY_EDITOR-UNITY_IOS.py`

代码里的宏要用正向的，例如：

```
#if UNITY_EDITOR
    a;
#elif UNITY_ANDROID
    b;
#else
    a;
#endif

#if UNITY_ANDROID && !UNITY_EDITOR
    b;
#else
    a;
#endif

编辑器Android平台，应该是a，但是dll中第二种写法会检测为b
```

# 说明

## 介绍

- code 要编译成Dll的代码放到该目录下
- dll 要编译成Dll的代码依赖的其他Dll放到该目录下
- project 编译过程中形成的工程在该目录下
    - build_log.log 编译日志
    - `bin/Release` 最终编译好的Dll会在这里
- template 构建编译工程用到的模板
- `dll_maker.log/dll_maker-prev.log` 操作日志
- `run_xx_xx_xx.py` 启动脚本
- `logger.py` log辅助脚本

## 背景

一个库工程主体是以下几个文件：
- `xx.sln`
    - 启动工程 
- `xx.csproj`
    - Dll依赖项
    - 代码文件注册
    - 条件编译符号
- `AssemblyInfo.cs`
    - 版本号
    - Dll输出名字

设定的替换变量：
- `PROJECT_NAME` 工程名
- `BUILD_DATE` 版本号