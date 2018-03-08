# pybatis
python for mybatis

有时候使用django的过程中,特别是模型交互非常多的情况下,比如跨库,跨表,这个时候我们必须用django 的orm raw方法去做
查询,但是当sql非常多的时候,这些sql就充斥在业务代码中,所以我们会想办法去管理。
鉴于java 的mybatis思想,主要借鉴了其模版化方式管理sql,我觉得非常好,所以做了一个简单的包。目前还在测试阶段,请谨慎使用。