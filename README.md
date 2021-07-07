# DRFdeepinto

**DRFTutorial**这个项目学习了DRF官方的教程，然后我发现通过这个教程并不能做成真正的RESTFUL
API，然后我决定去实现，于是便出现了这个深入学习的**DRFdeepinto**项目。通过这个项目的学习和
了解我们能做成真正的RESTFUL API。

但是，却会出现很多的SQL语句查询，按照SQL优化最基本的思想是，一个接口尽量发送一条SQL语句就能
给出最终的数据，为了实现RESTFUL 规范，我使用了很多违反性能的怪异方法。但是，当我开始修改来提
升性能的时候，我想了下，这只不过是一个用来学习DRF使用的，可以说成是《DRF RESTful API设计与实践》
的随书代码。所以没有必要去做性能优化。

至于性能优化，我想应该重新启动一个新的项目，这个项目可以用来表现非资深DRF使用者可能会出现的一些
问题。

设计一个商城的api:
```
api/v1/     api root
api/v1/users/  返回用户列表，也可以get,post
api/v1/users/用户id/ 根据用户id返回该用户的详细信息，也可以put,patch,delete

api/v1/categories/ 返回分类列表,也可以get,post
api/v1/categories/分类id/ 根据分类id返回该分类的相信信息，也可以put,patch,delete
api/v1/categories/分类id/goods/ 返回该分类id的所有产品信息,也可以post,get
api/v1/categories/分类id/goods/产品id/ 返回产品id的相信信息，也可以put,patch,delete
api/v1/categories/分类id/goods/产品id/goods_images/ 返回该分类id，产品id下的所有图片信息,也可以get,post
api/v1/categories/分类id/goods/产品id/goods_images/产品图片id/ 返回该产品图片id的详细信息，也可以put,patch,delete
api/v1/categories/分类id/goods/产品id/goods_videos/ 返回该分类id，产品id下的所有视频信息,也可以get,post
api/v1/categories/分类id/goods/产品id/goods_videos/产品视频id/ 返回该产品视频id的详细信息，也可以put,patch,delete
```

目前代码能实现上面的逻辑。但是

存在的问题：
```
api/v1/categories/分类id/goods/产品id/goods_videos/产品视频id/ 返回该产品视频id的详细信息，也可以put,patch,delete
```

比如说上面这个请求，其中产品id和分类id可以乱填，只要产品视频id填对，都可以返回正确的信息。说明存在问题。
这里明显需要校验参数。

另外还存在一个多次发送sql的性能问题。

最后，由于写的代码量有一点多了，有些地方还不能碰，一碰，整个桥就塌了可能会的感觉，所以，我决定不改了，留着。

虽然我知道怎么去改，但是我不想去碰这份代码了。算是我深入学习了下这个DRF框架。

**通过这个项目的编写，只是学会了如何用DRF去实现功能**。但是性能优化还需要去通过下一个项目的演练才能真正的
让DRF能在工作中使用上。

另外，需要去感谢stackoverflow上的提问者和回答者，没有它们我可能探索不到这里。

❤️非常感谢你们！❤️