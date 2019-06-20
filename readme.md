### 功能 ： 

> httpserver部分
>
> > 获取http请求 
> > 解析http请求
> > 将请求发送给WebFrame
> > 从WebFrame接收反馈数据
> > 将数据组织为Response格式发送给客户端

> WebFrame部分
>
> > 从httpserver接收具体请求
> > 根据请求进行逻辑处理和数据处理
> > 将需要的数据反馈给httpserver

> 特点 
>
> > 采用httpserver和应用处理分离的模式,降低了耦合度
> > 采用了用户配置文件的思路
> > webframe部分采用了模拟后端框架的处理方法

> 技术点
>
> > httpserver部分需要与两端建立通信
> > webFrame部分采用多路复用接收并发请求
> > 数据传递使用json格式