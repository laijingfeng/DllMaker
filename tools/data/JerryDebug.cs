using UnityEngine;
using System.Collections.Generic;
using System.IO;
using System;
using System.Collections;
using System.Reflection;
using System.Text;

public class JerryDebug : MonoBehaviour
{
    #region 配置

    /// <summary>
    /// 输出到屏幕
    /// </summary>
    private static bool m_OutScreen =
#if UNITY_EDITOR
        false;
#else
        true;
#endif

    /// <summary>
    /// 输出到文件
    /// </summary>
    private static bool m_OutFile =
#if UNITY_EDITOR
        false;
#else
        true;
#endif

    /// <summary>
    /// 输出到控制台
    /// </summary>
    private static bool m_OutConsole =
#if UNITY_EDITOR
        true;
#else
        false;
#endif

    /// <summary>
    /// 刷新OnGUI
    /// </summary>
    private static bool m_DoOnGUI = false;

    /// <summary>
    /// 单类最大日志量
    /// </summary>
    private const int MAX_MSG_CNT = 100;

    /// <summary>
    /// 是否启用
    /// </summary>
    private static bool m_Active = true;

    /// <summary>
    /// <para>是否接收消息</para>
    /// <para>可以暂停接收消息</para>
    /// </summary>
    private static bool m_ReceiveMsg = true;

    /// <summary>
    /// 多余日志按时间顺序删除
    /// </summary>
    private static bool m_LogDeleteByTime = true;

    /// <summary>
    /// LOG文件目录
    /// </summary>
    private static string LOG_FILE_PATH = 
#if UNITY_EDITOR
        Application.dataPath + "/../JerryDebug.txt";
#else
        Application.persistentDataPath + "/JerryDebug.txt";
#endif

    /// <summary>
    /// 按原始类型输出的类型，其他当做结构
    /// </summary>
    private static List<string> m_OriginalTypes = new List<string>()
    {
        "System.String",//string
        "System.Int32",//int
        "System.Single",//float
    };

    #endregion 配置

    #region 变量

    private static int m_CntInfo = 0;
    private static int m_CntWarning = 0;
    private static int m_CntError = 0;

    /// <summary>
    /// 单例
    /// </summary>
    private static JerryDebug m_instance = null;

    /// <summary>
    /// Log类型
    /// </summary>
    private enum LogType
    {
        /// <summary>
        /// 信息
        /// </summary>
        Info = 0,

        /// <summary>
        /// 警告
        /// </summary>
        Warning = 1,

        /// <summary>
        /// 错误
        /// </summary>
        Error = 2,
    }

    /// <summary>
    /// 消息信息
    /// </summary>
    private class MsgInfo
    {
        public string m_strMessage;
        public LogType m_logType;
    }

    public class ExtenActionConfig
    {
        public string name;
        public Action action;
    }

    /// <summary>
    /// 消息列表
    /// </summary>
    private static List<MsgInfo> m_listMsgList = new List<MsgInfo>();

    /// <summary>
    /// Log面板当前浏览进度
    /// </summary>
    private Vector2 m_vtScrollView = Vector2.zero;

    /// <summary>
    /// 低端控制按钮高度
    /// </summary>
    private float m_oneHeight = 22f;

    /// <summary>
    /// 是否显示最新的
    /// </summary>
    private bool m_ShowNewer = false;

    /// <summary>
    /// 是否显示帮助
    /// </summary>
    private bool m_Help = false;

    /// <summary>
    /// 是否显示错误
    /// </summary>
    private bool m_ShowError = true;

    /// <summary>
    /// 是否显示警告
    /// </summary>
    private bool m_ShowWarning = true;

    /// <summary>
    /// 是否显示普通信息
    /// </summary>
    private bool m_ShowInfo = true;

    /// <summary>
    /// 窗口大小
    /// </summary>
    private static Rect m_rect = new Rect(0, 0, Screen.width * 0.5f + 15, Screen.height * 0.5f);

    /// <summary>
    /// 帮助面板大小
    /// </summary>
    private Rect m_recHelp = new Rect(Screen.width * 0.5f + 15, 0, Screen.width * 0.5f - 15, Screen.height * 0.5f);

    #endregion 变量

    void Start()
    {
        if (System.IO.File.Exists(LOG_FILE_PATH))
        {
            File.Delete(LOG_FILE_PATH);
        }
    }

    #region 对外接口

    /// <summary>
    /// LOG
    /// </summary>
    /// <param name="msg"></param>
    /// <param name="type"></param>
    /// <param name="isProtoMsg"></param>
    public static void LogInfo(object msg, bool isProtoMsg = false)
    {
        AddLog(msg, LogType.Info, isProtoMsg);
    }

