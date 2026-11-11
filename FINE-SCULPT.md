# 人物与佛像细雕更新

本次在保留原始 GLB 的基础上生成 refined 版本，并接入 src/scene.js。

人物：眼睑、鼻翼、唇形、耳廓、发丝及盘髻纹理、领口金纹、服装褶皱、腰扣花丝、裙边纹样、手指关节。13个动画节点的局部变换与原始版完全一致。男模型31290三角面/710776字节，女模型34498三角面/813248字节；维持每角色31个网格与材质分组。

佛像：闭目眼睑、鼻翼与唇部轮廓、耳部内侧曲线、螺发刻线、袈裟滚边细纹、莲座珠圈及花瓣刻纹。所有7种GLB已检查加载、法线、PBR材质、落地位置和原始尺度；每个佛像新增2个合并后的细节材质组。主像约1.82MB；其他模型约0.51–1.05MB，简化坐像约0.67MB。

美术源：reference-visitors-refined.blend、buddha-fine-sculpt.blend。
预览：reference-visitors-refined-closeup.png、reference-visitors-refined-glb-verified.png、buddha-fine-sculpt-preview.png。
原始资产全部保留，网站使用 refined 文件名避免旧缓存。

验证：人物合掌及步行关节测试通过；七种佛像导出加载及边界测试通过；正式构建通过。浏览器确认全部9份细雕GLB已载入，无错误日志。手机实体设备性能未测试。
