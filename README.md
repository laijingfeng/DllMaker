项目 | 内容
---|---
标题 | DllMaker
目录 | Github
标签 | Github、dll-maker、DLLMaker
备注 | [GitHub](https://github.com/laijingfeng/DllMaker)
创建 | 2016-12-25
更新 | 2017-08-09 11:22:12

[TOC]

# 说明

给定代码文件，设置版本号，一键生成DLL文件

# 使用步骤

- 代码放到code目录，只会拿里边的`.cs`文件
- 依赖的DLL放到dll目录，只会拿`.dll`和`.DLL`文件
- 执行`run_工程名_版本号_附加的宏.py`
    - 注意：
        - 第一次使用需要配置正确的VS编译器路径：`devenv_path = 'E:\Program Files\VS2010\Common7\IDE\devenv.com'` 
    - 示例：
        - `run_JerryDebug_2016-12-26-00_none.py` 没有附加宏
        - `run_JerryDebug_2016-12-26-00_UNITY_EDITOR-UNITY_IOS.py`
- 看`project/build_log.log`是否说明编译成功
- 到`project/bin/Release`取编译的DLL

**注意**：代码里的宏要用正向的，例如：

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

> 备注：如果想要打包各种各样的小份DLL互相依赖，考虑到一个DLL分成了多平台，接下来派生出来的DLL都要多平台了，因此，建议尽量避免用太多平台宏

# 补充

## 项目结构

- code 要编译成DLL的代码放到该目录下
- dll 要编译成DLL的代码依赖的其他DLL放到该目录下
- project 编译过程中形成的工程在该目录下
    - build_log.log 编译日志
    - `bin/Release` 最终编译好的DLL会在这里
- template 构建编译工程用到的模板
- `dll_maker.log/dll_maker-prev.log` 操作日志
- `run_xx_xx_xx.py` 启动脚本
- `logger.py` log辅助脚本

## VS工程解析

一个库工程主体是以下几个文件：
- `xx.sln`
    - 启动工程 
- `xx.csproj`
    - DLL依赖项
    - 代码文件注册
    - 条件编译符号
- `AssemblyInfo.cs`
    - 版本号
    - DLL输出名字

设定的替换变量：
- `PROJECT_NAME` 工程名
- `BUILD_DATE` 版本号