��Ŀ | ����
---|---
���� | DllMaker
Ŀ¼ | Github
��ǩ | Github��dll-maker��DLLMaker
��ע | [GitHub](https://github.com/laijingfeng/DllMaker)
���� | 2016-12-25
���� | 2017-08-09 11:22:12

[TOC]

# ˵��

���������ļ������ð汾�ţ�һ������DLL�ļ�

# ʹ�ò���

- ����ŵ�codeĿ¼��ֻ������ߵ�`.cs`�ļ�
- ������DLL�ŵ�dllĿ¼��ֻ����`.dll`��`.DLL`�ļ�
- ִ��`run_������_�汾��_���ӵĺ�.py`
    - ע�⣺
        - ��һ��ʹ����Ҫ������ȷ��VS������·����`devenv_path = 'E:\Program Files\VS2010\Common7\IDE\devenv.com'` 
    - ʾ����
        - `run_JerryDebug_2016-12-26-00_none.py` û�и��Ӻ�
        - `run_JerryDebug_2016-12-26-00_UNITY_EDITOR-UNITY_IOS.py`
- ��`project/build_log.log`�Ƿ�˵������ɹ�
- ��`project/bin/Release`ȡ�����DLL

**ע��**��������ĺ�Ҫ������ģ����磺

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

�༭��Androidƽ̨��Ӧ����a������dll�еڶ���д������Ϊb
```

> ��ע�������Ҫ������ָ�����С��DLL�������������ǵ�һ��DLL�ֳ��˶�ƽ̨������������������DLL��Ҫ��ƽ̨�ˣ���ˣ����龡��������̫��ƽ̨��

# ����

## ��Ŀ�ṹ

- code Ҫ�����DLL�Ĵ���ŵ���Ŀ¼��
- dll Ҫ�����DLL�Ĵ�������������DLL�ŵ���Ŀ¼��
- project ����������γɵĹ����ڸ�Ŀ¼��
    - build_log.log ������־
    - `bin/Release` ���ձ���õ�DLL��������
- template �������빤���õ���ģ��
- `dll_maker.log/dll_maker-prev.log` ������־
- `run_xx_xx_xx.py` �����ű�
- `logger.py` log�����ű�

## VS���̽���

һ���⹤�����������¼����ļ���
- `xx.sln`
    - �������� 
- `xx.csproj`
    - DLL������
    - �����ļ�ע��
    - �����������
- `AssemblyInfo.cs`
    - �汾��
    - DLL�������

�趨���滻������
- `PROJECT_NAME` ������
- `BUILD_DATE` �汾��