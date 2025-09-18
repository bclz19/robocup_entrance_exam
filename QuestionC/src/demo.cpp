// 引入核心库：行为树工厂、延时和输出
#include <behaviortree_cpp/bt_factory.h>
#include <chrono>
#include <thread>
#include <iostream>

// 电量
int g_battery = 3;  // 初始值3

// 条件节点：检查电量 > 2
BT::NodeStatus CheckBattery(BT::TreeNode& node) {
    std::cout << "[条件] 检查电量: " << g_battery << std::endl;
    return (g_battery > 2) ? BT::NodeStatus::SUCCESS : BT::NodeStatus::FAILURE;
}

// 动作节点：移动，消耗1电量
BT::NodeStatus Move(BT::TreeNode& node) {
    std::cout << "[动作] 移动 (电量--)" << std::endl;
    g_battery -= 1;
    if (g_battery < 0) g_battery = 0;
    std::this_thread::sleep_for(std::chrono::milliseconds(200));  // 短延时模拟
    return BT::NodeStatus::SUCCESS;  // 总是成功
}

// 动作节点：充电，增加2电量
BT::NodeStatus Recharge(BT::TreeNode& node) {
    std::cout << "[动作] 充电 (电量++) => " << (g_battery += 2) << std::endl;
    if (g_battery > 10) g_battery = 10;
    std::this_thread::sleep_for(std::chrono::milliseconds(200));  // 短延时模拟
    return BT::NodeStatus::SUCCESS;  // 总是成功
}

int main() {
    // 创建工厂
    BT::BehaviorTreeFactory factory;

    // 注册3个节点
    factory.registerSimpleCondition("CheckBattery", std::bind(CheckBattery, std::placeholders::_1));
    factory.registerSimpleAction("Move", std::bind(Move, std::placeholders::_1));
    factory.registerSimpleAction("Recharge", std::bind(Recharge, std::placeholders::_1));

    // Fallback根节点，优先Sequence（检查+移动），失败则充电
    auto xml_text = R"(
<root main_tree_to_execute="SimpleTree" BTCPP_format="4">
  <BehaviorTree ID="SimpleTree">
    <Fallback name="root">
      <Sequence name="move_seq">
        <CheckBattery/>
        <Move/>
      </Sequence>
      <Recharge/>
    </Fallback>
  </BehaviorTree>
</root>
)";

    // 创建树
    auto tree = factory.createTreeFromText(xml_text);
    std::cout << "=== 行为树启动 ===" << std::endl;

    // 循环tick 5次
    for (int i = 0; i < 5; ++i) {
        tree.tickOnce();
        std::this_thread::sleep_for(std::chrono::milliseconds(800));  // 间隔0.8秒
    }
    return 0;
}
