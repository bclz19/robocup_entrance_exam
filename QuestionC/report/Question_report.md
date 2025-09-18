# 环境配置

本程序在ubuntu22.04下经过测试

```
sudo apt install cmake git libzmq3-dev libboost-dev
```
安装BehaviorTree.CPP库

克隆BehaviorTree.CPP：
```
git clone https://github.com/BehaviorTree/BehaviorTree.CPP.git
```
编译：cd BehaviorTree.CPP && mkdir build && cd build && cmake .. && make && sudo make install

至此，环境配置完毕

## 写个示例程序

比如我就写在/QuestionC中

然后我把源代码写在/src里面，然后任务非常简单，就是检查电量CheckBattery，电量大于2，就Move，否则就Recharge。

ok，那怎么做呢？

首先BehaviorTree的树的内容是写在xml里面的，然后用createTreeFromText函数转化成tree，那么这样我们就直接去看xml内容好了，先是定义树的名字叫SimpleTree，然后开始定义节点，首先是根节点，它的类型是Fallback，这是一种控制节点，他按照顺序尝试子节点，如果哪个返回success，就执行，不然就继续。

然后我们来看这个root有哪几个子节点，很明显有两个，然后两个都是sequence，这个同样都是控制节点，这个就是执行全部子节点，然后如果都success就返回success，否则就返回false，然后第一个sequence名字叫做mov_seq，他包括
一个条件节点和一个动作节点，就是检查电量和行动，行动会耗电。然后如果检查电量<2就返回failure，然后就去recharge了。

tree交代如此，具体节点的行为在前面的cpp中有具体实现，不再赘述。然后执行就tick就完事了。

(base) bclz19@utopia:~/QuestionC/build$ ./demo 
=== 最简单行为树启动 ===
[条件] 检查电量: 3
[动作] 移动 (电量--)
[条件] 检查电量: 2
[动作] 充电 (电量++) => 4
[条件] 检查电量: 4
[动作] 移动 (电量--)
[条件] 检查电量: 3
[动作] 移动 (电量--)
[条件] 检查电量: 2
[动作] 充电 (电量++) => 4

跑一次看看得了。

## 小问题

然后之后回答下问的几个小问题。

- 有哪几类节点，控制节点，条件节点，动作节点，继承关系和代码前面已经叙述过，不再重复说明。
- 场上情况获取，其实就是用node.blackboard()访问，黑板，然后场上是外部的呀，怎么写进黑板呢？哦，原来有blackboard->set()这种方法。数据结构就是键值对咯。
- 哦坏了，第三个忘记写了，不管了，问题不大，改动其实很简单，我之前所有的概率都是100%，改一下就有各种情况了，加点随机事件进去


## C-2

哦这个显然局域网下可以用tcp-ip协议，这个很简单，ai都能写，我和袁昊同学合作测试了下ai写的，没问题，放在script里面了。要测试的话你得自己改一改ip，然后程序是双工的，收和发都是一样的。
