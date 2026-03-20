# ...existing code...
class RandomForest:
    @classmethod
    def add_vectors(cls, v1, v2):
        return [sum(i) for i in zip(v1, v2)]

    @staticmethod
    def _safe_get(inp, idx, default=0.0):
        return inp[idx] if idx < len(inp) else default

    @classmethod
    def score(cls, input):
        """
        对 7 个组分别打票，每组由三个值 x,y,z 构成（组起始索引按 0,21,42,...126）。
        返回长度为3的累计 votes 列表：[votes_still, votes_walk, votes_fall]
        """
        # 阈值常量（可调）
        Z_STILL_TH = 9.019443988800049
        XY_WALK_LOW = 2.254075527191162
        XY_WALK_HIGH = 8.019443988800049
        XY_FALL_TH = 8.019443988800049

        votes = [0.0, 0.0, 0.0]

        # 7 组，起始索引间隔 21
        for g in range(7):
            base = g * 21
            x = abs(cls._safe_get(input, base, 0.0))
            y = abs(cls._safe_get(input, base + 1, 0.0))
            z = abs(cls._safe_get(input, base + 2, 0.0))

            # 优先判断静止（z 接近重力方向/大值）
            if z >= Z_STILL_TH:
                var = [1.0, 0.0, 0.0]  # 静止
            # 行走：x,y 在中间区间
            elif (x >= XY_WALK_LOW and x <= XY_WALK_HIGH) and (y >= XY_WALK_LOW and y <= XY_WALK_HIGH):
                var = [0.0, 1.0, 0.0]  # 行走
            # 摔倒：x 或 y 极大
            elif (x >= XY_FALL_TH) or (y >= XY_FALL_TH):
                var = [0.0, 0.0, 1.0]  # 摔倒
            else:
                # 默认归为行走（可根据实际数据改为更保守策略）
                var = [0.0, 1.0, 0.0]

            votes = cls.add_vectors(votes, var)

        return votes

    @classmethod
    def run(cls, input: list):
        res = cls.score(input)
        print(res)
        return res.index(max(res))
# ...existing code...