    /// <summary>
    /// LOG
    /// </summary>
    /// <param name="msg"></param>
    /// <param name="type"></param>
    /// <param name="isProtoMsg"></param>
    public static void LogWarn(object msg, bool isProtoMsg = false)
    {
        AddLog(msg, LogType.Warning, isProtoMsg);
    }

    /// <summary>
    /// LOG
    /// </summary>
    /// <param name="msg"></param>
    /// <param name="type"></param>
    /// <param name="isProtoMsg"></param>
    public static void LogError(object msg, bool isProtoMsg = false)
    {
        AddLog(msg, LogType.Error, isProtoMsg);
    }

    #endregion 对外接口

    #region Proto消息处理

    private static string m_CurMsg;

    private static string HandleProtoMsg(object obj)
    {
        m_CurMsg = string.Empty;
        
        AndMsgLine("************* Begin: " + obj + "*************");
        PrintProperties(obj, 1);
        AndMsgLine("************* End: " + obj + "*************");

        return m_CurMsg;
    }

    private static void AndMsgLine(object msg)
    {
        m_CurMsg += (string.IsNullOrEmpty(m_CurMsg) ? "" : "\n") + msg;
    }

    private static void PrintProperties(object obj, int indent)
    {
        if (obj == null)
        {
            return;
        }

        string indentString = new string(' ', indent * 3);
        Type objType = obj.GetType();
        PropertyInfo[] properties = objType.GetProperties();

        if (properties != null
            && properties.Length > 0)
        {
            AndMsgLine(string.Format("{0}", new string(' ', (indent - 1) * 3)) + "{");
        }

        //列表特判
        if (objType.Name.Equals("List`1"))
        {
            AndMsgLine(indentString + obj.ToString().Replace("System.Collections.Generic.List`1", "list") + " Count = " + ((IList)obj).Count + " :");
            PrintList((IList)obj, indent + 1);
        }
        else
        {
            foreach (PropertyInfo property in properties)
            {
                //找ProtoBuf.ProtoMemberAttribute属性标记的
                Attribute attri = Attribute.GetCustomAttribute(property, typeof(ProtoBuf.ProtoMemberAttribute));
                if (attri == null)
                {
                    continue;
                }

                object propValue = property.GetValue(obj, null);

                if (propValue is IList)//列表
                {
                    AndMsgLine(indentString + property.Name + " Count = " + ((ICollection)propValue).Count + " :");
                    PrintList((IList)propValue, indent + 1);
                }
                else if (property.PropertyType.Assembly == objType.Assembly
                    && property.PropertyType.IsEnum == false)//新的结构
                {
                    AndMsgLine(indentString + property.Name + ": " + propValue);
                    PrintProperties(propValue, indent + 1);
                }
                else
                {
                    AndMsgLine(indentString + property.Name + ": " + propValue);
                }
            }
        }

        if (properties != null
            && properties.Length > 0)
        {
            AndMsgLine(string.Format("{0}", new string(' ', (indent - 1) * 3)) + "}");
        }
    }

    /// <summary>
    /// 输出List
    /// </summary>
    /// <param name="list"></param>
    /// <param name="indent"></param>
    private static void PrintList(IList list, int indent)
    {
        if (list == null)
        {
            return;
        }

        int i = 0;
        foreach (object o in list)
        {
            string indentString = new string(' ', indent * 3);
            indentString += "--";
            AndMsgLine(indentString + o + "[" + i + "]");
            PrintProperties(o, indent + 1);
            i++;
        }
    }

    #endregion Proto消息处理

    /// <summary>
    /// AddLog
    /// </summary>
    /// <param name="msg"></param>
    /// <param name="logType"></param>
    /// <param name="isProtoMsg"></param>
    private static void AddLog(object msg, LogType logType = LogType.Info, bool isProtoMsg = false)
    {
        if (!Application.isPlaying || m_Active == false || m_ReceiveMsg == false)
        {
            return;
        }

        string strMessage = string.Empty;
        
        if(isProtoMsg)
        {
            strMessage = HandleProtoMsg(msg);
        }
        else
        {
            strMessage = HandleInfo(msg); 
        }
        
        if (m_instance == null)
        {
            GameObject go = new GameObject("JerryDebug");
            m_instance = go.AddComponent<JerryDebug>();
            DontDestroyOnLoad(go);
        }

        if (m_OutScreen == true)
        {
            AddToScreen(strMessage, logType);
        }

        if (m_OutFile == true)
        {
            AddToFile(strMessage);
        }

        if(m_OutConsole)
        {
            AddToConsole(strMessage, logType);
        }
    }

    #region 输出到文件处理

    private static List<string> m_MsgToFile = new List<string>();

