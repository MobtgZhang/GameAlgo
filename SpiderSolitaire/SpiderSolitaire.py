import random
import pprint

class Card:
    def __init__(self,cd_num,cd_type,is_flipped):
        self.cd_num = cd_num
        self.cd_type = cd_type
        self.is_flipped = is_flipped
    def __repr__(self):
        return "( " + str(self.cd_num) + " + "+self.cd_type+ " + " + str(self.is_flipped) + " )"
    def __str__(self):
        return "( " + str(self.cd_num) + " + "+self.cd_type+ " + " + str(self.is_flipped) + " )"
def main():
    CARD_NUMS = 13
    CARD_TYPES = ["红桃","黑桃","方块","梅花"]
    # CARD_TYPES = ["黑桃","黑桃","梅花","梅花"]
    POSITIONS = 10
    POS_CARD_NUMS = 6
    POS_FRONT_NUM = 4
    # 八副牌随机打乱牌面
    all_cards = []
    for _ in range(2):
        for cd_num in range(1,CARD_NUMS+1):
            for cd_type in CARD_TYPES:
                cd_tp = Card(cd_num,cd_type,is_flipped=False)
                all_cards.append(cd_tp)
    random.shuffle(all_cards)
    # 初始化位置
    all_positions = []
    card_tp_idx = 0
    for idx in range(POSITIONS):
        tmp_cards_list = []
        if idx<POS_FRONT_NUM:
            for _ in range(POS_CARD_NUMS-1):
                tmp_cards_list.append(all_cards[card_tp_idx])
                card_tp_idx += 1
            tmp_card = all_cards[card_tp_idx]
            tmp_card.is_flipped = True
            tmp_cards_list.append(tmp_card)
            card_tp_idx += 1
        else:
            for _ in range(POS_CARD_NUMS-2):
                
                tmp_cards_list.append(all_cards[card_tp_idx])
                card_tp_idx += 1
            tmp_card = all_cards[card_tp_idx]
            tmp_card.is_flipped = True
            tmp_cards_list.append(tmp_card)
            card_tp_idx += 1
        all_positions.append(tmp_cards_list)
    # 初始化发牌的序列
    all_send_cards_list = []
    CARDS_SEND_NUM = 5
    for _ in range(CARDS_SEND_NUM):
        tp_card_list = []
        for _ in range(POSITIONS):
            tp_card_list.append(all_cards[card_tp_idx])
            card_tp_idx += 1
        all_send_cards_list.append(card_tp_idx)
    # 已经发好牌
    # 这里是尝试50次数
    for all_step_counter in range(50):
        # 检查可以走的状态
        steps_list_idx = []
        for idx in range(POSITIONS):
            card_list_A = all_positions[idx]
            if len(card_list_A) == 0:
                continue
            tp_index = -1
            
            while len(card_list_A)>0 and card_list_A[tp_index].is_flipped:
                if tp_index == -1:
                    pass
                else:
                    # 检查这一列是否为相同花色的连续正序列，如果是则可以移动一串牌面，否则不能移动。
                    if card_list_A[tp_index].cd_num - card_list_A[tp_index+1].cd_num == 1 and \
                        card_list_A[tp_index].cd_type == card_list_A[tp_index+1].cd_type:
                            pass
                    else:
                        break
                for idy in range(POSITIONS):
                    if idx!=idy:
                        # 比较剩下的牌面是否可以放在另外一个牌B上面
                        card_list_B = all_positions[idy]
                        if len(card_list_B) == 0:
                            # A可以放B上面
                            steps_list_idx.append([(idx,tp_index),idy])
                        elif card_list_B[-1].cd_num - card_list_A[tp_index].cd_num == 1:
                            # A可以放B上面
                            steps_list_idx.append([(idx,tp_index),idy])
                        else:
                            continue
                tp_index -= 1
                if len(all_positions[idx]) < abs(tp_index):
                    break  
        # 显示移动的结果
        for pos_tp_idx in range(POSITIONS):
            tempory_index = -1
            out_line = ""
            while len(all_positions[pos_tp_idx])>0 and all_positions[pos_tp_idx][tempory_index].is_flipped:
                out_line = str(all_positions[pos_tp_idx][tempory_index]) +","+ out_line
                tempory_index -= 1
                if len(all_positions[pos_tp_idx]) < abs(tempory_index):
                    break  
            print("位置：",pos_tp_idx,";\t牌面数量:",len(all_positions[pos_tp_idx]),";\t翻面的牌",out_line)
        
        if len(steps_list_idx) == 0:
            print("没有可以移动的牌了")
            break
        else:
            print("可操作步骤：",steps_list_idx)
        # 随机选择一个步骤进行移动
        rand_step = random.randint(0,len(steps_list_idx)-1)
        print("随机选择的步骤：",rand_step,steps_list_idx[rand_step])
        cardAidx = steps_list_idx[rand_step][0][0]
        cardAnums = steps_list_idx[rand_step][0][1]
        cardBidx = steps_list_idx[rand_step][1]
        for idx in range(cardAnums,0):
            cardA = all_positions[cardAidx][idx]
            all_positions[cardBidx].append(cardA)
        
        for _ in range(cardAnums,0):
            cardA = all_positions[cardAidx].pop()
        if len(all_positions[cardAidx]) == 0:
            pass
        elif not all_positions[cardAidx][-1].is_flipped:
            all_positions[cardAidx][-1].is_flipped = True
        else:
            pass
        # 显示移动的结果
        for pos_tp_idx in range(POSITIONS):
            tempory_index = -1
            out_line = ""
            while len(all_positions[pos_tp_idx])>0 and all_positions[pos_tp_idx][tempory_index].is_flipped:
                out_line = str(all_positions[pos_tp_idx][tempory_index]) +","+ out_line
                tempory_index -= 1
                if len(all_positions[pos_tp_idx]) < abs(tempory_index):
                    break    
            print("位置：",pos_tp_idx,";\t牌面数量",len(all_positions[pos_tp_idx]),";\t翻面的牌",out_line)
        print("count:",all_step_counter,"---------------------------------")
if __name__ == "__main__":
    main()

    