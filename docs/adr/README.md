# 决定记录（ADR）

每个关键决定一份文件。状态有三种：

- **已确定**：产品负责人已确认。任何 agent 不得推翻，只能提议修改。
- **提议中**：评审员的建议，等产品负责人确认。确认前可以作为工作假设，但不能当作既定事实引用。
- **已废弃**：被后来的决定取代，文件保留，注明被哪一条取代。

| 编号 | 决定 | 状态 |
|---|---|---|
| [ADR-001](ADR-001-wired-input-first.md) | 接线路线优先 | 已确定 |
| [ADR-002](ADR-002-buy-before-build.md) | 先买后造，阶段 0 不写应用代码 | 提议中 |
| [ADR-003](ADR-003-verify-not-transcribe.md) | 做验证而不是听写，判错必须有正面证据 | 提议中 |
| [ADR-004](ADR-004-onset-pitch-split-sample-clock.md) | 起音和音高分开，评分用采样时间戳 | 提议中 |
| [ADR-005](ADR-005-cross-platform-core-offline-first.md) | 核心算法做成跨平台 C++ 库，Windows 离线先行 | 已确定 |
| [ADR-006](ADR-006-hardware-direct-monitoring.md) | 硬件直接监听加有线耳机，第一版不做软件监听和蓝牙 | 已确定 |
| [ADR-007](ADR-007-input-abstraction-note-events.md) | 输入层抽象为统一的音符事件 | 提议中 |
| [ADR-008](ADR-008-personal-data-outside-repo.md) | 个人数据和代码分开存放 | 已确定 |
| [ADR-009](ADR-009-first-algorithm-choice.md) | 第一版算法选型 | 提议中 |

新增决定时，复制任意一份的结构，编号顺延，并更新这张表。
