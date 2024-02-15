import random

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
    # CARD_TYPES = ["红桃","黑桃","方块","梅花"]
    # CARD_TYPES = ["方块","红桃","方块","红桃"]
    CARD_TYPES = ["黑桃","黑桃","黑桃","黑桃"]
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
    for _ in range(CARDS_SEND_NUM*POSITIONS):
        all_send_cards_list.append(all_cards[card_tp_idx])
        card_tp_idx += 1
    tempory_sent_card_turns = 5
    # 已经发好牌
    # 步骤记录表，记录在移动过程中是否存在圈
    circle_graph_list = []
    # 收好的牌
    closingcards_list = []
    for all_step_counter in range(1000):
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
            print("位置：",pos_tp_idx,";\t牌面数量",len(all_positions[pos_tp_idx]),
                      ";\t(未翻面:%d/翻面:%d)"%(len(all_positions[pos_tp_idx])-abs(tempory_index)+1,abs(tempory_index)-1,),";\t翻面的牌",out_line)
        
        if len(steps_list_idx) == 0:
            print("没有可以移动的牌了")
            break
        else:
            print("可操作步骤：",steps_list_idx)
        # 选择移动牌面最大的那个
        min_move_num = -1
        min_move_idx = -1
        for idx_move_tp,item in enumerate(steps_list_idx):
            if item[0][1]<min_move_num and steps_list_idx[idx_move_tp] not in circle_graph_list:
                min_move_idx = idx_move_tp
                min_move_num = item[0][1]
        if min_move_idx>0:
            selected_move_step = min_move_idx
            print("优化之后的步骤",selected_move_step,steps_list_idx[selected_move_step])
        else:
            # 随机选择一个步骤进行移动
            selected_move_step = random.randint(0,len(steps_list_idx)-1)
            print("随机选择的步骤：",selected_move_step,steps_list_idx[selected_move_step])
        # 将选择好的步骤添加到图当中
        circle_graph_list.append(steps_list_idx[selected_move_step])
        
        cardAidx = steps_list_idx[selected_move_step][0][0]
        cardAnums = steps_list_idx[selected_move_step][0][1]
        cardBidx = steps_list_idx[selected_move_step][1]
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
            print("位置：",pos_tp_idx,";\t牌面数量",len(all_positions[pos_tp_idx]),
                      ";\t(未翻面:%d/翻面:%d)"%(len(all_positions[pos_tp_idx])-abs(tempory_index)+1,abs(tempory_index)-1,),";\t翻面的牌",out_line)
        print("count:",all_step_counter,"---------------------------------")
        if random.random()>0.8 and all_step_counter>50:
            # 发牌操作
            if tempory_sent_card_turns>0:
                print("-----------------------------发牌---------------------------")
                for pos_tp_idx in range(POSITIONS):
                    tempory_card = all_send_cards_list.pop()
                    tempory_card.is_flipped=True
                    all_positions[pos_tp_idx].append(tempory_card)
                tempory_sent_card_turns -= 1
            else:
                print("牌已经发完了")
            
            # 显示移动的结果
            for pos_tp_idx in range(POSITIONS):
                tempory_index = -1
                out_line = ""
                while len(all_positions[pos_tp_idx])>0 and all_positions[pos_tp_idx][tempory_index].is_flipped:
                    out_line = str(all_positions[pos_tp_idx][tempory_index]) +","+ out_line
                    tempory_index -= 1
                    if len(all_positions[pos_tp_idx]) < abs(tempory_index):
                        break    
                print("位置：",pos_tp_idx,";\t牌面数量",len(all_positions[pos_tp_idx]),
                      ";\t(未翻面:%d/翻面:%d)"%(len(all_positions[pos_tp_idx])-abs(tempory_index)+1,abs(tempory_index)-1,),";\t翻面的牌",out_line)
            print("count:",all_step_counter,"---------------------------------")
        # 检查每个位置上的牌面是否满足条件
        for pos_tp_idx in range(POSITIONS):
            if len(all_positions[pos_tp_idx])<CARD_NUMS:
                continue
            
            bool_cards_gotten = False
            for card_tp_idx in range(len(all_positions[pos_tp_idx])):
                
                if all_positions[pos_tp_idx][-card_tp_idx-1].cd_num == card_tp_idx+1:
                    pass
                else:
                    if card_tp_idx == CARD_NUMS:
                        bool_cards_gotten = True
                    break
            if bool_cards_gotten:
                # 收回牌
                print("--------------------------------------收牌--------------------------------------")
                print("牌堆位置",pos_tp_idx)
                tmp_closingcards = []
                for card_tp_idx in range(CARD_NUMS):
                    tmp_closingcards.append(all_positions[pos_tp_idx].pop())
                closingcards_list.append(tmp_closingcards)
                # 检查是否翻面
                all_positions[pos_tp_idx][-1].is_flipped = True
                print("收好的牌：",tmp_closingcards)
                print("牌堆位置",pos_tp_idx,all_positions[pos_tp_idx])
        # 输出当前的状态表
    print("收好牌的数量：",len(closingcards_list),len(closingcards_list)*13)
if __name__ == "__main__":
    main()