    /// <summary>
    /// 增加到文件输出
    /// </summary>
    /// <param name="strMsg"></param>
    private static void AddToFile(string strMsg)
    {
        m_MsgToFile.Add(System.DateTime.Now.ToString("HH:mm:ss") + " : " + strMsg);
    }

    void Update()
    {
        //因为写入文件的操作必须在主线程中完成，所以在Update中哦给你写入文件。
        if (m_MsgToFile.Count > 0)
        {
            string[] temp = m_MsgToFile.ToArray();
            foreach (string t in temp)
            {
                using (StreamWriter writer = new StreamWriter(LOG_FILE_PATH, true, Encoding.UTF8))
                {
                    writer.WriteLine(t);
                }
                m_MsgToFile.Remove(t);
            }
        }
    }

    #endregion 输出到文件处理

    #region 输出到屏幕处理

    private static void AddToScreen(string strMessage, LogType logType)
    {
        #region CheckCnt

        if (m_LogDeleteByTime)
        {
            if (m_CntWarning + m_CntInfo + m_CntError >= MAX_MSG_CNT * 3)
            {
                MsgInfo mi = m_listMsgList[0];
                if (mi != null)
                {
                    m_listMsgList.Remove(mi);
                    switch (mi.m_logType)
                    {
                        case LogType.Info:
                            {
                                m_CntInfo--;
                            }
                            break;
                        case LogType.Warning:
                            {
                                m_CntWarning--;
                            }
                            break;
                        case LogType.Error:
                            {
                                m_CntError--;
                            }
                            break;
                    }
                }
            }
        }
        else
        {
            switch (logType)
            {
                case LogType.Warning:
                    {
                        while (m_CntWarning >= MAX_MSG_CNT)
                        {
                            MsgInfo mi = m_listMsgList.Find((x) => x.m_logType == LogType.Warning);
                            if (mi != null)
                            {
                                m_listMsgList.Remove(mi);
                                m_CntWarning--;
                            }
                            else
                            {
                                break;
                            }
                        }
                    }
                    break;
                case LogType.Info:
                    {
                        while (m_CntInfo >= MAX_MSG_CNT)
                        {
                            MsgInfo mi = m_listMsgList.Find((x) => x.m_logType == LogType.Info);
                            if (mi != null)
                            {
                                m_listMsgList.Remove(mi);
                                m_CntInfo--;
                            }
                            else
                            {
                                break;
                            }
                        }
                    }
                    break;
                case LogType.Error:
                    {
                        while (m_CntError >= MAX_MSG_CNT)
                        {
                            MsgInfo mi = m_listMsgList.Find((x) => x.m_logType == LogType.Error);
                            if (mi != null)
                            {
                                m_listMsgList.Remove(mi);
                                m_CntError--;
                            }
                            else
                            {
                                break;
                            }
                        }
                    }
                    break;
            }
        }

        #endregion

        switch (logType)
        {
            case LogType.Info:
                {
                    m_CntInfo++;
                }
                break;
            case LogType.Warning:
                {
                    m_CntWarning++;
                }
                break;
            case LogType.Error:
                {
                    m_CntError++;
                }
                break;
        }

        m_listMsgList.Add(new MsgInfo()
        {
            m_strMessage = System.DateTime.Now.ToString("HH:mm:ss") + "：\n" + strMessage,
            m_logType = logType,
        });
    }

    #endregion 输出到屏幕处理

    #region 输出到Console处理

    private static void AddToConsole(string strMessage, LogType logType)
    {
        switch (logType)
        {
            case LogType.Info:
                {
                    UnityEngine.Debug.Log(strMessage);
                }
                break;
            case LogType.Warning:
                {
                    UnityEngine.Debug.LogWarning(strMessage);
                }
                break;
            case LogType.Error:
                {
                    UnityEngine.Debug.LogError(strMessage);
                }
                break;
        }
    }

    #endregion 输出到Console处理

    private static string HandleInfo(object obj)
    {
        System.Type t = obj.GetType();
        foreach (string s in m_OriginalTypes)
        {
            if (t.ToString().Equals(s))
            {
                return obj.ToString();
            }
        }
        return JsonUtility.ToJson(obj, true);
    }

    #region GUI处理

    void OnGUI()
    {
        if (m_Active == false || m_DoOnGUI == false)
        {
            return;
        }

        m_rect = GUI.Window(0, m_rect, RefreshUI, "JerryDebug");
        if (m_Help)
        {
            m_recHelp.x = m_rect.x + m_rect.width;
            m_recHelp.y = m_rect.y;
            GUI.Window(1, m_recHelp, RefreshHelp, "Setting");
        }
        FillBottomCtr();
    }

    #region 扩展

