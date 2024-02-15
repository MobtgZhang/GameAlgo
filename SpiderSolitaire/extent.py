import argparse
import random
import pathlib
import pprint
import logging

logger = logging.getLogger(__name__)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hard",action="store_true")
    parser.add_argument("--medium",action="store_true")
    parser.add_argument("--easy",action="store_false")
    parser.add_argument("--debug",action="store_false")
    parser.add_argument("--logdir",type=pathlib.Path,default="logs/")
    args = parser.parse_args()
    return args
class Card:
    def __init__(self,cd_num,cd_type,is_flipped):
        self.cd_num = cd_num
        self.cd_type = cd_type
        self.is_flipped = is_flipped
    def __repr__(self):
        return "( " + str(self.cd_num) + " + "+self.cd_type+ " + " + str(self.is_flipped) + " )"
    def __str__(self):
        return "( " + str(self.cd_num) + " + "+self.cd_type+ " + " + str(self.is_flipped) + " )"
def display_positions(all_positions):
    # 显示移动的结果
    for pos_tp_idx in range(len(all_positions)):
        tempory_index = -1
        out_line = ""
        while len(all_positions[pos_tp_idx])>0 and all_positions[pos_tp_idx][tempory_index].is_flipped:
            out_line = str(all_positions[pos_tp_idx][tempory_index]) +","+ out_line
            tempory_index -= 1
            if len(all_positions[pos_tp_idx]) < abs(tempory_index):
                break  
        logger.info("位置：%d;\t牌面数量：%d;\t(未翻面:%d/翻面:%d);\t翻面的牌 %s" 
                    %(pos_tp_idx,len(all_positions[pos_tp_idx]),
                      len(all_positions[pos_tp_idx])-abs(tempory_index)+1,abs(tempory_index)-1,str(out_line)))
def main(args):
    if args.easy:
        CARD_TYPES = ["黑桃","黑桃","黑桃","黑桃"]
    elif args.medium:
        CARD_TYPES = ["方块","红桃","方块","红桃"]
    elif args.hard:
        CARD_TYPES = ["红桃","黑桃","方块","梅花"]
    else:
        raise RuntimeError("请你定义好难度标准")
    CARD_NUMS = 13
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
    for all_step_counter in range(5000):
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
        display_positions(all_positions)
        if len(steps_list_idx) == 0:
            logger.info("没有可以移动的牌了")
            break
        else:
            logger.info("可操作步骤：%s"%str(steps_list_idx))
        # 选择移动牌面最大的那个
        min_move_num = -1
        min_move_idx = -1
        for idx_move_tp,item in enumerate(steps_list_idx):
            if item[0][1]<min_move_num and steps_list_idx[idx_move_tp] not in circle_graph_list:
                min_move_idx = idx_move_tp
                min_move_num = item[0][1]
        if min_move_idx>0:
            selected_move_step = min_move_idx
            logger.info("优化之后的步骤：%d\t%s"%(selected_move_step,str(steps_list_idx[selected_move_step])))
        else:
            # 随机选择一个步骤进行移动
            selected_move_step = random.randint(0,len(steps_list_idx)-1)
            logger.info("随机选择的步骤：%d\t%s"%(selected_move_step,steps_list_idx[selected_move_step]))
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
        display_positions(all_positions)
        logger.info("count: "+str(all_step_counter)+" ---------------------------------")
        if random.random()>0.8 and all_step_counter>50:
            # 发牌操作
            if tempory_sent_card_turns>0:
                logger.info("-----------------------------发牌---------------------------")
                #print("-----------------------------发牌---------------------------")
                for pos_tp_idx in range(POSITIONS):
                    tempory_card = all_send_cards_list.pop()
                    tempory_card.is_flipped=True
                    all_positions[pos_tp_idx].append(tempory_card)
                tempory_sent_card_turns -= 1
            else:
                logger.info("牌已经发完了")
                #print("牌已经发完了")
            
            # 显示移动的结果
            display_positions(all_positions)
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
                logger.info("--------------------------------------收牌--------------------------------------")
                logger.info("牌堆位置："+str(pos_tp_idx))
                print("--------------------------------------收牌--------------------------------------")
                print("牌堆位置：",str(pos_tp_idx))
                tmp_closingcards = []
                for card_tp_idx in range(CARD_NUMS):
                    tmp_closingcards.append(all_positions[pos_tp_idx].pop())
                closingcards_list.append(tmp_closingcards)
                # 检查是否翻面
                all_positions[pos_tp_idx][-1].is_flipped = True
                logger.info("收好的牌："+str(tmp_closingcards))
                logger.info("牌堆位置： "+str(pos_tp_idx)+"\t"+str(all_positions[pos_tp_idx]))
                print("收好的牌：",tmp_closingcards)
                print("牌堆位置： ",pos_tp_idx)
                pprint.pprint(all_positions[pos_tp_idx])
        # 输出当前的状态表
    logger.info("收好牌的数量："+str(len(closingcards_list))+"\t"+str(len(closingcards_list)*13))
    print("收好牌的数量：",len(closingcards_list),len(closingcards_list)*13)
if __name__ == "__main__":
    args = get_args()
    # setting logging
    logging.captureWarnings(True)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    # 终端输出
    #ch = logging.StreamHandler()
    #ch.setLevel(logging.DEBUG if args.debug else logging.INFO)
    #ch.setFormatter(formatter)
    #root_logger.addHandler(ch)
    # 文件输出
    if not args.logdir.exists():
        logging.debug(f'Creating directory: {args.logdir}')
        args.logdir.mkdir(parents=True)
    fh = logging.FileHandler(args.logdir / 'spider.log',mode="w")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    root_logger.addHandler(fh)
    
    main(args)