    /// <summary>
    /// 填充下面操作
    /// </summary>
    private void FillBottomCtr()
    {
        GUI.color = Color.green;
        if (GUI.Button(new Rect(m_rect.x, m_rect.y + m_rect.height, m_rect.width * 0.5f, m_oneHeight), "Help"))
        {
            m_Help = !m_Help;
        }
        GUI.color = Color.white;

        if (GUI.Button(new Rect(m_rect.x + m_rect.width * 0.5f, m_rect.y + m_rect.height, m_rect.width * 0.5f, m_oneHeight), "Clear"))
        {
            m_listMsgList.Clear();
            m_CntError = 0;
            m_CntInfo = 0;
            m_CntWarning = 0;
        }
    }

    public static List<ExtenActionConfig> CtrAction = new List<ExtenActionConfig>();
    
    /// <summary>
    /// 填充控制面板
    /// </summary>
    private void FillCtrButton()
    {
        GUI.color = Color.green;

        int idx = 0;
        foreach (ExtenActionConfig config in CtrAction)
        {
            if (idx % 3 == 0)
            {
                GUILayout.BeginHorizontal();
            }

            if (config != null && config.action != null)
            {
                if (GUILayout.Button(config.name))
                {
                    if (config.action != null)
                    {
                        config.action();
                    }
                }
            }

            if (idx % 3 == 2)
            {
                GUILayout.EndHorizontal();
            }
            idx++;
        }
        if (idx % 3 != 0)
        {
            GUILayout.EndHorizontal();
        }

        GUI.color = Color.white;
    }

    #endregion 扩展

    private void RefreshHelp(int iWindowID)
    {
        GUILayout.BeginVertical();

        GUILayout.BeginHorizontal();
        m_ReceiveMsg = GUILayout.Toggle(m_ReceiveMsg, "ReceiveMsg");
        GUILayout.EndHorizontal();

        GUILayout.BeginHorizontal();

        GUI.color = Color.white;
        m_ShowNewer = GUILayout.Toggle(m_ShowNewer, "ToBottom");
        GUI.color = Color.white;

        GUI.color = Color.white;
        m_LogDeleteByTime = GUILayout.Toggle(m_LogDeleteByTime, "DeleteByTimeOrType");
        GUI.color = Color.white;

        GUILayout.EndHorizontal();

        GUILayout.BeginHorizontal();

        GUI.color = Color.white;
        m_ShowInfo = GUILayout.Toggle(m_ShowInfo, "Info");
        GUI.color = Color.white;

        GUI.color = Color.yellow;
        m_ShowWarning = GUILayout.Toggle(m_ShowWarning, "Warn");
        GUI.color = Color.white;

        GUI.color = Color.red;
        m_ShowError = GUILayout.Toggle(m_ShowError, "Error");
        GUI.color = Color.white;

        GUILayout.EndHorizontal();

        FillCtrButton();

        GUILayout.EndVertical();
    }

    /// <summary>
    /// 刷新信息
    /// </summary>
    private void RefreshUI(int iWindowID)
    {
        float width = Screen.width * 0.5f;
        float height = Screen.height * 0.5f;
        float width1 = 15, height1 = 30;
        GUI.DragWindow(new Rect(0, 0, width - width1 - 10, height));
        GUI.DragWindow(new Rect(width, 0, 15, height));
        if (m_ShowNewer)
        {
            m_vtScrollView.y = 10000f;
        }
        m_vtScrollView = GUILayout.BeginScrollView(m_vtScrollView, GUILayout.Width(width - width1), GUILayout.Height(height - height1));
        for (int i = 0, imax = m_listMsgList.Count; i < imax; i++)
        {
            if (!IsShow(m_listMsgList[i].m_logType))
            {
                continue;
            }
            GUI.color = GetColor(m_listMsgList[i].m_logType);
            GUI.skin.box.alignment = TextAnchor.UpperLeft;
            GUI.skin.box.wordWrap = true;
            GUILayout.Box(m_listMsgList[i].m_strMessage);
        }
        GUILayout.EndScrollView();
    }

    private Color GetColor(LogType type)
    {
        Color cc = Color.white;
        switch (type)
        {
            case LogType.Info:
                {
                    cc = Color.white;
                }
                break;
            case LogType.Warning:
                {
                    cc = Color.yellow;
                }
                break;
            case LogType.Error:
                {
                    cc = Color.red;
                }
                break;
        }
        return cc;
    }

    private bool IsShow(LogType type)
    {
        if (m_ShowError && type == LogType.Error)
        {
            return true;
        }
        if (m_ShowWarning && type == LogType.Warning)
        {
            return true;
        }
        if (m_ShowInfo && type == LogType.Info)
        {
            return true;
        }
        return false;
    }

    #endregion GUI处理
}